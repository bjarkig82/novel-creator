"""Instrument only the isolated pinned Git checkout, after baseline preservation."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path.cwd()
base = root / '.tools/t172-git-native-20261028'
source = base / 'source'
expected = 'f8165afd89b0c190677a093f20894f5fce12f97a'
assert subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip() == expected
assert not subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'])
assert (base / 'baseline/git.exe').is_file(), 'Preserve the unmodified build first'

header = '''/* Diagnostic only: owner-thread inclusive/exclusive native timers. */
#ifndef T172_PROFILE_H
#define T172_PROFILE_H
enum t172_kind { T172_LOOKUP, T172_SERIALIZE, T172_OBJECT_WRITE,
                 T172_DEFLATE, T172_FSYNC, T172_KINDS };
uint64_t t172_profile_begin(enum t172_kind kind);
void t172_profile_end(enum t172_kind kind, uint64_t start);
#endif
'''
implementation = r'''
/* This diagnostic state is thread-local; unrelated commands/threads stay off. */
struct t172_frame { enum t172_kind kind; uint64_t start, child; };
static __declspec(thread) int t172_active, t172_depth;
static __declspec(thread) struct t172_frame t172_stack[32];
static __declspec(thread) uint64_t t172_calls[T172_KINDS];
static __declspec(thread) uint64_t t172_inclusive[T172_KINDS];
static __declspec(thread) uint64_t t172_exclusive[T172_KINDS];
static uint64_t t172_total_start, t172_clock_pairs;

uint64_t t172_profile_begin(enum t172_kind kind)
{
    uint64_t start;
    int saved_errno = errno;
    if (!t172_active)
        return 0;
    start = getnanotime();
    if (t172_depth >= 32)
        BUG("T172 diagnostic nesting overflow");
    t172_stack[t172_depth].kind = kind;
    t172_stack[t172_depth].start = start;
    t172_stack[t172_depth++].child = 0;
    errno = saved_errno;
    return start;
}

void t172_profile_end(enum t172_kind kind, uint64_t start)
{
    uint64_t elapsed, child;
    int saved_errno = errno;
    if (!start)
        return;
    elapsed = getnanotime() - start;
    if (!t172_depth || t172_stack[t172_depth - 1].kind != kind ||
        t172_stack[t172_depth - 1].start != start)
        BUG("T172 diagnostic nesting mismatch");
    child = t172_stack[--t172_depth].child;
    if (child > elapsed)
        BUG("T172 diagnostic elapsed mismatch");
    t172_calls[kind]++;
    t172_inclusive[kind] += elapsed;
    t172_exclusive[kind] += elapsed - child;
    if (t172_depth)
        t172_stack[t172_depth - 1].child += elapsed;
    errno = saved_errno;
}

static void t172_profile_start(void)
{
    const char *enabled = getenv("GIT_T172_PROFILE");
    int i, saved_errno = errno;
    uint64_t start;
    t172_active = enabled && !strcmp(enabled, "1");
    if (!t172_active)
        return;
    memset(t172_calls, 0, sizeof(t172_calls));
    memset(t172_inclusive, 0, sizeof(t172_inclusive));
    memset(t172_exclusive, 0, sizeof(t172_exclusive));
    t172_depth = 0;
    t172_clock_pairs = 0;
    for (i = 0; i < 1000; i++) {
        start = getnanotime();
        t172_clock_pairs += getnanotime() - start;
    }
    t172_total_start = getnanotime();
    errno = saved_errno;
}

static void t172_profile_report(int result)
{
    static const char *names[] = { "lookup", "serialize", "object_write", "deflate", "fsync" };
    uint64_t elapsed;
    int i, saved_errno = errno;
    if (!t172_active)
        return;
    elapsed = getnanotime() - t172_total_start;
    t172_active = 0;
    if (t172_depth)
        BUG("T172 diagnostic unfinished frames");
    fprintf(stderr, "T172_PROFILE {\"result\":%d,\"total_ns\":%"PRIuMAX
            ",\"clock_1000_pairs_ns\":%"PRIuMAX",\"metrics\":{",
            result, (uintmax_t)elapsed, (uintmax_t)t172_clock_pairs);
    for (i = 0; i < T172_KINDS; i++)
        fprintf(stderr, "%s\"%s\":{\"calls\":%"PRIuMAX
                ",\"inclusive_ns\":%"PRIuMAX",\"exclusive_ns\":%"PRIuMAX"}",
                i ? "," : "", names[i], (uintmax_t)t172_calls[i],
                (uintmax_t)t172_inclusive[i], (uintmax_t)t172_exclusive[i]);
    fprintf(stderr, "}}\n");
    errno = saved_errno;
}
'''

files = ('cache-tree.c', 'odb.c', 'git-zlib.c', 'wrapper.c')
before = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in files}
texts = {name: (source / name).read_text(encoding='utf-8') for name in files}
for name in files:
    needle = '#include "git-compat-util.h"'
    assert texts[name].count(needle) == 1
    texts[name] = texts[name].replace(needle, needle + '\n#include "t172-profile.h"', 1)

needle = 'int cache_tree_update(struct index_state *istate, int flags)'
assert texts['cache-tree.c'].count(needle) == 1
texts['cache-tree.c'] = texts['cache-tree.c'].replace(needle, implementation + '\n' + needle, 1)
needle = '\ttrace2_region_enter("cache_tree", "update", the_repository);'
assert texts['cache-tree.c'].count(needle) == 1
texts['cache-tree.c'] = texts['cache-tree.c'].replace(needle, needle + '\n\tt172_profile_start();', 1)
needle = '\todb_transaction_commit(transaction);'
assert texts['cache-tree.c'].count(needle) == 1
texts['cache-tree.c'] = texts['cache-tree.c'].replace(needle, needle + '\n\tt172_profile_report(i);', 1)
needle = '''		strbuf_grow(&buffer, entlen + 100);
		strbuf_addf(&buffer, "%o %.*s%c", mode, entlen, path + baselen, '\\0');
		strbuf_add(&buffer, oid->hash, the_hash_algo->rawsz);'''
assert texts['cache-tree.c'].count(needle) == 1
texts['cache-tree.c'] = texts['cache-tree.c'].replace(needle,
    '\t\t{\n\t\t\tuint64_t t172_start = t172_profile_begin(T172_SERIALIZE);\n' + needle +
    '\n\t\t\tt172_profile_end(T172_SERIALIZE, t172_start);\n\t\t}', 1)

wrappers = (
    ('odb.c', 'int odb_has_object(', 'static int t172_real_odb_has_object(', '''
int odb_has_object(struct object_database *odb, const struct object_id *oid, unsigned flags)
{
    uint64_t start = t172_profile_begin(T172_LOOKUP);
    int result = t172_real_odb_has_object(odb, oid, flags);
    t172_profile_end(T172_LOOKUP, start);
    return result;
}
'''),
    ('odb.c', 'int odb_write_object_ext(', 'static int t172_real_odb_write_object_ext(', '''
int odb_write_object_ext(struct object_database *odb, const void *buf, unsigned long len,
                        enum object_type type, struct object_id *oid,
                        struct object_id *compat_oid, unsigned flags)
{
    uint64_t start = t172_profile_begin(T172_OBJECT_WRITE);
    int result = t172_real_odb_write_object_ext(odb, buf, len, type, oid, compat_oid, flags);
    t172_profile_end(T172_OBJECT_WRITE, start);
    return result;
}
'''),
    ('git-zlib.c', 'int git_deflate(', 'static int t172_real_git_deflate(', '''
int git_deflate(git_zstream *stream, int flush)
{
    uint64_t start = t172_profile_begin(T172_DEFLATE);
    int result = t172_real_git_deflate(stream, flush);
    t172_profile_end(T172_DEFLATE, start);
    return result;
}
'''),
    ('wrapper.c', 'int git_fsync(', 'static int t172_real_git_fsync(', '''
int git_fsync(int fd, enum fsync_action action)
{
    uint64_t start = t172_profile_begin(T172_FSYNC);
    int result = t172_real_git_fsync(fd, action);
    t172_profile_end(T172_FSYNC, start);
    return result;
}
'''),
)
for file, old, renamed, wrapper in wrappers:
    assert texts[file].count(old) == 1, old
    texts[file] = texts[file].replace(old, renamed, 1) + wrapper
for name, text in texts.items():
    (source / name).write_text(text, encoding='utf-8', newline='\n')
(source / 't172-profile.h').write_text(header, encoding='utf-8', newline='\n')
manifest = {'upstream_commit': expected, 'before_sha256': before,
    'after_sha256': {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in (*files, 't172-profile.h')},
    'scope': 'Diagnostic-only opt-in owner-thread timers; original return values, calls and errno retained. '
             'Exclusive timings exclude nested instrumented operations; native clock overhead is not subtracted.'}
(root / 'tests/evaluations/windows-phase22-native-git-instrumentation-20261028.json').write_text(
    json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
patch = subprocess.check_output(['git', '-C', str(source), 'diff', '--no-ext-diff', '--binary'])
(root / 'tests/evaluations/windows-phase22-native-git-instrumentation-20261028.patch').write_bytes(patch)
print(json.dumps(manifest, indent=2))
