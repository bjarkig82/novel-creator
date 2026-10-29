#!/usr/bin/env bash
# Isolated WSL/ext4 verification; no system packages, real novels or cleanup deletes.
set -euo pipefail
source_root=${1:?source checkout path required}
installer_python=${2:?existing private Python with pip required}
wheel_directory=${3:-$source_root/dist/package-init-local}
test -f "$source_root/pyproject.toml"
mkdir -p "$HOME/.cache/novel-creator-verification"
snapshot=$(mktemp -d "$HOME/.cache/novel-creator-verification/package-init.XXXXXX")
printf '%s\n' "$snapshot"
tar -C "$source_root" --exclude=./.git --exclude=./.venv --exclude=./.tools \
    --exclude=./dist --exclude=./build --exclude=./src/novel_creator.egg-info -cf - . |
    tar -xf - -C "$snapshot"
find "$snapshot" -type f -exec chmod 644 {} +
python3 -m venv --without-pip "$snapshot/.runtime"
"$installer_python" -m pip --python "$snapshot/.runtime/bin/python" install pip \
    "$wheel_directory"/*.whl > "$snapshot/install.txt" 2>&1
# Source tests explicitly launch the src layout; install its editable resource
# mappings only in this private source-test runtime. Clean package checks below
# create another environment and never inherit these sites.
"$snapshot/.runtime/bin/python" -m pip install -e "$snapshot" > "$snapshot/editable-install.txt" 2>&1
cd "$snapshot"
git init -q -b main
git config user.name 'Disposable Linux Verification'
git config user.email linux@example.invalid
"$snapshot/.runtime/bin/python" -m unittest discover -q > "$snapshot/tests.txt" 2>&1
tail -8 "$snapshot/tests.txt"
"$snapshot/.runtime/bin/python" tests/verify_package_install.py \
    --wheel "$wheel_directory"/*.whl > "$snapshot/clean-install.json" 2>&1
cat "$snapshot/clean-install.json"
