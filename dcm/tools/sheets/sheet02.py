#!/usr/bin/env python3
"""Sheet 2 - gate supply (PDF page 2): the two floating gate supplies (toroid secondaries 12t + 4t
on wire pads J3/J5/J4 and J6/J8/J7, ZLLS400TA rectifiers, MMSZ5228BS zener clamps, 4.7u caps,
10k bleeders) and the DCM primary switch Q1 (MMBT3904: 15V -> J1 - primary - J2 -> collector;
base from PWM_TRANS through R11, pull-down R13; clamp R7 - D9 - C9 || R14 back to 15V).
There is no PDF print of the DCM project: the rectifier half is the asym board's page 2 (same
parts and nets), the primary switch is drawn from the IPC netlist.
The toroid itself (10/6/4, 8t primary, 2 x (12t + 4t) secondaries) is wound and fitted by hand:
it has no symbol (as in Proteus, where it is a drawing only); a text note documents it."""
from _common import *  # noqa: F401,F403

sh = sheet("02_gate_supply.kicad_sch")


def rectifier_cell(X, Y, j_top, j_mid, j_bot, d_top, d_bot, z_top, z_bot, c_top, c_bot, r_bl, vcc, src, ret):
    """Rows: Y = vcc, Y + 10 = src, Y + 20 = ret. j_top -> d_top (A at the pin) -> vcc; j_mid on
    src; j_bot -> d_bot (C at the pin, A on ret). Zeners z_top (vcc-src) / z_bot (src-ret),
    cathodes up; caps c_top / c_bot pin 1 up; bleeder r_bl vcc-ret, pin 1 on vcc."""
    rows = [Y, Y + g(10), Y + g(20)]
    for j, row in zip((j_top, j_mid, j_bot), rows):
        terminal(sh, j, X, row, "left")
    _, a, c = horiz2(sh, "D_Schottky", d_top, X + g(10), rows[0], "ZLLS400TA", left="A", text="above")
    sh.wire((X, rows[0]), a)
    _, c2, a2 = horiz2(sh, "D_Schottky", d_bot, X + g(10), rows[2], "ZLLS400TA", left="C", text="below")
    sh.wire((X, rows[2]), c2)
    xz, xc, xr, xe = X + g(20), X + g(30), X + g(46), X + g(52)
    sh.wire(c, (xr, rows[0]))
    sh.wire((X, rows[1]), (xe, rows[1]))
    sh.wire(a2, (xr, rows[2]))
    for k, (z, cc) in enumerate(((z_top, c_top), (z_bot, c_bot))):
        mid = rows[k] + g(5)
        _, zt, zb = vert2(sh, "D_Zener", z, xz, mid, "MMSZ5228BS-7-F", top="C", text="left")
        _, ct, cb = vert2(sh, "C", cc, xc, mid, "4.7u", top=1)
        for (x, t, b) in ((xz, zt, zb), (xc, ct, cb)):
            sh.wire((x, rows[k]), t)
            sh.wire(b, (x, rows[k + 1]))
    for x in (xz, xc):
        for row in rows:
            sh.junction(x, row)
    _, rt, rb = vert2(sh, "R", r_bl, xr, Y + g(10), "10k", top=1)
    sh.wire((xr, rows[0]), rt)
    sh.wire(rb, (xr, rows[2]))
    sh.glabel(src, xe, rows[1], 0)
    # floating rails: global labels to sheet 1, power flags (fed by passives only)
    for net, row, d in ((vcc, rows[0], "up"), (ret, rows[2], "down")):
        q = (xc, row - g(4)) if d == "up" else (xc, row + g(4))
        sh.wire((xc, row), q)
        sh.glabel(net, q[0], q[1], 90 if d == "up" else 270)
        f = (xc + g(6), row)
        sh.junction(xc + g(6), row)
        sh.pwr_flag(f[0], f[1], 0 if d == "up" else 180)


rectifier_cell(g(30), g(20), "J3", "J5", "J4", "D3", "D4", "D7", "D8", "C1", "C2", "R9",
               "DRV1_VCC", "SOURCE_HI", "DRV1_RET")
