#!/usr/bin/env bash
# JLCPCB fabrication + assembly outputs from kicad/gate_drive.kicad_pcb:
#   fab/out/gerber/        gerbers (2 copper layers, mask, paste, silk, outline) + Excellon drills
#   fab/out/gate_drive_gerber.zip   the upload for the PCB order
#   fab/out/jlc_bom.csv    copy of fab/jlc_bom.csv (assembly BOM)
#   fab/jlc_cpl.csv        assembly CPL (committed, regenerated here)
# fab/out/ is not committed (.gitignore). Not JLC-assembled: fab/hand_fit.csv.
set -eu
cd "$(dirname "$0")/.."
CLI=tools/p2k/bin/kicad-cli
PCB=kicad/gate_drive.kicad_pcb
OUT=fab/out
rm -rf "$OUT"; mkdir -p "$OUT/gerber"
$CLI pcb export gerbers --layers F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.SilkS,B.SilkS,Edge.Cuts \
    --subtract-soldermask -o "$OUT/gerber/" "$PCB" >/dev/null
$CLI pcb export drill --format excellon --drill-origin absolute --excellon-units mm \
    --excellon-separate-th -o "$OUT/gerber/" "$PCB" >/dev/null
(cd "$OUT/gerber" && zip -q -r ../gate_drive_gerber.zip .)
$CLI pcb export pos --side both --format csv --units mm -o "$OUT/pos.csv" "$PCB" >/dev/null
python3 fab/make_cpl.py "$OUT/pos.csv" fab/jlc_cpl.csv
cp fab/jlc_bom.csv "$OUT/jlc_bom.csv"
echo "make_fab: $(ls "$OUT/gerber" | wc -l) gerber/drill files -> $OUT/gate_drive_gerber.zip; BOM + CPL in $OUT and fab/"
