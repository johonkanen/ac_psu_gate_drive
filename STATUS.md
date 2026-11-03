# Status

Updated: 2026-11-03 (Phases 0–4 and the JLC files done in one session, Opus 5.5; ALL CHECKS PASSED)

Repository: https://github.com/johonkanen/ac_psu_gate_drive (local ~/dev/ac_psu_gate_drive).

## Decisions (user, 2026-11-03)

- Convert the asymmetric board `V3_ee10` only (not the DCM variant).
- J9 is a **male** header (the ac_psu baseboard has the female sockets).
- JLC parts list for every part except the hand-wound toroid.
- Proteus pad sizes where KiCad pads collide with Proteus copper: carried over from the ac_psu /
  tube_psu decision (DRV1, DRV2, J9, D2; `tools/gen_footprints.py` PROTEUS_PADS). Say if you
  want something else.

## Phase 0 – sources, config, IPC

`source/` = copies of the .pdsprj, the PDF (renders + text) and the CADCAM zip (unpacked to
`source/cadcam/`). `p2k_config.py`: 24 nets, 136 records, 40 parts, 17 vias 0.381/0.254,
2 copper layers, outline 22.4 × 34.9 mm. `p2k ipc356` → `reference/` (cheat sheets),
`p2k check_sources`: every X2 flash/drill matches an IPC record. No tool changes in
proteus2kicad were needed (submodule at c5682dd, the same as tube_psu).

## Phase 1 – schematic

- `tools/make_part_map.py` → `lib/part_map.csv` (values from ROOT.DSN, page from the PDF text,
  package from the IPC pad pattern – the ROOT.LYT records of this older save do not parse).
- `tools/gen_symbols.py` → `lib/gate_drive.kicad_sym`: R, C, D_Schottky, D_Zener (pins A/C),
  PIN (one pad), SI8271, IXDD609 (as tube_psu), HB_GT_CONNECTOR (pins 15–26, 29–40, 43–48, as
  ac_psu), power GND / 5V / 15V, PWR_FLAG.
- Transcription rules: power nets GND, 5V, 15V as power symbols; the other named nets as global
  labels in IPC spelling (PDF lower-case labels pwm_hi, drv1_vcc, Gate_HI … = IPC upper case);
  D1+/D1−/D2+/D2− local labels; auto-named nets (#00038 … #00046: DRV3 out → J1, J2 → C12,
  J3/J4/J6/J7 → rectifiers) plain wires. PWR_FLAGs on 5V/15V/GND (from J9) and on the four
  floating rails DRV1/2_VCC, DRV1/2_RET (fed by diodes only).
- The toroid has no part in Proteus (a drawing on page 2) → no symbol; a text note on sheet 2
  lists the windings.
- ERC: 0 errors, 2 warnings `ground_pin_not_ground` (Si8271 GND2 on the floating DRV1/2_RET
  rails – by design).

## Phase 2 – footprints

`tools/gen_footprints.py` → `lib/footprint_map.csv`, `lib/gate_drive.pretty` (6 project
footprints: SOD-323 A/C (KiCad pads / Proteus pads), SOIC-8 with the Proteus 5.5 mm rows and
pads, IXYS D2 DFN-8 from the IPC pads, the partial 2×24 1.27 mm header (Proteus pads 0.762 /
drill 0.558), the toroid wire pad 1.27 / 0.762). Every part fits its IPC pads within 0.039 mm.

## Phase 3 – PCB

`tools/make_pcb.sh` (build_pcb, gerber_to_tracks, assign_nets, pours_to_zones, place_refdes):
452 tracks, 17 vias, 8 zones; 0 shorts / 0 orphans / 0 opens after zone fill; reproducible
byte for byte (`--check`). Design rules (`p2k_config.py` PCB_RULES) from `tools/measure_gaps.py`:
smallest different-net gap 0.1524 mm, copper to edge 0.354 mm, drill to drill 0.711 mm,
thinnest track 0.1016 mm. First DRC with KiCad pads: 5 shorts / 6 clearance / 9 mask bridges
at DRV1, DRV2 (5V and DRV_VCC tracks between the SOIC rows), J9 (tracks between the 1.27 mm
pads) and D2 → Proteus pads on those four. DRC now: 0 shorts, 0 unconnected, 0 parity;
15 courtyards_overlap (accepted, dense Proteus placement), 7 silk warnings.

