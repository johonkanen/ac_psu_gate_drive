#!/usr/bin/env python3
"""Sheet 2 - gate supply (PDF page 2): the two floating gate supplies (toroid secondaries 12t + 4t
on wire pads J3/J5/J4 and J6/J8/J7, ZLLS400TA rectifiers, MMSZ5228BS zener clamps, 4.7u caps,
10k bleeders) and the toroid primary driver DRV3 (IXDD609, PWM_TRANS -> J1, J2 via C12 to GND).
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

# --- toroid primary driver ------------------------------------------------------------------
UX, UY = g(90), g(135)
u = sh.place("IXDD609", "DRV3", UX, UY, value="IXDD609D2TR")
VCC1, VCC8, IN, EN = u.pin(1), u.pin(8), u.pin(2), u.pin(3)
OUTA, OUTB, GND4, GND5, TAB = u.pin(7), u.pin(6), u.pin(4), u.pin(5), u.pin(9)
RAIL, GROW = UY - g(16), UY + g(16)
xs = UX - g(12)
sh.wire(VCC1, (xs, VCC1[1]))
sh.wire(VCC8, (xs, VCC8[1]))
sh.wire(EN, (xs, EN[1]))
sh.wire((xs, RAIL), (xs, EN[1]))
sh.junction(xs, VCC1[1])
sh.junction(xs, VCC8[1])
x0 = g(40)
sh.wire((x0, RAIL), (xs, RAIL))
power_at(sh, "15V", (x0, RAIL), "left")
sh.wire((x0, GROW), (UX + g(10), GROW))
power_at(sh, "GND", (x0, GROW), "left")
for i, (cref, cval) in enumerate((("C7", "4.7u"), ("C8", "100n"))):
    x = x0 + g(6 + 8 * i)
    _, ct, cb = vert2(sh, "C", cref, x, (RAIL + GROW) / 2, cval, top=2)
    sh.wire((x, RAIL), ct)
    sh.wire(cb, (x, GROW))
    sh.junction(x, RAIL)
    sh.junction(x, GROW)
xr = x0 + g(24)
sh.wire(IN, (x0, IN[1]))
sh.glabel("PWM_TRANS", x0, IN[1], 180)
_, rt, rb = vert2(sh, "R", "R11", xr, IN[1] + g(6), "10k", top=1)
sh.wire((xr, IN[1]), rt)
sh.wire(rb, (xr, GROW))
sh.junction(xr, IN[1])
sh.junction(xr, GROW)
xg = UX + g(10)
for p in (GND4, GND5, TAB):
    sh.wire(p, (xg, p[1]))
sh.wire((xg, min(GND4[1], GND5[1], TAB[1])), (xg, GROW))
for p in (GND4, GND5, TAB):
    if p[1] != min(GND4[1], GND5[1], TAB[1]):
        sh.junction(xg, p[1])
sh.junction(xg, GROW)
# outputs joined -> J1 (primary start); J2 (primary end) -> C12 -> GND
xo = UX + g(14)
sh.wire(OUTA, (xo, OUTA[1]), (xo, OUTB[1]), OUTB)
sh.junction(xo, OUTA[1])
terminal(sh, "J1", xo + g(6), OUTA[1], "right")
sh.wire((xo, OUTA[1]), (xo + g(6), OUTA[1]))
xc = UX + g(30)
terminal(sh, "J2", xc, OUTA[1] - g(4), "up")
_, ct, cb = vert2(sh, "C", "C12", xc, OUTA[1] + g(6), "100n", top=2)
sh.wire((xc, OUTA[1] - g(4)), ct)
sh.wire(cb, (xc, GROW), (xg, GROW))

sh.text("Gate power supply transformer (wound and fitted by hand, not on the BOM): toroid 10/6/4,\n"
        "drawn in the Proteus PDF as a graphic only (no part). Windings as drawn there (dot = start):\n"
        "  primary 8t: J1 (dot) - J2\n"
        "  HI secondary: 12t J3 (dot) - J4, 4t J4 (dot) - J5\n"
        "  LO secondary: 12t J6 (dot) - J7, 4t J7 (dot) - J8\n"
        "Note: the rectifier circuit above has J5 / J8 on SOURCE_HI / SOURCE_LO and J4 / J7 on the\n"
        "negative-rail diodes (IPC netlist); the drawing puts J4 / J7 between the 12t and 4t windings.\n"
        "PDF labels drv1_vcc / pwm_trans = nets DRV1_VCC / PWM_TRANS.", g(140), g(30))
sh.save()
print("sheet02: written")
