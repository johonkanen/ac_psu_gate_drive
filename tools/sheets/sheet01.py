#!/usr/bin/env python3
"""Sheet 1 - gate drivers (PDF page 1): the isolated gate drivers DRV1 (high side, PWM_HI ->
GATE_HI) and DRV2 (low side, PWM_LO -> GATE_LO), Si8271, and the HB GT connector J9."""
from _common import *  # noqa: F401,F403

sh = sheet("01_gate_drivers.kicad_sch")


def si8271_cell(ref, UX, UY, pwm, r_pd, c_dec, vcc, ret, dp, dm, r_on, r_off, gate, r_gs, src):
    """Si8271 cell as drawn in the PDF. Input: pwm label with pull-down r_pd (pin 1 = pwm),
    VDD1 + EN on 5V with c_dec (pin 2 = 5V), GND1 on GND. Output: VDD2 = vcc, GND2 = ret
    (global labels, the supply comes from sheet 2), OUT+ -> local label dp -> r_on (pin 1),
    OUT- -> dm -> r_off (pin 1), both pin 2 on the gate label, r_gs (pin 1 gate, pin 2 src)."""
    u = sh.place("SI8271", ref, UX, UY, value="SI8271")
    VIN, VDD1, GND1, EN = (u.pin(n) for n in (1, 2, 3, 4))
    VDD2, OUTP, OUTM, GND2 = (u.pin(n) for n in (8, 7, 6, 5))
    # --- input side
    xl = UX - g(46)
    sh.wire(VIN, (xl, VIN[1]))
    sh.glabel(pwm, xl, VIN[1], 180)
    _, rt, rb = vert2(sh, "R", r_pd[0], UX - g(40), VIN[1] + g(5), r_pd[1], top=1, text="left")
    sh.wire((UX - g(40), VIN[1]), rt)
    sh.junction(UX - g(40), VIN[1])
    gnd_row = rb[1] + g(2)
    xv = UX - g(24)                     # 5V column: VDD1 and EN, C_dec beside it
    sh.wire(VDD1, (xv, VDD1[1]))
    sh.wire(EN, (xv, EN[1]))
    sh.wire((xv, VDD1[1] - g(4)), (xv, EN[1]))
    sh.junction(xv, VDD1[1])
    power_at(sh, "5V", (xv, VDD1[1] - g(4)), "up")
    _, ct, cb = vert2(sh, "C", c_dec[0], UX - g(32), gnd_row - g(5), c_dec[1], top=2)
    sh.wire(ct, (UX - g(32), VDD1[1]), (xv, VDD1[1]))
    xg = UX - g(16)
    sh.wire(GND1, (xg, GND1[1]), (xg, gnd_row))
    sh.wire(rb, (rb[0], gnd_row), (xg, gnd_row))
    sh.wire(cb, (cb[0], gnd_row))
    sh.junction(cb[0], gnd_row)
    sh.junction(xg, gnd_row)
    sh.wire((xg, gnd_row), (xg, gnd_row + g(2)))
    power_at(sh, "GND", (xg, gnd_row + g(2)), "down")
    # --- output side
    q = (VDD2[0] + g(3), VDD2[1] - g(4))
    sh.wire(VDD2, (q[0], VDD2[1]), q)
    sh.glabel(vcc, q[0], q[1], 90)
    q = (GND2[0] + g(2), GND2[1] + g(8))
    sh.wire(GND2, (q[0], GND2[1]), q)
    sh.glabel(ret, q[0], q[1], 270)
    label_right(sh, dp, OUTP, 5)
    label_right(sh, dm, OUTM, 5)
    ya, yb = OUTP[1] - g(3), OUTM[1] + g(4)
    _, a1, a2 = horiz2(sh, "R", r_on[0], UX + g(22), ya, r_on[1], left=1, text="above")
    _, b1, b2 = horiz2(sh, "R", r_off[0], UX + g(22), yb, r_off[1], left=1, text="below")
    sh.wire(right(OUTP, 5), (right(OUTP, 5)[0], ya), a1)
    sh.wire(right(OUTM, 5), (right(OUTM, 5)[0], yb), b1)
    xj = UX + g(30)
    sh.wire(a2, (xj, a2[1]), (xj, b2[1]))
    sh.wire(b2, (xj, b2[1]))
    sh.junction(xj, b2[1])
    glabel_right(sh, gate, (xj, a2[1]), 4)
    sh.junction(xj, a2[1])
    _, rt, rb = vert2(sh, "R", r_gs[0], xj, b2[1] + g(6), r_gs[1], top=1, text="left")
    sh.wire((xj, b2[1]), rt)
    q = down(rb, 2)
    sh.wire(rb, q)
    sh.glabel(src, q[0], q[1], 270)
    return u


