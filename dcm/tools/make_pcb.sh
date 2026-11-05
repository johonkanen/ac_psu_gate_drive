#!/usr/bin/env bash
# Phase 3: rebuild kicad/gate_drive.kicad_pcb from the schematic and the Proteus gerbers
# (shared tools in tools/p2k, board values in p2k_config.py). Re-runnable; two runs give a
# byte-identical board (UUIDs seeded per step).
#   1 build_pcb         footprints with nets at the Proteus positions, outline
#   2 gerber_to_tracks  copper gerbers -> tracks and vias, pour outlines on User.1-4
#   3 assign_nets       nets of tracks/vias/pours by copper connectivity -> reports/pour_nets.json
#   4 pours_to_zones    pours -> filled zones
#   5 place_refdes      references clear of pads / silk / edge (else smaller, else Fab only; Phase 5)
# Board-only footprints (none on this board) and the footprint fit come from tools/gen_footprints.py
# and p2k.check_footprints (reports/footprint_fit.csv) - run those first after footprint changes.
#
#   tools/make_pcb.sh           rebuild the board in place
#   tools/make_pcb.sh --check   rebuild into a temporary directory and fail unless the board and
#                               reports/pour_nets.json equal the committed ones byte for byte
set -eu
cd "$(dirname "$0")/.."
K=tools/p2k/bin/kipy
run() {
    $K -m p2k.build_pcb
    $K -m p2k.gerber_to_tracks
    $K -m p2k.assign_nets
    $K -m p2k.pours_to_zones
    $K -m p2k.place_refdes
}
if [ "${1:-}" = "--check" ]; then
    tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
    mkdir -p "$tmp/reports"
    cp reports/footprint_fit.csv "$tmp/reports/"
    cp kicad/gate_drive.kicad_pro "$tmp/"   # pcbnew loads the project next to the board (affects the UUID sequence)
    export P2K_PCB="$tmp/gate_drive.kicad_pcb" P2K_REPORTS="$tmp/reports"
    run >"$tmp/log" 2>&1 || { cat "$tmp/log"; echo "make_pcb: FAILED"; exit 1; }
    ok=1
    cmp -s "$P2K_PCB" kicad/gate_drive.kicad_pcb || { echo "make_pcb: kicad/gate_drive.kicad_pcb is not up to date (run tools/make_pcb.sh)"; ok=0; }
    cmp -s "$tmp/reports/pour_nets.json" reports/pour_nets.json || { echo "make_pcb: reports/pour_nets.json is not up to date"; ok=0; }
    grep -E "^(build_pcb|gerber_to_tracks: [0-9]|assign_nets: stage|pours_to_zones|place_refdes)" "$tmp/log" | sed "/^build_pcb/s/ -> .*//"
    [ $ok -eq 1 ] && echo "make_pcb: board rebuilt from scratch, byte-identical" || exit 1
else
    run
fi
