#!/usr/bin/env python3
"""Footprint assignment and the project footprint library of gate_drive (stdlib only).

Writes (through the shared generator tools/p2k/p2k/footprints.py)
  lib/footprint_map.csv   refdes -> footprint for all 40 parts
  lib/gate_drive.pretty/  project footprints: derived from KiCad library footprints (pads
                          renumbered to the Proteus ids, pad centres moved onto the Proteus
                          positions) or built from the IPC-D-356A pads where KiCad has nothing

Usage: python3 tools/gen_footprints.py [--check]      (needs the KiCad AppImage mount)

RULES (symbol + IPC pad pattern -> footprint) and PROJECT (project footprint specs); syntax in
tools/p2k/p2k/footprints.py. Pad numbers always equal the IPC pin ids. Pad sizes: KiCad's
(p2k_config.py FOOTPRINT_PAD_SIZES = "kicad") unless a spec says ipc_sizes.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "p2k"))  # proteus2kicad
from p2k import footprints  # noqa: E402

# Proteus pad sizes only on the parts whose KiCad pads short or come closer than 0.15 mm to the
# Proteus tracks (Phase 3 DRC with KiCad pads, STATUS.md "Phase 3"; the user decision of ac_psu and
# tube_psu): DRV1/DRV2 (5V / DRV_VCC tracks between the SOIC pad rows), J9 (tracks between the
# 1.27 mm pads; KiCad 1.0 mm pads), D2 (SOURCE_LO track at the cathode pad).
PROTEUS_PADS = frozenset("DRV1 DRV2 J9 D2".split())

RULES = [
    ("R", dict(tht=False, span=1.73, pad=(0.889, 0.889)), "Resistor_SMD:R_0603_1608Metric", "0603 (Proteus pads 1.73 mm apart)"),
    ("R", dict(tht=False, span=2.90, pad=(1.143, 1.803)), "Resistor_SMD:R_1206_3216Metric", "1206"),
    ("C", dict(tht=False, span=1.60, pad=(0.939, 0.99)), "Capacitor_SMD:C_0603_1608Metric", "0603"),
    ("C", dict(tht=False, span=3.15, pad=(1.016, 1.524)), "Capacitor_SMD:C_1206_3216Metric_Pad1.33x1.80mm_HandSolder", "1206"),
    ("D_Schottky", dict(span=2.60, refdes=PROTEUS_PADS), "gate_drive:D_SOD-323_AC_Proteus", "SOD-323 (ZLLS400TA), pads A/C, Proteus pad size"),
    ("D_Schottky", dict(span=2.60), "gate_drive:D_SOD-323_AC", "SOD-323 (ZLLS400TA), pads A/C"),
    ("D_Zener", dict(span=2.60), "gate_drive:D_SOD-323_AC", "SOD-323 (MMSZ5228BS), pads A/C"),
    ("SI8271", dict(refdes=PROTEUS_PADS), "gate_drive:SOIC-8_3.9x4.9mm_P1.27mm_Proteus", "SOIC-8, Proteus pad rows 5.5 mm apart"),
    ("IXDD609", dict(), "gate_drive:DFN-8-1EP_P0.95mm_IXDD60xD2", "IXYS D2 DFN-8 with thermal pad 9, Proteus land pattern"),
    ("HB_GT_CONNECTOR", dict(refdes=PROTEUS_PADS), "gate_drive:PinHeader_2x24_P1.27mm_Vertical_Pins15-48",
     "2x24 1.27 mm, pins 15-26/29-40/43-48 only"),
    ("PIN", dict(n=1), "gate_drive:WirePad_D1.27mm_Drill0.762mm", "toroid winding wire pad"),
]

PROJECT = {
    "D_SOD-323_AC": dict(base="Diode_SMD:D_SOD-323_HandSoldering", renumber={"1": "C", "2": "A"}, ipc="D1",
                         descr="SOD-323 diode, pads C/A, Proteus pad positions"),
    "D_SOD-323_AC_Proteus": dict(base="Diode_SMD:D_SOD-323_HandSoldering", renumber={"1": "C", "2": "A"}, ipc="D2",
                                 ipc_sizes=True, descr="SOD-323 diode, pads C/A, Proteus pads (0.508 x 0.838)"),
    "SOIC-8_3.9x4.9mm_P1.27mm_Proteus": dict(base="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", ipc="DRV1",
                                             ipc_sizes=True,
                                             descr="SOIC-8, Proteus pads (0.61 x 1.5, rows 5.5 mm apart)"),
    "DFN-8-1EP_P0.95mm_IXDD60xD2": dict(ipc="DRV3", descr="IXYS IXDD604/609 D2 package: 8 pads 0.45 x 1.2 at 0.95 mm pitch, "
                                                           "rows 4.5 mm apart, thermal pad 9 (2.6 x 3.1)"),
    "PinHeader_2x24_P1.27mm_Vertical_Pins15-48": dict(
        base="Connector_PinHeader_1.27mm:PinHeader_2x24_P1.27mm_Vertical", drop="J9", ipc="J9", ipc_sizes=True,
        descr="2x24 1.27 mm header position, only pins 15-26, 29-40, 43-48 fitted (HB GT CONNECTOR), "
              "Proteus pads (0.762 mm, drill 0.558)"),
    "WirePad_D1.27mm_Drill0.762mm": dict(ipc="J1", descr="Plated wire pad for a toroid winding lead, "
                                                         "1.27 mm pad, 0.762 mm drill (Proteus PIN)"),
}


if __name__ == "__main__":
    footprints.run(RULES, PROJECT)
