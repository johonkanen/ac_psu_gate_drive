#!/usr/bin/env bash
# Regenerate both sheets into place and fail if any committed sheet file changed (git diff).
set -u
cd "$(dirname "$0")/.."
for s in tools/sheets/sheet[0-9][0-9].py; do python3 "$s" >/dev/null || exit 1; done
if git ls-files --error-unmatch kicad/01_gate_drivers.kicad_sch >/dev/null 2>&1; then
    git diff --quiet -- kicad/*.kicad_sch || { echo "check_sheets: sheet scripts and kicad/*.kicad_sch differ"; git diff --stat -- kicad/*.kicad_sch; exit 1; }
fi
echo "check_sheets: 2 sheets regenerated, identical"
