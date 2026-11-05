# dcm – DCM variant of the gate-driver board

KiCad 10.0.7 conversion of the Proteus board `gate_drive_power_dcm_fb_v3_ee10` (2021-03-22). It is
the asym board of the repository root with the toroid primary driver replaced: instead of the
IXDD609 (DRV3) driving the primary through C12, a single NPN Q1 (MMBT3904) switches the primary
from 15V (J1 = 15V, J2 = collector), with the leakage/flyback energy clamped by R7 – D9 into
C9 ‖ R14 back to 15V. Same outline (22.4 × 34.9 mm), same J9 pinout, same gate drivers and rectifiers.

Converted 2026-11-03 (user: "convert the dcm version too"), same method and tools as the root board
(proteus2kicad playbook phases 0–4, submodule `../tools/p2k` through the symlink `tools/p2k`).
This folder is self-contained: its own `p2k_config.py`, so every tool run inside `dcm/` works on
this board. `tools/check_all.sh` must end with `ALL CHECKS PASSED`.

## Sources (`source/`)

`/mnt/c/Users/jaarh/Sync/proteus_projektit/Projects/gate_drive_power_asym_fb/V3_ee10/dcm/`: the
`.pdsprj` (Proteus 8.12 SP0) and the CADCAM zip (unpacked to `source/cadcam/`; identical copies in
`Sync_backup` and `D:\Sync_vamuuskopio`). **No PDF print exists** for this project.

IPC-D-356A: 135 records, 26 nets, 43 parts, 16 vias 0.381/0.254, no N/C, no holes.
Against the asym board: removed DRV3, C7 (4.7u 1206), C12 (100n); added Q1 MMBT3904, R7 10k,
R13 2.2k, R14 10k, C9 100n, D9 ZLLS400TA (values from ROOT.DSN); R11 is now the base resistor
(was the PWM_TRANS pull-down; R13 is that now). C8, R9, R11 and D6 moved; the copper around the primary switch and 5 vias differ.

## How it differs from the root conversion

- **Pages without a PDF:** `tools/make_part_map.py` puts the parts of the asym PDF page 1 on sheet 1
  (identical parts and nets; `sheet01.py` is the root script) and all others on sheet 2. The Q1
  primary-switch block on sheet 2 is drawn from the IPC netlist, not from a Proteus drawing.
- Symbols: `Q_NPN` (KiCad Device:Q_NPN, pins 1=B 2=E 3=C) instead of IXDD609.
- Footprints: `gate_drive:SOT-23_Proteus` – KiCad SOT-23 with the pad centres on the Proteus land
  pattern (rows 2.3 mm apart; KiCad's own SOT-23 is off by 0.28 mm); no DFN-8.
- DRC: 14 accepted courtyard overlaps (root: 15) and one extra warning `track_dangling` – a 6.5 µm
  15V stub that is in the Proteus bottom-copper gerber itself (line 86), kept as drawn.

## Findings (reported, not changed)

1. **R7 = 10k in the clamp path.** Q1 collector → R7 10k → D9 → C9 ‖ R14 → 15V. With 10k in series
   the clamp takes only milliamps, so at turn-off the leakage-inductance energy is hardly clamped and
   the collector can ring well above the MMBT3904's 40 V V_CEO. A clamp resistor is usually a few
   ohms to tens of ohms; R14 10k across C9 is the usual bleed. Check the value fitted on the built
   boards (10R vs 10k?).
2. **Base drive / available power.** Base current from PWM_TRANS through R11 10k is about 0.26 mA at
   3.3 V (0.43 mA at 5 V); with h_FE ≈ 100 the collector current saturates at roughly 25–40 mA, far
   below the 200 mA rating. That caps the primary peak current and so the gate-supply power
   (two Si8271 outputs). R13 2.2k loads PWM_TRANS only (it is on the source side of R11).
3. **Toroid windings unknown for DCM.** Sheet 2's note gives the asym drawing's windings; the
   DCM project has no drawing/PDF, and a DCM flyback normally uses a different turns ratio and
   winding polarity. Note what is actually wound.
4. Root findings 3 (baseboard pins 25/39), 4 (J9 drill) and 5 (0603 4.7 µF DC bias) apply as well.

## JLC (`fab/`)

As the root board (`fab/README.md`). The root's user BOM decisions are applied: SI8271DB-ISR,
D6/D7 MMSZ5246BS-7-F 16 V (rails +14.5…16 / −3…−4.5 V). New: Q1 C20526, R13 C4190 (both basic).
**ZLLS400TA (C460267) has 2 in stock (2026-11-03 afternoon; 2012 in the morning)** – short for both
boards (DCM needs 5 per board, asym 4). Not changed (open question).

## Last verification (`tools/check_all.sh`, 2026-11-03)

```
erc: 0 errors, 2 warnings (reports/erc.rpt)
compare: parts 43/43 present, 0 missing, 0 extra; pins compared 119, wrong-net pins 0; IPC nets touched 26, complete 26
check_footprints: 43/43 parts fitted, 119 pads, 10 footprints, worst residual 0.039 mm (limit 0.05)
make_pcb: board rebuilt from scratch, byte-identical
check_board: 455 tracks, 16 vias, 8 zones
assign_nets: after zone fill: 26 groups, 0 shorts, 0 orphans, 0 opens, 0 items with a foreign net
drc: 22 violations, 0 shorts, 0 unconnected, 0 parity issues (14 courtyards_overlap accepted, 7 silk, 1 track_dangling)
ipc356_diff: matched 135 (119 pads incl. 0 N/C, 16 vias, 0 holes), 26 Proteus nets mapped 1:1, 0 mismatches
roundtrip: F.Cu only pad-shape clusters (69), B.Cu XOR 0.00 mm^2, drills 0 mismatches
ALL CHECKS PASSED
```
