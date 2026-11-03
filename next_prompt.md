# Next prompt

Ready-to-paste prompt for the next agent session.

```
Work in /home/jari/dev/ac_psu_gate_drive (GitHub johonkanen/ac_psu_gate_drive; KiCad 10.0.7 conversion of the Proteus gate-driver board
gate_drive_power_asym_fb_v3_ee10; phases 0-4 and the JLC files are done). Read README.md, PLAN.md,
STATUS.md (findings and open questions) and fab/README.md. Never run the KiCad AppImage with --version.

Verify first: tools/check_all.sh must end with ALL CHECKS PASSED, with at handoff:
  compare: parts 40/40 present ... wrong-net pins 0; IPC nets touched 24, complete 24
  erc: 0 errors, 2 warnings
  check_footprints: 40/40 parts fitted ... worst residual 0.039 mm
  make_pcb: board rebuilt from scratch, byte-identical
  drc: 22 violations, 0 shorts, 0 unconnected, 0 parity issues (15 courtyards_overlap accepted)
  ipc356_diff: matched 136 ... 24 Proteus nets mapped 1:1, 0 mismatches
  roundtrip: only pad-shape clusters, drills 0 mismatches

Open for the user (ask, do not change without an answer):
1. The Si8271 variant (UVLO letter; fab BOM has SI8271AB-ISR provisionally, DB suggested for the
   17.5-20.5 V VDD2-GND2 supply). D6/D7 are 16 V in the BOM (user rails +14.5..16 / -3..-4.5 V).
2. DRV3 IXDD609D2TR has no JLC stock: distributor + hand-solder/consign, or redesign.
3. Baseboard pins 25/39 carry SDM_RAW_VOLTAGE signals on J2/J8/J4 and meet DRV1/2_VCC (finding 3).
4. Push only when the user asks.
5. Later (separate step): the noise fixes of ac_psu reports/noise/README.md finding 9 (local CM
   return capacitor, CM choke in the 15 V feed, low-capacitance gate-supply transformer). From then
   on the board deviates from Proteus: add an explicit deviation list as in ac_psu v4
   (lib/v4_deviations.csv / v4_copper.csv pattern) and freeze the generated board.

Done when: the chosen points are implemented, tools/check_all.sh passes, fab/ regenerated
(fab/make_fab.sh, python3 fab/jlc_bom_check.py 5) if the BOM changed, STATUS.md has a short
section, next_prompt.md is replaced, committed (Co-Authored-By: Claude Opus 5.5
<noreply@anthropic.com>), not pushed.
```
