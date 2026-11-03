# fab – JLCPCB manufacturing files

| File | |
|---|---|
| `jlc_bom.csv` | Assembly BOM in JLC's format (Comment, Designator, Footprint, JLCPCB Part #): 11 lines, 30 SMD parts on the top side |
| `jlc_cpl.csv` | Assembly CPL (Designator, Mid X, Mid Y, Layer, Rotation) for exactly those parts, made by `make_fab.sh` |
| `hand_fit.csv` | Not JLC-assembled: the toroid (wound by the user), DRV3 IXDD609D2TR (not stocked), J9 (header with 4 pins to clip) |
| `make_fab.sh` | Gerbers + Excellon drills → `out/gate_drive_gerber.zip`, position file → `jlc_cpl.csv`, BOM copy (`out/` is not committed) |
| `make_cpl.py`, `jlc_bom_check.py` | From ac_psu `fab/`: CPL with per-package rotation corrections (SOIC 270, SOD-323 180); stock check of every code: `python3 fab/jlc_bom_check.py 5` |
| `jlc_search.py` | Keyword search of the JLC library (used to pick the codes) |
| `jlc_stock_2026-11-03.json` | Stock check for 5 boards (after the D6/D7 change): every BOM line in stock; IXDD609D2TR 0 |

Order flow: `fab/make_fab.sh`, upload `fab/out/gate_drive_gerber.zip` (2 layers, 1.6 mm), then
`fab/jlc_bom.csv` and `fab/jlc_cpl.csv`. **Check every rotation in JLC's placement preview.**
JLC 2-layer capabilities (checked 2026-11-03: 0.10/0.10 mm track/space, via 0.15/0.25 mm): the
board's 0.1016 mm tracks, 0.1524 mm gaps and 0.254/0.381 mm vias are within them.

Part choices (open points in STATUS.md "Open questions"):

| Ref | Design | BOM | Note |
|---|---|---|---|
| DRV1, DRV2 | SI8271 (no suffix in Proteus) | **SI8271DB-ISR (C461855)** | User 2026-11-03. Output UVLO letter D (A 5 V, B 8 V, D 12 V, G 3 V per the ordering-guide rows seen; check the datasheet table): VDD2–GND2 is 17.5–20.5 V with the user's rails. |
| D6, D7 | MMSZ5228BS-7-F (3.9 V) | **MMSZ5246BS-7-F 16 V (C151819)** | Positive-rail clamps (VCC–SOURCE). User 2026-11-03: rails +14.5…16 V / −3…−4.5 V, so the 3.9 V part was wrong here; 16 V (15.2–16.8 V) stays off inside the range (a 15 V part, 14.25–15.75 V, would conduct). The schematic still shows the Proteus value (STATUS.md finding 1). |
| D5, D8 | MMSZ5228BS-7-F (3.9 V) | C2895358, as designed | Negative-rail clamps, 3.71–4.1 V: inside −3…−4.5 V. |
| C1–C4 | 4.7u (0603) | 25 V X5R (C5360844) | C1/C4 carry the positive rail; at 15 V DC bias an 0603 X5R keeps roughly 1 µF. |
| C7, C8 | 4.7u / 100n (1206) | 50 V X7R basic parts | 15 V rail |
| R2/R5, R4/R12 | 3R / 22R 1206 | C17939 / C17958 | |
| DRV3 | IXDD609D2TR | hand-fit (`hand_fit.csv`) | JLC: 0 stock; Mouser/Digikey, hand-solder or consign. No footprint-compatible part at JLC (2026-11-03). In stock, same pin numbering but SOIC-8 (board change): IXDN609SIATR (C5242049, 2194; pin 3 NC – EN is tied to VCC here anyway) and IXDD609SIATR (C2677099, 50; with EN). With the 15–17 V rail on J9-47 (user, 2026-11-03; the baseboard net is named 20V) the 18 V parts also qualify, with 1 V margin: MIC4452YM-TR (C435908, 2702, 12 A, SOIC-8). The IXYS parts (35 V) keep the larger margin. |
| J9 | HB GT connector | 2×17 1.27 mm male THT header C27985217, hand-fit | clip pins 27/28 and 41/42 (no holes) |
