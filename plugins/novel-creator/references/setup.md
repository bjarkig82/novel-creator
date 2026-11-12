# Private runtime and failure recovery

The bootstrap uses only the standard library. Invoke it with Python >=3.11;
it checks Git >=2.39 and supports Windows and Linux. It does not activate an
environment or change global pip, PATH, Git or host settings. Proxy, certificate
and package-index settings are retained from the environment and from pip's
effective system/user/site or explicit PIP_CONFIG_FILE configuration. Setup reads
configuration using the private runtime's isolated interpreter, copies only
global/install proxy, cert, client-cert, index-url and extra-index-url options,
then disables configuration files for installation. Install-specific settings
override global settings; inherited PIP_* transport settings keep precedence.
Empty configuration or environment values are ignored as in pip, so they do not
erase a nonempty network setting from a lower-priority scope.
Destination overrides such as target, prefix, user and python are excluded.
Configuration output is captured privately, never logged or printed.

Linux uses `${XDG_CACHE_HOME:-~/.cache}/novel-creator/runtimes/0.8.0`.
Windows uses `%LOCALAPPDATA%/NovelCreator/runtimes/0.8.0`.
Use `--novel PATH` so setup can reject caches inside the intended book. Cache
paths must not redirect through symlinks or junctions or live within the plugin.
No runtime files are written to the book or plugin cache.

Without `--wheel`, bootstrap installs the exact manifest requirement,
`novel-creator==0.8.0`, from PyPI through the configured package index.
Use `--wheel PATH` for an unpublished local candidate or explicit local
validation; the wheel's product and exact version are checked before install and
its bytes establish runtime provenance. Plugin installation alone does not prove
PyPI availability. If the pinned version is missing, report the actual index
failure; use a matching local wheel only when available for the intended setup.
Changed candidate bytes or a different package source need a separate
XDG_CACHE_HOME/LOCALAPPDATA. Do not change HOME or CODEX_HOME.

Success is JSON `ok: true` with `data.runtime_python`, `version` and `reused`.
Reuse requires an exact, isolated installed package and healthy dependencies.
Failures return clean JSON `ok: false` with an actionable error and nonzero exit.
Install/create failures preserve an owned partial runtime for a same-source
retry. Occupied unknown directories are preserved and refused. A concurrent
`<version>.lock` is never automatically deleted: wait for its setup to finish;
after a crash, verify no setup process remains before manually removing that
specific lock. Lock cleanup closes its handle before deleting the same lock,
including on Windows, and preserves a replacement lock. Do not remove runtime
directories blindly.

Bootstrap creates only a runtime. The setup skill then uses its returned
interpreter to initialize exactly one new format-1 notebook. Notebook-init
failures preserve all partial files and need diagnosis before any retry.
Successful initialization must never be repeated. Existing legacy and
standalone notebook adoption is unsupported by this plugin.
