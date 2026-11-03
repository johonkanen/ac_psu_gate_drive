#!/usr/bin/env bash
# Run every verification step. Exit status is non-zero if any step fails.
# The tools are the proteus2kicad submodule in tools/p2k; board values in p2k_config.py.
set -u
cd "$(dirname "$0")/.."
[ -x tools/p2k/bin/p2k ] || { echo "tools/p2k missing: git submodule update --init"; exit 1; }
fail=0
step() { echo "== $1"; shift; "$@" || { echo "!! FAILED: $*"; fail=1; }; }

step "KiCad environment" tools/p2k/bin/kipy -c "import pcbnew; v = pcbnew.GetBuildVersion(); print('pcbnew', v); assert v.startswith('10.0.7'), v"
# Phase 0: sources
step "IPC-D-356A parser self-check" tools/p2k/bin/p2k ipc356 --check
step "Gerber X2 export vs IPC (pads, vias, drills, outline)" tools/p2k/bin/p2k check_sources
# Phase 1: schematic
step "Part map up to date" python3 tools/make_part_map.py --check
step "Symbol library up to date" python3 tools/gen_symbols.py --check
step "Symbol pin sets vs IPC" tools/p2k/bin/p2k check_symbols
step "Sheets up to date (regenerated, byte-identical)" tools/check_sheets.sh
step "ERC" tools/erc.sh
step "Netlist comparison vs IPC" tools/p2k/bin/p2k compare_netlists
# Phase 2: footprints
step "Footprint library and map up to date" python3 tools/gen_footprints.py --check
step "Footprints vs IPC pad geometry" tools/p2k/bin/kipy -m p2k.check_footprints --pcbnew
# Phase 3: PCB
step "PCB rebuilt from schematic + gerbers, up to date" tools/make_pcb.sh --check
step "Board pads, vias vs IPC" tools/p2k/bin/kipy -m p2k.check_board
step "Board copper connectivity after zone fill" tools/p2k/bin/kipy -m p2k.assign_nets --check
step "DRC with schematic parity" tools/p2k/bin/p2k drc
# Phase 4: the finished board against the Proteus CADCAM files (independent of the generators)
step "IPC-D-356 from the board vs Proteus (pads, vias, nets)" tools/p2k/bin/p2k ipc356_diff
step "Gerber round trip vs Proteus (copper XOR, coverage, drills)" tools/p2k/bin/p2k gerber_roundtrip --check

echo
[ $fail -eq 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECKS FAILED"
exit $fail
