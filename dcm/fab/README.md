# dcm/fab – JLCPCB manufacturing files of the DCM board

Same layout and scripts as the root `fab/` (see `../../fab/README.md` for the order flow,
rotation corrections and JLC capability check); run inside `dcm/`.

| File | |
|---|---|
| `jlc_bom.csv` | 12 lines, 34 SMD parts on the top side |
| `jlc_cpl.csv` | CPL for exactly those parts (`make_fab.sh`; SOT-23 +180, SOIC +270, SOD-323 +180) |
| `hand_fit.csv` | The toroid (wound by the user) and J9 (2×17 1.27 mm male header, clip pins 27/28/41/42) |
| `jlc_stock_2026-11-03.json` | Stock check for 5 boards: every line in stock except ZLLS400TA (2) |

Part choices beyond the root board's:

| Ref | Design | BOM | Note |
|---|---|---|---|
| Q1 | MMBT3904 | C20526 (basic) | SOT-23, 1=B 2=E 3=C |
| R13 | 2.2k 0603 | C4190 (basic) | |
| R7, R14 | 10k 0603 | C25804 | R7 value: see `../README.md` finding 1 |
| C9 | 100n 0603 | C14663 | |
| D1–D4, D9 | ZLLS400TA | C460267 | **2 in stock on 2026-11-03** (open question; in stock: ZLLS400QTA C151560, 36 pcs, automotive grade of the same part) |
| D6, D7 | MMSZ5228BS-7-F | MMSZ5246BS-7-F 16 V (C151819) | user decision of the root board (same rails) |
| DRV1, DRV2 | SI8271 | SI8271DB-ISR (C461855) | user decision of the root board |
