"""proteus2kicad configuration of the gate_drive_power_asym_fb_v3_ee10 board (tools in tools/p2k,
see its README).

Plain Python; every value here is specific to this board. Coordinates in mm, IPC frame (Y up).
"""

PROJECT = "gate_drive"  # KiCad project / library name

# --- Footprints (gen_footprints) -----------------------------------------------------

# "kicad" = KiCad library pad sizes and drills (pad centres on the Proteus positions).
FOOTPRINT_PAD_SIZES = "kicad"

# Sources (relative to the repo root). The CADCAM export (Proteus 8.12 SP0, 2021-03-22) has
# Gerber X2 attributes; the drill is the gerber "Drill TOP-BOT Plated" (no Excellon, no
# non-plated holes).
CADCAM = "source/cadcam"
IPC = "source/cadcam/gate_drive_power_asym_fb_v3_ee10 - CADCAM Netlist.IPC"

# --- Schematic skeleton (make_skeleton) ----------------------------------------------

# (Proteus page, sheet name, file)
SHEETS = [
    (1, "Gate drivers", "01_gate_drivers.kicad_sch"),
    (2, "Gate supply", "02_gate_supply.kicad_sch"),
]
SCH_TITLE = "Half-bridge gate driver, asymmetric gate supply"
SCH_COMPANY = "gate_drive_power_asym_fb"
SCH_REV = "V3_ee10"
SCH_COMMENT = "Redrawn from Proteus gate_drive_power_asym_fb_v3_ee10"
SCH_NOTE = ("Half-bridge gate driver V3_ee10 - redrawn from Proteus. One sheet per Proteus PDF page.\n"
            "Net names follow the IPC-D-356A netlist (reference/pins_by_net.md).")

# --- IPC-D-356A fix-ups (ipc356) -----------------------------------------------------

# No refdes is longer than 6 characters on this board.
TRUNCATED_REFDES = {}
TRUNCATED_NETS = {}
KICAD_REFDES = {}

# No =POWER suffixes in this netlist.
NET_ALIASES = {}

# Blank-refdes records: 17 vias, 0.381 mm pad / 0.254 mm drill. No free pads, no holes.
VIA_DRILLS = (0.254,)
FREE_PAD_DRILLS = ()
HOLE_DRILLS = ()
HOLES_PLATED = True

# Expected counts in the Proteus file (PLAN.md section 1).
EXPECTED_IPC = {
    "nets": 24,           # NNAME declarations
    "records": 136,
    "refdes_raw": 41,     # 40 parts + the blank refdes of the vias
    "tht_records": 55,    # J9 30 pins + J1-J8 + 17 vias
    "smd_records": 81,
    "smd_top": 81,
    "smd_bottom": 0,
    "nc_pads": 0,
    "vias": 17,
    "free_pads": 0,
    "holes": 0,
    "parts": 40,
}

# --- Gerbers (check_sources, later the PCB tools) ------------------------------------

COPPER = [
    ("Top Copper", "F.Cu", "User.1"),
    ("Bottom Copper", "B.Cu", "User.2"),
]
DRILL_PLATED = "Drill TOP-BOT Plated"
DRILL_NONPLATED = None
OUTLINE = "Mechanical 1"
OUTLINE_RECT = (-23.254, 6.1, 22.411, 34.9)  # x, y, width, height

# --- PCB (p2k.build_pcb, gerber_to_tracks, assign_nets, pours_to_zones, check_board, drc) ---

# Proteus stack (CADCAM READ-ME): 2 x 0.036 Cu, 1.483 FR4 core.
PCB_THICKNESS = 1.555  # mm, without the 2 x 0.01 mm solder resist
# Design rules from the Proteus copper as built (STATUS.md "Phase 3", tools/measure_gaps.py), in mm.
PCB_RULES = dict(
    min_track=0.1,        # thinnest conductor draw 0.1016 (4 mil)
    min_via=0.38,         # all 17 vias 0.381 / 0.254
    min_annular=0.06,     # (0.381 - 0.254) / 2 = 0.0635
    min_drill=0.25,
    clearance=0.15,
    hole_clearance=0.15,
    hole_to_hole=0.25,
    edge_clearance=0.3,
    track=0.254,          # Default netclass
    via=0.381,
    via_drill=0.254,
)
# Board-only footprints: none (no mounting holes, no free pads on this board).

# Error-severity DRC types that remain by design ({type: reason}, see STATUS.md "Phase 3").
DRC_ACCEPTED = {
    "courtyards_overlap": "KiCad courtyards vs the dense Proteus placement (15 pairs)",
}

# --- Phase 4 checks (p2k.gerber_roundtrip, p2k.ipc356_diff) ---------------------------
# No stacked vias, no smaller KiCad drills (the KiCad drills are larger or equal), no Excellon file.
