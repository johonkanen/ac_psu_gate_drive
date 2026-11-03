# fab – JLCPCB manufacturing files

| File | |
|---|---|
| `jlc_bom.csv` | Assembly BOM in JLC's format (Comment, Designator, Footprint, JLCPCB Part #): 10 lines, 30 SMD parts on the top side |
| `jlc_cpl.csv` | Assembly CPL (Designator, Mid X, Mid Y, Layer, Rotation) for exactly those parts, made by `make_fab.sh` |
| `hand_fit.csv` | Not JLC-assembled: the toroid (wound by the user), DRV3 IXDD609D2TR (not stocked), J9 (header with 4 pins to clip) |
| `make_fab.sh` | Gerbers + Excellon drills → `out/gate_drive_gerber.zip`, position file → `jlc_cpl.csv`, BOM copy (`out/` is not committed) |
| `make_cpl.py`, `jlc_bom_check.py` | From ac_psu `fab/`: CPL with per-package rotation corrections (SOIC 270, SOD-323 180); stock check of every code: `python3 fab/jlc_bom_check.py 5` |
| `jlc_search.py` | Keyword search of the JLC library (used to pick the codes) |
| `jlc_stock_2026-11-03.json` | Stock check for 5 boards: every BOM line in stock; IXDD609D2TR 0 |

Order flow: `fab/make_fab.sh`, upload `fab/out/gate_drive_gerber.zip` (2 layers, 1.6 mm), then
`fab/jlc_bom.csv` and `fab/jlc_cpl.csv`. **Check every rotation in JLC's placement preview.**
JLC 2-layer capabilities (checked 2026-11-03: 0.10/0.10 mm track/space, via 0.15/0.25 mm): the
board's 0.1016 mm tracks, 0.1524 mm gaps and 0.254/0.381 mm vias are within them.

Part choices (open points in STATUS.md "Open questions"):

| Ref | Design | BOM | Note |
|---|---|---|---|
| DRV1, DRV2 | SI8271 (no suffix in Proteus) | SI8271AB-ISR (C17275034, 5 V output UVLO) | **provisional**: the variant letter sets the output UVLO (A 5 V, B 8 V, D 12 V, G 3 V); pick it for the real VDD2–GND2 rail (see the D6/D7 question). DB-ISR (C461855) has the most stock. |
| D5–D8 | MMSZ5228BS-7-F (3.9 V) | C2895358, as designed | **D6/D7 clamp VCC–SOURCE at 3.9 V** – confirm the fitted part (STATUS.md finding 1). |
| C1–C4 | 4.7u (0603) | 25 V X5R (C5360844) | C1/C4 carry the positive rail; at 15 V DC bias an 0603 X5R keeps roughly 1 µF. |
| C7, C8 | 4.7u / 100n (1206) | 50 V X7R basic parts | 15 V rail |
| R2/R5, R4/R12 | 3R / 22R 1206 | C17939 / C17958 | |
| DRV3 | IXDD609D2TR | hand-fit (`hand_fit.csv`) | JLC: 0 stock; Mouser/Digikey, hand-solder or consign |
| J9 | HB GT connector | 2×17 1.27 mm male THT header C27985217, hand-fit | clip pins 27/28 and 41/42 (no holes) |