rectifier_cell(g(30), g(72), "J6", "J8", "J7", "D1", "D2", "D6", "D5", "C4", "C3", "R10",
               "DRV2_VCC", "SOURCE_LO", "DRV2_RET")

# --- toroid primary switch (DCM) -----------------------------------------------------------
# Drawn from the IPC netlist (no PDF of the DCM project).
RAIL, SW, GROW = g(124), g(140), g(162)
x0 = g(30)
UX = g(84)
q = sh.place("Q_NPN", "Q1", UX, g(150), value="MMBT3904")
B, E, C = q.pin(1), q.pin(2), q.pin(3)
power_at(sh, "15V", (x0, RAIL), "left")
sh.wire((x0, GROW), (E[0], GROW))
power_at(sh, "GND", (x0, GROW), "left")
# 15V decoupling C8 (1206)
x = x0 + g(6)
_, ct, cb = vert2(sh, "C", "C8", x, (RAIL + GROW) / 2, "100n", top=2)
sh.wire((x, RAIL), ct)
sh.wire(cb, (x, GROW))
sh.junction(x, RAIL)
sh.junction(x, GROW)
# base drive: PWM_TRANS -> R11 -> B, pull-down R13 (pin 1 on PWM_TRANS)
xp = x0 + g(30)
_, r1, r2 = horiz2(sh, "R", "R11", (xp + B[0]) / 2, B[1], "10k", left=1, text="above")
sh.wire((x0 + g(24), B[1]), r1)
sh.glabel("PWM_TRANS", x0 + g(24), B[1], 180)
sh.wire(r2, B)
_, rt, rb = vert2(sh, "R", "R13", xp, B[1] + g(6), "2.2k", top=1, text="left")
sh.wire((xp, B[1]), rt)
sh.wire(rb, (xp, GROW))
sh.junction(xp, B[1])
sh.junction(xp, GROW)
sh.wire(E, (E[0], GROW))
# primary: 15V -> J1 (dot) ... J2 -> collector
xj = UX - g(10)
terminal(sh, "J1", xj, RAIL + g(4), "down")
sh.wire((xj, RAIL), (xj, RAIL + g(4)))
sh.junction(xj, RAIL)
sh.wire(C, (C[0], SW))
terminal(sh, "J2", xj, SW, "left")
sh.wire((xj, SW), (C[0], SW))
# clamp: collector -> R7 -> D9 (A) -> C9 || R14 -> 15V
_, a1, a2 = horiz2(sh, "R", "R7", C[0] + g(10), SW, "10k", left=2, text="below")
sh.wire((C[0], SW), a1)
sh.junction(C[0], SW)
_, d1, d2 = horiz2(sh, "D_Schottky", "D9", C[0] + g(22), SW, "ZLLS400TA", left="A", text="below")
sh.wire(a2, d1)
xn1, xn2 = C[0] + g(32), C[0] + g(40)
sh.wire(d2, (xn2, SW))
sh.junction(xn1, SW)
for xx, ref, sym, val in ((xn1, "C9", "C", "100n"), (xn2, "R14", "R", "10k")):
    _, t, b = vert2(sh, sym, ref, xx, (RAIL + SW) / 2, val, top=1)
    sh.wire((xx, RAIL), t)
    sh.wire(b, (xx, SW))
sh.junction(xn1, RAIL)
sh.wire((x0, RAIL), (xn2, RAIL))

sh.text("Gate power supply transformer (wound and fitted by hand, not on the BOM): toroid 10/6/4,\n"
        "as on the asym board (Proteus: a drawing only, no part). Windings of the asym drawing\n"
        "(dot = start; the DCM project has no PDF, the turns may differ):\n"
        "  primary: J1 (dot, 15V) - J2 (Q1 collector)\n"
        "  HI secondary: 12t J3 (dot) - J4, 4t J4 (dot) - J5\n"
        "  LO secondary: 12t J6 (dot) - J7, 4t J7 (dot) - J8\n"
        "DCM variant: single-ended primary switched by Q1, the flyback energy clamped by\n"
        "R7 - D9 into C9 || R14 at 15V. J5 / J8 on SOURCE_HI / SOURCE_LO, J4 / J7 on the\n"
        "negative-rail diodes (IPC netlist).", g(140), g(30))
sh.save()
print("sheet02: written")
