# Hero pipeline

The hero is two 2880 by 962 images from the Framer export, shown through a before/after slider.
The originals say DESIGN on the left and RESEARCH on the right. We never edit them. Three scripts
in `tools/` derive the files the site actually uses.

## Inputs

| File | What |
|---|---|
| `assets/images/bkZpxj8grx5v3QcIPHdwYG9sw0o.webp` | Colour layer, dotted background, horizontal pattern period 38px |
| `assets/images/gERBzf4G8UwGf737LFgkQbapKiY.webp` | Sketch layer, grid background, pattern period 46px |

## Outputs

| File | Made by |
|---|---|
| `assets/images/hero-qual-quant-color.webp` | `tools/hero_relabel.py` then `tools/hero_toplabel.py` |
| `assets/images/hero-qual-quant-sketch.webp` | same |
| `assets/og.jpg` | `tools/og_image.py` from the two outputs above |

Run from the repo root, in this order:

```bash
python -I tools/hero_relabel.py
```

```bash
python -I tools/hero_toplabel.py
```

```bash
python -I tools/og_image.py
```

Each script writes check crops to `tools/out/` so you can eyeball the result before committing.
After regenerating, bump the `?v=` suffix on both hero image references in `index.html` and on
`og.jpg` in all seven pages.

## What `hero_relabel.py` does

1. Erases DESIGN and RESEARCH (and their underline or bracket) by cloning background from the
   same rows, shifted horizontally by a multiple of the pattern period. The shift is chosen by
   matching the bands just above and below the erase box, and the source must not overlap the
   box or contain dark pixels. Erase boxes: colour `(840, 96, 1160, 172)` and `(1650, 96, 2080,
   172)`; sketch `(840, 100, 1160, 212)` and `(1650, 100, 2080, 212)`. Icons start at y 219, so
   do not go lower.
2. Paints QUALITATIVE centred at x 994 and QUANTITATIVE at x 1861, top y 109 or 110, cap height
   41 for the colour layer (Arial Black, black, 3px underline) and 44 for the sketch layer (Segoe
   Print Bold, grey 74/75/75, roughened with a noise mask, bracket line with end ticks below).

## What `hero_toplabel.py` does

Paints AI UX RESEARCHER centred on x 1440 at top y 60, cap height 25 (colour, letterspaced
Arial Black) and 27 (sketch, roughened Segoe Print Bold). It first checks the band is clean. It
started at y 38 and the fixed nav clipped it; 60 is the tested value.

## What `og_image.py` does

Takes the left half of the colour layer and the right half of the sketch layer, crops to the
1200 by 630 ratio centred on the divider, darkens the bottom third with a gradient, and writes
"Reuben Luera" with the caption "AI UX Researcher | HP, Adobe Research, Amazon Fire TV". The
human chose this caption over "HP | Adobe Research | Amazon Fire TV".

## The slider

`assets/site.js` sets `--pos` from the range input. That is all it does now. The load-time swing
(34 to 66 and back) and the "Drag" pill were both built and then removed on 2026-10-08 at the
human's request; the arrows on the handle are the only affordance. See [[decisions]].

## On another OS

The scripts reference `C:/Windows/Fonts/ariblk.ttf`, `segoeprb.ttf` and `segoeuib.ttf`. Replace
with any heavy grotesque, a marker-style script, and a bold UI sans. The measurements above
assume similar cap-height to width ratios; check the crops in `tools/out/` after the first run.