## Phase 4 – verification

`p2k ipc356_diff`: 136/136 records, 24 nets 1:1, 0 mismatches. `p2k gerber_roundtrip --check`:
only pad-shape clusters (52, KiCad vs Proteus pad shapes), 0 uncovered draws/flashes, 0 drill
mismatches. Negative test: a via moved 0.2 mm fails ipc356_diff, gerber_roundtrip and
check_board. Same-session verification (the playbook suggests a fresh session for Phase 4;
optional here – the checks are the shared, already-reviewed tools).

## JLC (fab/)

`fab/README.md`: BOM 10 lines / 30 top-side SMD parts, CPL, hand-fit list (toroid, DRV3, J9),
stock check for 5 boards: every BOM line in stock. IXDD609D2TR: 0 at JLC (only SOIC/DIP/TO
versions stocked). J9: 2×17 1.27 mm male THT header C27985217 with pins 27/28/41/42 clipped.
The board is within JLC's 2-layer limits (0.10 mm track/space, 0.15/0.25 mm via).

## Findings (reported, not changed – principle 7)

1. **Resolved in the BOM (user, 2026-11-03: rails +14.5…16 V and −3…−4.5 V):** D6 / D7 → MMSZ5246BS-7-F 16 V
   in `fab/jlc_bom.csv`; the schematic keeps the Proteus value (changing it is the first deviation from
   Proteus – do it together with the finding-9 noise changes and a deviation list). Original finding:
   **D6 / D7 (MMSZ5228BS-7-F, 3.9 V zener) sit across DRV2_VCC–SOURCE_LO / DRV1_VCC–SOURCE_HI**
   (cathode on VCC). As drawn they clamp the positive gate rail to about 3.9 V; D5 / D8 (same
   part) clamp the negative rail to −3.9 V, which fits an asymmetric supply. From the turns ratio
   (8t primary driven ±7.5 V through C12; the positive diode on a 16t or 12t tap) the positive
   rail would otherwise be about 11–15 V. Confirm the zener actually fitted on D6/D7 (or that the
   +3.9 V rail is intended, e.g. a GaN gate) – it also decides the Si8271 UVLO variant.
2. **Toroid drawing vs netlist:** the drawing on page 2 puts J4 / J7 between the 12t and 4t
   windings and J5 / J8 at the 4t end; the netlist has J5 / J8 on SOURCE_HI / SOURCE_LO and J4 /
   J7 on the negative-rail diodes D4 / D2. Electrically consistent (VCC from 16t, RET from 4t);
   noted because the winding description depends on it.
3. **Mating with the baseboard (ac_psu sheet02.py):** face to face, J9-26 (DRV1_VCC) meets
   baseboard pin 25 and J9-40 (DRV2_VCC) meets baseboard pin 39. Those baseboard pins are N/C on
   most sockets but carry SDM_RAW_VOLTAGE (J2-39), ISO_AFE_SDM_RAW_VOLTAGE (J8-39) and
   ISO_DAB_SDM_RAW_VOLTAGE (J4-25): a gate-driver board in J2/J8/J4 puts its floating gate
   supply on those signals. Check whether that is intended (maybe a different board goes there).
   The other pins mate as expected (43/44, 45/46, 47/48 swap; J9-47 "15V" = baseboard 20V).
4. J9 drill 0.558 mm (Proteus) for 0.4 mm square header pins (diagonal 0.57 mm) is tight; KiCad's
   library drill is 0.65 but its 1.0 mm pads collide with the Proteus tracks. Kept as Proteus.
5. C1–C4 are 0603 4.7 µF: at ~15 V DC bias an X5R 25 V 0603 keeps roughly 1 µF.

## Open questions for the user

- DRV3 IXDD609D2TR: buy from a distributor (hand-solder or consign), or change the board to the SOIC-8
  IXDN609SIATR / IXDD609SIATR stocked at JLC (same pin numbering; fab/README.md). Si8271: SI8271DB-ISR
  (user, 2026-11-03).
- Finding 3 (baseboard pins 25/39).

## Last verification (`tools/check_all.sh`)

