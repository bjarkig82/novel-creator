#!/usr/bin/env bash
# Literal Bash guide, with the documented identified-wheel prepublication substitution.
set -euo pipefail
source_root=${1:?source path required}
wheel_directory=${2:?verified candidate directory required}
base_python=${3:?Python with normal pip/venv support required}
mkdir -p "$HOME/.cache/novel-creator-verification"
scratch=$(mktemp -d "$HOME/.cache/novel-creator-verification/release-guide.XXXXXX")
printf '%s\n' "$scratch"
export HOME="$scratch"
export GIT_CONFIG_GLOBAL="$scratch/.gitconfig"
export GIT_CONFIG_NOSYSTEM=1
printf '[user]\nname = Disposable Bash Guide\nemail = guide@example.invalid\n' > "$GIT_CONFIG_GLOBAL"
export PATH="$(dirname "$base_python"):$PATH"
unset PYTHONPATH PYTHONHOME
python3 --version
git --version
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
runtime="$HOME/NovelCreatorRuntime"
python3 -m venv "$runtime"
"$runtime/bin/python" -m pip install --no-cache-dir --index-url https://pypi.org/simple "$wheel_directory"/*.whl
source "$runtime/bin/activate"
novel-creator --version
novel-creator init --help
mkdir "$HOME/Novels"
cd "$HOME/Novels"
novel-creator init 'My Novel'
cd 'My Novel'
"$runtime/bin/python" .novel-creator/run.py context --novel . --json
"$runtime/bin/python" .novel-creator/run.py session list --novel . --json
"$runtime/bin/python" .novel-creator/run.py inspect --novel . --kind novel_project --json
novel-creator init 'Bref' --path "$HOME/Novels/Bref" --title 'Bréf frá morgundeginum' --language is
python -c 'import sys; print(sys.executable)'
"$runtime/bin/python" "$source_root/tests/verify_guide_failures.py" \
    --python "$runtime/bin/python" --console "$runtime/bin/novel-creator" \
    --workspace "$scratch/troubleshooting" > "$scratch/troubleshooting.json"
cat "$scratch/troubleshooting.json"
printf 'RELEASE_GUIDE_ROOT=%s\n' "$scratch"
