from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1290, 340
img = Image.new('RGB', (W, H))
px  = img.load()

# ── Background gradient (bilinear: dark navy → dark purple) ───────────────
# corners: TL=(10,10,23)  TR=(28,6,50)  BL=(8,6,30)  BR=(24,3,56)
TL = (10, 10, 23);  TR = (28,  6, 50)
BL = ( 8,  6, 30);  BR = (24,  3, 56)

for x in range(W):
    tx = x / (W - 1)
    for y in range(H):
        ty = y / (H - 1)
        r = int(TL[0]*(1-tx)*(1-ty) + TR[0]*tx*(1-ty) + BL[0]*(1-tx)*ty + BR[0]*tx*ty)
        g = int(TL[1]*(1-tx)*(1-ty) + TR[1]*tx*(1-ty) + BL[1]*(1-tx)*ty + BR[1]*tx*ty)
        b = int(TL[2]*(1-tx)*(1-ty) + TR[2]*tx*(1-ty) + BL[2]*(1-tx)*ty + BR[2]*tx*ty)
        px[x, y] = (r, g, b)

draw = ImageDraw.Draw(img)

# ── Fonts ─────────────────────────────────────────────────────────────────
FONT_DIR = '/usr/share/fonts/truetype/ubuntu/'
font_title   = ImageFont.truetype(FONT_DIR + 'Ubuntu-B.ttf', 128)
font_tag     = ImageFont.truetype(FONT_DIR + 'Ubuntu-R.ttf',  34)
font_wm      = ImageFont.truetype(FONT_DIR + 'Ubuntu-B.ttf', 360)

# ── Watermark "X" (very faint, right side) ───────────────────────────────
# Draw in a color slightly lighter than background corner
draw.text((W - 260, -60), 'X', fill=(36, 16, 72), font=font_wm)

# ── Title: "rebel" white + "X" green ─────────────────────────────────────
WHITE = (255, 255, 255)
GREEN = (18,  222, 115)   # #12DE73 — matches homescreen dot

X_START, Y_TITLE = 64, 78

# Measure "rebel" width
rebel_bbox = draw.textbbox((X_START, Y_TITLE), 'rebel', font=font_title)
rebel_w    = rebel_bbox[2] - rebel_bbox[0]

draw.text((X_START, Y_TITLE),            'rebel', fill=WHITE, font=font_title)
draw.text((X_START + rebel_w, Y_TITLE),  'X',     fill=GREEN, font=font_title)

# ── Tagline ───────────────────────────────────────────────────────────────
draw.text((X_START + 2, Y_TITLE + 136),
          'Built different. Made to dominate.',
          fill=(130, 130, 130), font=font_tag)

# ── Bottom accent line: green → purple → transparent ─────────────────────
for x in range(W):
    t = x / (W - 1)
    if t <= 0.35:
        # green → purple
        s = t / 0.35
        r = int(18  + (120 - 18)  * s)
        g = int(222 + (40  - 222) * s)
        b = int(115 + (230 - 115) * s)
        alpha = 1.0
    elif t <= 0.75:
        # purple → fade out
        s = (t - 0.35) / 0.40
        r = int(120 * (1 - s))
        g = int(40  * (1 - s))
        b = int(230 * (1 - s))
        alpha = 1.0 - s
    else:
        continue

    # Blend with background pixel
    for y in range(H - 3, H):
        bg = px[x, y]
        blended = (
            int(r * alpha + bg[0] * (1 - alpha)),
            int(g * alpha + bg[1] * (1 - alpha)),
            int(b * alpha + bg[2] * (1 - alpha)),
        )
        draw.point((x, y), fill=blended)

# ── Save ──────────────────────────────────────────────────────────────────
os.makedirs('/home/baraa/RebellionX-Repo/banners', exist_ok=True)
out = '/home/baraa/RebellionX-Repo/banners/rebelx.png'
img.save(out, 'PNG', optimize=True)
print(f'Saved {W}x{H} → {out}')
