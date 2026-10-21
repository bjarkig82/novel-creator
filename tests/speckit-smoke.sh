#!/usr/bin/env bash
# Exercise the checked-in Bash workflow without changing the working checkout.
set -euo pipefail

repo_root="$(CDPATH='' cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fixture="$(mktemp -d)"
trap 'rm -rf "$fixture"' EXIT
mkdir -p "$fixture/repo with spaces"
cp -R "$repo_root/.specify" "$fixture/repo with spaces/"
cd "$fixture/repo with spaces"
rm -f .specify/feature.json
unset SPECIFY_FEATURE_DIRECTORY SPECIFY_FEATURE SPECIFY_INIT_DIR

for script in .specify/scripts/bash/*.sh; do
    bash -n "$script"
done
for name in check-prerequisites create-new-feature resolve-template setup-plan setup-tasks; do
    bash ".specify/scripts/bash/$name.sh" --help > /dev/null
done

# A fresh cloud checkout can resolve templates without a CLI installation.
bash .specify/scripts/bash/resolve-template.sh spec-template --json > "$fixture/template.json"
jq -e '.TEMPLATE_NAME == "spec-template" and (.TEMPLATE_CONTENT | length > 0)' "$fixture/template.json" > /dev/null

# Read-only feature selection must not overwrite per-checkout state.
export SPECIFY_FEATURE_DIRECTORY=specs/001-cloud-smoke
bash .specify/scripts/bash/check-prerequisites.sh --json --paths-only > "$fixture/paths.json"
jq -e '.FEATURE_DIR | startswith("/") and endswith("/specs/001-cloud-smoke")' "$fixture/paths.json" > /dev/null
test ! -f .specify/feature.json
unset SPECIFY_FEATURE_DIRECTORY

# Feature creation supplies the persisted pointer for subsequent commands.
bash .specify/scripts/bash/create-new-feature.sh --json --short-name cloud-smoke 'Cloud smoke test' > "$fixture/feature.json"
jq -e '.SPEC_FILE | endswith("/specs/001-cloud-smoke/spec.md")' "$fixture/feature.json" > /dev/null
test -s specs/001-cloud-smoke/spec.md
bash .specify/scripts/bash/setup-plan.sh --json > "$fixture/plan.json"
jq -e '.IMPL_PLAN | endswith("/specs/001-cloud-smoke/plan.md")' "$fixture/plan.json" > /dev/null
cmp .specify/templates/plan-template.md specs/001-cloud-smoke/plan.md

# Re-running planning must preserve authored work.
printf '\nAuthored plan content\n' >> specs/001-cloud-smoke/plan.md
cp specs/001-cloud-smoke/plan.md "$fixture/saved-plan.md"
bash .specify/scripts/bash/setup-plan.sh --json > "$fixture/plan.json"
cmp "$fixture/saved-plan.md" specs/001-cloud-smoke/plan.md

bash .specify/scripts/bash/setup-tasks.sh --json > "$fixture/tasks.json"
jq -e '.AVAILABLE_DOCS == [] and (.TASKS_TEMPLATE_CONTENT | length > 0)' "$fixture/tasks.json" > /dev/null
if bash .specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks > "$fixture/check.json" 2> "$fixture/error.txt"; then
    echo 'ERROR: Missing tasks.md should fail prerequisite checks' >&2
    exit 1
fi
if command -v rg >/dev/null 2>&1; then
    rg -q '\$speckit-tasks' "$fixture/error.txt"
else
    grep -Fq '$speckit-tasks' "$fixture/error.txt"
fi
printf '# Tasks\n' > specs/001-cloud-smoke/tasks.md
bash .specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks > "$fixture/check.json"
jq -e '.AVAILABLE_DOCS | index("tasks.md") != null' "$fixture/check.json" > /dev/null

# Check template overrides through both standalone and checklist commands.
mkdir -p .specify/templates/overrides
printf '# Custom checklist\n' > .specify/templates/overrides/checklist-template.md
bash .specify/scripts/bash/resolve-template.sh checklist-template --json > "$fixture/template.json"
jq -e '.TEMPLATE_CONTENT == "# Custom checklist\n"' "$fixture/template.json" > /dev/null
bash .specify/scripts/bash/check-prerequisites.sh --json --template checklist-template > "$fixture/check.json"
jq -e '.TEMPLATE_CONTENT == "# Custom checklist\n"' "$fixture/check.json" > /dev/null

# Dry runs must not change the selected feature or create spec directories.
cp .specify/feature.json "$fixture/saved-feature.json"
bash .specify/scripts/bash/create-new-feature.sh --json --dry-run --short-name next-feature 'Next feature' > "$fixture/dry-run.json"
jq -e '.SPEC_FILE | endswith("/specs/002-next-feature/spec.md")' "$fixture/dry-run.json" > /dev/null
test ! -d specs/002-next-feature
cmp "$fixture/saved-feature.json" .specify/feature.json

echo 'Spec Kit Bash smoke checks passed.'
