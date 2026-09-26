# Wiring

Only three wires are needed: the two paddle contacts and their common ground.
The XIAO's internal pull-up resistors keep the inputs HIGH; closing a paddle
contact pulls the input to GND.

## Connections

| 3.5 mm jack   | Paddle      | XIAO pin |
|---------------|-------------|----------|
| **Tip**       | Dit         | **D1**   |
| **Ring**      | Dah         | **D2**   |
| **Sleeve**    | Common      | **GND**  |

This follows the usual convention for paddles (and the vband adapter):
tip = dit, ring = dah, sleeve = common. If your paddle is wired the other way
round, swap in software (see the README) instead of rewiring.

## XIAO SAMD21 pinout

Top view, USB‑C connector at the top:

```
              ┌──[USB-C]──┐
   A0 / D0  ──┤ 1      14 ├──  5V      (do not use)
   A1 / D1  ──┤ 2      13 ├──  GND     ◄── jack SLEEVE
   A2 / D2  ──┤ 3      12 ├──  3V3     (do not use)
   A3 / D3  ──┤ 4      11 ├──  D10
   A4 / D4  ──┤ 5      10 ├──  D9
   A5 / D5  ──┤ 6       9 ├──  D8
   A6 / D6  ──┤ 7       8 ├──  D7
              └───────────┘
      D1 ◄── jack TIP  (dit)
      D2 ◄── jack RING (dah)
```

## 3.5 mm plug and jack

```
   Plug:   ┌──────────┬──┬──────┬──┬────┐
           │  Sleeve  │▓▓│ Ring │▓▓│Tip >
           └──────────┴──┴──────┴──┴────┘
             common       dah       dit
```

### Jack breakout boards

Small TRS breakout boards are usually labelled for audio:

| Board label           | Contact | Connect to |
|-----------------------|---------|------------|
| `L` / `LEFT` / `T`    | Tip     | D1         |
| `R` / `RIGHT` / `R1`  | Ring    | D2         |
| `G` / `GND` / `S`     | Sleeve  | GND        |

Some boards and bare jacks have extra pins (switch contacts that open when a
plug is inserted, or a second ring pin on TRRS jacks). Leave those
unconnected.

**Always verify with a multimeter:** insert the paddle plug, set the meter to
continuity, and check which board pad beeps when you press dit and which when
you press dah (the other probe on the sleeve pad). Labels on cheap breakout
boards are not always right.

### Bare panel jack

Look at the jack from the solder side and use continuity again: plug in a
cable, then find the lug connected to the plug's tip, ring and sleeve. The
sleeve lug is usually the one connected to the metal bushing / front nut.

## Optional protection

The direct connection works and is what most DIY adapters use. If the paddle
cable is long or you want some protection against static discharge, add a
**220 Ω … 1 kΩ** resistor in series with each input:

```
   jack TIP  ──[ 220 Ω ]── D1
   jack RING ──[ 220 Ω ]── D2
   jack SLEEVE ──────────── GND
```

The internal pull-ups (≈ 40 kΩ) are much larger, so the logic levels are not
affected.

## Do not

- **Do not** connect 5V or 3V3 to the jack. The inputs only need to be pulled
  to GND by the paddle contacts.
- **Do not** connect the output of an external keyer, transceiver or any
  circuit that drives a voltage. The SAMD21 is a 3.3 V part and its pins are
  **not 5 V tolerant**.
- Avoid the XIAO's back-side pads (battery, SWD) unless you know what you are
  doing.

## Enclosure tips

- Glue or screw the jack to the enclosure so that plugging in does not stress
  the solder joints.
- Leave the USB‑C connector and the RST pads reachable, or at least keep the
  lid removable for firmware updates.
- A small window or light pipe over the yellow LED is handy to see the
  keying state.

## Quick test after wiring

1. Plug in the paddle, then the USB cable. The yellow LED blinks once.
2. Press dit: the yellow LED lights up. Same for dah.
3. Open <https://w3c.github.io/uievents/tools/key-event-viewer.html> and
   check: dit → `ControlLeft`, dah → `ControlRight`.
