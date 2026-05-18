from PIL import Image, ImageDraw, ImageFont

SIZE   = 512
RADIUS = 108   # iOS icon corner radius at 512px

FONT_DIR = '/usr/share/fonts/truetype/ubuntu/'
font_R = ImageFont.truetype(FONT_DIR + 'Ubuntu-B.ttf', 300)
font_x = ImageFont.truetype(FONT_DIR + 'Ubuntu-B.ttf', 168)

WHITE = (255, 255, 255)
GREEN = (18,  222, 115)   # #12DE73

# ── Helpers ────────────────────────────────────────────────────────────────
def lerp(a, b, t): return int(a + (b - a) * t)

def gradient_bg(size):
    """Bilinear gradient: dark navy → dark purple (same palette as banner)"""
    img = Image.new('RGB', (size, size))
    px  = img.load()
    TL = (10, 10, 23); TR = (30,  6, 52)
    BL = ( 8,  5, 28); BR = (22,  2, 58)
    for x in range(size):
        tx = x / (size - 1)
        for y in range(size):
            ty = y / (size - 1)
            r = lerp(lerp(TL[0], TR[0], tx), lerp(BL[0], BR[0], tx), ty)
            g = lerp(lerp(TL[1], TR[1], tx), lerp(BL[1], BR[1], tx), ty)
            b = lerp(lerp(TL[2], TR[2], tx), lerp(BL[2], BR[2], tx), ty)
            px[x, y] = (r, g, b)
    return img

# ── Build icon ─────────────────────────────────────────────────────────────
bg   = gradient_bg(SIZE)
icon = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))

# Rounded-rect mask
mask = Image.new('L', (SIZE, SIZE), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE-1, SIZE-1], radius=RADIUS, fill=255)

icon.paste(bg.convert('RGBA'), mask=mask)
draw = ImageDraw.Draw(icon)

# ── Measure glyphs ─────────────────────────────────────────────────────────
R_bb = draw.textbbox((0, 0), 'R', font=font_R)
R_w  = R_bb[2] - R_bb[0]
R_h  = R_bb[3] - R_bb[1]

x_bb = draw.textbbox((0, 0), 'x', font=font_x)
x_w  = x_bb[2] - x_bb[0]
x_h  = x_bb[3] - x_bb[1]

# ── Position R (centered, slightly left & up) ──────────────────────────────
R_left = (SIZE - R_w) // 2 - 18
R_top  = (SIZE - R_h) // 2 - 16

# ── Faint "R" shadow / depth layer ────────────────────────────────────────
for off in [(4, 5), (3, 4), (2, 3)]:
    draw.text((R_left + off[0], R_top + off[1]), 'R',
              fill=(0, 0, 0, 60), font=font_R)

# ── Draw "R" in white ─────────────────────────────────────────────────────
draw.text((R_left, R_top), 'R', fill=WHITE + (255,), font=font_R)

# ── Position "x" deep inside the leg of R ────────────────────────────────
# Ubuntu Bold R at 300px: leg centre is ~68% x, 72% y of the R bounding box
X_cx = R_left + int(R_w * 0.72)
X_cy = R_top  + int(R_h * 0.72)

X_left = X_cx - x_w // 2
X_top  = X_cy - x_h // 2

# Dark mask: paint a patch of dark bg so the X "cuts through" the R leg
mask_pad = 6
draw.rectangle(
    [X_left - mask_pad, X_top - mask_pad,
     X_left + x_w + mask_pad, X_top + x_h + mask_pad],
    fill=(14, 10, 28, 220)
)

# Green glow layers
for off, a in [((4,4), 55), ((3,3), 90), ((2,2), 130), ((1,1), 80)]:
    draw.text((X_left + off[0], X_top + off[1]), 'x',
              fill=(18, 222, 115, a), font=font_x)

# Draw "x" in green on top
draw.text((X_left, X_top), 'x', fill=GREEN + (255,), font=font_x)

# ── Save ──────────────────────────────────────────────────────────────────
out = '/home/baraa/RebellionX-Repo/icons/rebelx.png'
import os; os.makedirs(os.path.dirname(out), exist_ok=True)
icon.save(out, 'PNG')
print(f'Icon saved → {out}')