# PDF labels pwm_hi / drv1_vcc / Gate_HI / ... = IPC nets PWM_HI / DRV1_VCC / GATE_HI / ...
si8271_cell("DRV1", g(60), g(40), "PWM_HI", ("R1", "10k"), ("C6", "100n"), "DRV1_VCC", "DRV1_RET",
            "D1+", "D1-", ("R12", "22R"), ("R2", "3R"), "GATE_HI", ("R6", "10k"), "SOURCE_HI")
si8271_cell("DRV2", g(60), g(90), "PWM_LO", ("R3", "10k"), ("C5", "100n"), "DRV2_VCC", "DRV2_RET",
            "D2+", "D2-", ("R4", "22R"), ("R5", "3R"), "GATE_LO", ("R8", "10k"), "SOURCE_LO")

# --- J9 HB GT connector -------------------------------------------------------------------
JX, JY = g(170), g(65)
j9 = sh.place("HB_GT_CONNECTOR", "J9", JX, JY, value="HB GT CONNECTOR")
P = j9.pin
bus_group(sh, [P(15), P(17), P(19)], P(17), "left", label="SOURCE_HI")
bus_group(sh, [P(16), P(18), P(20)], P(18), "right", label="SOURCE_HI")
bus_group(sh, [P(21), P(23), P(25)], P(23), "left", label="GATE_HI")
bus_group(sh, [P(22), P(24)], P(24), "right", label="GATE_HI")
glabel_right(sh, "DRV1_VCC", P(26), 4)
bus_group(sh, [P(29), P(31), P(33)], P(31), "left", label="SOURCE_LO")
bus_group(sh, [P(30), P(32), P(34)], P(32), "right", label="SOURCE_LO")
bus_group(sh, [P(35), P(37), P(39)], P(37), "left", label="GATE_LO")
bus_group(sh, [P(36), P(38)], P(38), "right", label="GATE_LO")
glabel_right(sh, "DRV2_VCC", P(40), 4)
glabel_left(sh, "PWM_LO", P(43), 4)
glabel_right(sh, "PWM_HI", P(44), 4)
q = left(P(45), 4)
sh.wire(P(45), q)
power_at(sh, "GND", q, "left")
q = right(P(46), 4)
sh.wire(P(46), q)
power_at(sh, "5V", q, "right")
q = left(P(47), 4)
sh.wire(P(47), q)
power_at(sh, "15V", q, "left")
glabel_right(sh, "PWM_TRANS", P(48), 4)
# the rails enter the board on J9 (passive pins): power flags
flagged_power(sh, "5V", JX - g(30), JY + g(40))
flagged_power(sh, "15V", JX - g(20), JY + g(40))
flagged_power(sh, "GND", JX - g(10), JY + g(46))

sh.text("PDF labels pwm_hi/lo, drv1/2_vcc, Gate_HI/LO, Source_LO, 5v = nets PWM_HI/LO, DRV1/2_VCC,\n"
        "GATE_HI/LO, SOURCE_LO, 5V. J9 mates face to face with the baseboard J1-J4/J6/J8 (ac_psu):\n"
        "pins 43/44, 45/46, 47/48 swap; J9-47 '15V' is the baseboard's 20V rail.", g(20), g(130))
sh.save()
print("sheet01: written")
