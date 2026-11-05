# Proteus → KiCad migration plan: gate_drive_power_asym_fb_v3_ee10

Goal: redraw the Proteus schematic of the half-bridge gate-driver board in KiCad 10.0.7, rebuild
the PCB from the Proteus gerbers so that every pad, track, via and pour carries the net of the
redrawn schematic, prove both identical to the Proteus design with scripted checks, and make a
JLCPCB parts list (BOM + CPL) for everything except the hand-wound gate-supply toroid.

Method: the proteus2kicad playbook `tools/p2k/CONVERSION_PLAYBOOK.md` (phases 0–4), with the
shared tools of the submodule `tools/p2k` and the board values in `p2k_config.py`, as in
`~/dev/ac_psu_kicad` and `~/dev/tube_psu_kicad`. Only what is specific to this board is here.

Scope (user, 2026-11-03): the asymmetric-supply board (`V3_ee10`). Later the same day (user): the
DCM variant (`V3_ee10/dcm/gate_drive_power_dcm_fb_v3_ee10`) too, in `dcm/` (`dcm/README.md`). J9 is a male header. Later,
not in this conversion: the noise fixes of ac_psu `reports/noise/README.md` finding 9.

## 1. Inventory (checked 2026-11-03)

Source folder `C:\Users\jaarh\Sync\proteus_projektit\Projects\gate_drive_power_asym_fb\V3_ee10\`
(`/mnt/c/...`), copies in `source/`:

| Item | Notes |
|---|---|
| `source/gate_drive_power_asym_fb_v3_ee10.pdsprj` | Proteus 8.12 SP0, saved 2021-03-22. `p2k.pdsprj.dsn_values` reads the 40 schematic values; the ROOT.LYT layout records are not in the format `lyt_parts` reads (packages taken from the IPC pad patterns instead). Stale layout value seen: C1 "4.7uH". |
| `source/schematic_pdf/gate_drive_power_asym_fb_v3_ee10.PDF` | 2 pages, printed 2026-11-02. Page 1 gate drivers DRV1/DRV2 (Si8271) + J9; page 2 the two floating supplies, DRV3 (IXDD609) and the toroid drawing (graphic only, no part). Renders `hi-1.png`, `hi-2.png`, text `schematic_text.txt`. |
| `source/gate_drive_power_asym_fb_v3_ee10 - CADCAM.ZIP` → `source/cadcam/` | 2021-03-22, Gerber X2 (`%TA.AperFunction` on every aperture, one `TF.SameCoordinates`), metric `FSLAX45Y45`, 2 copper layers, top silk / resist / paste / assembly, bottom resist, Mechanical 1 outline, drill as gerber `Drill TOP-BOT Plated` (no Excellon, no non-plated holes), IPC-D-356A netlist, READ-ME (stack 0.036 Cu / 1.483 FR4 / 0.036 Cu). |

Board: outline 22.4 × 34.9 mm at (−23.254, 6.1) mm; no arcs; Top Copper 46 G36 pour regions
(8 pours with 38 clear holes), Bottom Copper tracks only; all parts on top.

IPC-D-356A: 136 records (55 THT, 81 SMD all top), 24 nets (6 auto-named `#000xx`), 40 parts,
17 vias 0.381/0.254 mm (blank refdes), no N/C pads, no holes, no free pads, no truncated
refdes, no `=POWER` aliases. J9 has pins 15–26, 29–40, 43–48 only (a 2×24 1.27 mm position,
the same partial footprint as the ac_psu baseboard J1–J4/J6/J8). J1–J8 are single wire pads
(1.27 mm, drill 0.762) for the toroid leads.

## 2. Phases

As the playbook. Sheets: page 1 → `01_gate_drivers.kicad_sch`, page 2 → `02_gate_supply.kicad_sch`
(scripts `tools/sheets/sheet01.py`, `sheet02.py`). The toroid has no symbol (a text note on
sheet 2 documents the windings). Phase 5 (clean-up) only on user request. JLC files in `fab/`
(pattern of ac_psu `fab/`).

## 3. Risks (as found)

- KiCad pads larger than the Proteus pads on the dense SOIC / 1.27 mm header → Proteus pad sizes
  on the conflicting parts (done: DRV1, DRV2, J9, D2).
- IXDD609D2TR (DFN-8) not stocked at JLC → hand-fit or consign.