```
== KiCad environment
pcbnew 10.0.7
== IPC-D-356A parser self-check
ipc356: nets=24, records=136, refdes_raw=41, tht_records=55, smd_records=81, smd_top=81, smd_bottom=0, nc_pads=0, vias=17, free_pads=0, holes=0, parts=40
ipc356: OK
== Gerber X2 export vs IPC (pads, vias, drills, outline)
check_sources: OK
== Part map up to date
make_part_map: lib/part_map.csv up to date (40 parts)
== Symbol library up to date
gen_symbols: lib/gate_drive.kicad_sym up to date (12 symbols)
== Symbol pin sets vs IPC
symbols: 8 part types, 40 refdes, 3 power symbols
symbols: OK
== Sheets up to date (regenerated, byte-identical)
check_sheets: 2 sheets regenerated, identical
== ERC
erc: 0 errors, 2 warnings (reports/erc.rpt)
== Netlist comparison vs IPC
compare: parts 40/40 present, 0 missing, 0 extra; pins compared 119, wrong-net pins 0; IPC nets touched 24, complete 24
compare: per sheet (drawn/total) 1:13/13 2:27/27
compare: OK
== Footprint library and map up to date
gen_footprints: 40 parts, 10 footprints (6 project), up to date
== Footprints vs IPC pad geometry
check_footprints: pcbnew placement of 40 parts, worst pad offset 0.039 mm
check_footprints: 40/40 parts fitted, 119 pads, 10 footprints, worst residual 0.039 mm (limit 0.05)
check_footprints: OK
== PCB rebuilt from schematic + gerbers, up to date
build_pcb: 40 footprints placed (0 excluded from board), 0 mounting holes, 24 nets, 4 outline segments
gerber_to_tracks: 452 tracks, 17 vias (IPC 17), 8 pour outlines on User.1-4
assign_nets: stage A (no pours): 34 groups, 0 shorts, 0 orphans, 5 opens
assign_nets: stage B (with pours): 24 groups, 0 shorts, 0 orphans, 0 opens
pours_to_zones: 8 pours -> 8 zones; 16 holes closed by the stroke, 22 holes kept
place_refdes: 1 Fab only, 6 kept, 28 moved, 5 moved, 0.8 mm text (sizes 1.0, 0.8 mm)
make_pcb: board rebuilt from scratch, byte-identical
== Board pads, vias vs IPC
check_board: 40 footprints, 119 pads, worst pad offset 0.039 mm (limit 0.05), 24 IPC nets mapped 1:1, 0 mounting holes
check_board: 452 tracks, 17 vias, 8 zones
check_board: OK
== Board copper connectivity after zone fill
assign_nets: after zone fill: 24 groups, 0 shorts, 0 orphans, 0 opens, 0 items with a foreign net
assign_nets: OK (report reports/assign_nets.txt)
== DRC with schematic parity
drc: 22 violations, 0 shorts, 0 unconnected, 0 parity issues (reports/drc.json)
drc:     15 error    courtyards_overlap  accepted: KiCad courtyards vs the dense Proteus placement (15 pairs)
drc:      3 warning  silk_overlap
drc:      2 warning  silk_edge_clearance
drc:      2 warning  silk_over_copper
drc: OK
== IPC-D-356 from the board vs Proteus (pads, vias, nets)
ipc356_diff: Proteus 136 records, KiCad 136; matched 136 (119 pads incl. 0 N/C, 17 vias, 0 holes), worst position offset 0.040 mm (limit 0.05)
ipc356_diff: 24 Proteus nets mapped 1:1 onto KiCad nets, 0 mismatches
ipc356_diff: pads with another size in KiCad (info): C 18, D 14, R 22
ipc356_diff: OK
== Gerber round trip vs Proteus (copper XOR, coverage, drills)
roundtrip: F.Cu   XOR   12.92 mm^2, beyond 0.05 mm: only Proteus   0.88, only KiCad   6.70 mm^2; clusters >= 0.01 mm^2: 52 pad shape; draws/flashes off the other copper: 0 Proteus, 0 KiCad
roundtrip: B.Cu   XOR    0.00 mm^2, beyond 0.05 mm: only Proteus   0.00, only KiCad   0.00 mm^2; clusters >= 0.01 mm^2: none; draws/flashes off the other copper: 0 Proteus, 0 KiCad
roundtrip: drills 0 mismatches; report reports/roundtrip/roundtrip.txt, overlays reports/roundtrip/*.png
roundtrip: OK

ALL CHECKS PASSED
```
