#!/usr/bin/env python3
"""Generate lib/gate_drive.kicad_sym, the project symbol library (helpers: p2k.symgen).

Pin numbers equal the Proteus/IPC pin ids; box symbols carry the Proteus pin names from the
PDF. Simple symbols are copied from the KiCad 10 standard library (flattened, pins renumbered).
Power symbols carry the IPC net names of the rails drawn as Proteus power terminals.

Run:  tools/gen_symbols.py           (needs the AppImage mount for the std libs)
      tools/gen_symbols.py --check   (fail if lib/gate_drive.kicad_sym is not up to date)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "p2k"))  # proteus2kicad
from p2k.symgen import *  # noqa: E402,F401,F403
from p2k.symgen import run  # noqa: E402

GROUNDS = ["GND"]
SUPPLIES = ["5V", "15V"]


def build():
    D_PINS = {"1": "C", "2": "A"}
    syms = [
        from_std("Device", "R", "R", "R", "R"),
        from_std("Device", "C", "C", "C", "C"),
        from_std("Device", "D_Schottky", "D_Schottky", "D", desc="Schottky diode, pins A/C", pins=D_PINS),
        from_std("Device", "D_Zener", "D_Zener", "D", desc="Zener diode, pins A/C", pins=D_PINS),
        from_std("Connector", "TestPoint", "PIN", "J", "PIN",
                 desc="Proteus PIN terminal: one plated pad for a transformer winding wire"),
        box("SI8271", "DRV", [(2, "VDD1", PI), (1, "Vin", IN), (4, "EN", IN), (3, "GND1", PI)],
            [(8, "VDD2", PI), (7, "OUT+", OUT), (6, "OUT-", OUT), (5, "GND2", PI)],
            desc="Isolated single gate driver SOIC-8"),
        # OUTA and OUTB are one output on two pins (tied together): OUTB is passive so that ERC
        # does not report Output-Output (as on tube_psu).
        box("IXDD609", "DRV", [(1, "VCC", PI), (8, "VCC", PI), (2, "IN", IN), (3, "EN", IN)],
            [(7, "OUTA", OUT), (6, "OUTB", PAS), (4, "GND", PI), (5, "GND", PI), (9, "TAB", PAS)],
            desc="9 A gate driver DFN-8 with thermal pad"),
    ]
    l, r = header([*range(15, 27), *range(29, 41), *range(43, 49)])
    syms.append(box("HB_GT_CONNECTOR", "J", l, r, show_pin_names=False,
                    desc="Half-bridge gate-driver connector 2x24 1.27 mm, pins 15..48 without 27,28,41,42 "
                         "(as on the PCB; mates face to face with the ac_psu baseboard J1-J4/J6/J8)"))
    syms.append(rename(std_symbol("power", "PWR_FLAG"), "PWR_FLAG"))
    syms += [power(n, True) for n in GROUNDS] + [power(n, False) for n in SUPPLIES]
    return syms


if __name__ == "__main__":
    sys.exit(run(build))
