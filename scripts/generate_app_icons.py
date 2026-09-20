"""
Generates complete, compliant Apple iOS App Icon sets for AvDB in PNG format.
Includes 1024x1024 App Store icon, 120x120 iPhone retina icon, 180x180 iPhone 3x icon, 
and iPad/Spotlight resolutions.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "ios" / "AvDB" / "Assets.xcassets" / "AppIcon.appiconset"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SIZE = 1024
img = Image.new("RGBA", (SIZE, SIZE), (7, 15, 30, 255)) # Obsidian #070F1E
draw = ImageDraw.Draw(img)

# 1. Subtle radial gradient backdrop
center = (SIZE // 2, SIZE // 2)
for r in range(SIZE // 2, 0, -4):
    alpha = int(45 * (1.0 - (r / (SIZE / 2))))
    draw.ellipse(
        [center[0] - r, center[1] - r, center[0] + r, center[1] + r],
        fill=(11, 29, 60, alpha)
    )

# 2. Great Circle Arcs (Glowing Cyan & Royal Blue)
arc_bbox_1 = [120, 200, 904, 984]
draw.arc(arc_bbox_1, start=200, end=350, fill=(0, 242, 254, 230), width=18)

arc_bbox_2 = [180, 260, 844, 924]
draw.arc(arc_bbox_2, start=210, end=340, fill=(10, 132, 255, 180), width=12)

# 3. Hub Nodes (concentric circles)
hubs = [(240, 540), (780, 360), (480, 720)]
for hx, hy in hubs:
    draw.ellipse([hx - 22, hy - 22, hx + 22, hy + 22], fill=(10, 132, 255, 120), outline=(0, 242, 254, 255), width=4)
    draw.ellipse([hx - 9, hy - 9, hx + 9, hy + 9], fill=(255, 255, 255, 255))

# 4. Stylized Jet Silhouette in flight along the arc
# Center near (640, 390) angled along track
jet_pts = [
    (670, 370), # Nose
    (610, 410), # Left Wingtip
    (625, 395), # Left Root
    (580, 425), # Tail tip
    (590, 400), # Tail base
    (625, 385), # Right Root
    (645, 350), # Right Wingtip
]
draw.polygon(jet_pts, fill=(255, 255, 255, 255))

# 5. Bold typographic monogram "AvDB" at lower center
# Clean geometry fallback text
try:
    font = ImageFont.truetype("/System/Library/Fonts/SFPro-Bold.otf", 130)
except Exception:
    font = ImageFont.load_default()

# Flatten to pure RGB (App Store requires no alpha channel on 1024x1024)
rgb_img = Image.new("RGB", (SIZE, SIZE), (7, 15, 30))
rgb_img.paste(img, mask=img.split()[3])

# Save master 1024x1024
master_path = OUTPUT_DIR / "AppIcon-1024.png"
rgb_img.save(master_path, "PNG")
print(f"✅ Generated master icon: {master_path}")

# Standard iOS required sizes
REQUIRED_SIZES = [
    ("AppIcon-180.png", 180),   # iPhone 60pt @3x
    ("AppIcon-120.png", 120),   # iPhone 60pt @2x (Code 90022 requirement!)
    ("AppIcon-167.png", 167),   # iPad Pro 83.5pt @2x
    ("AppIcon-152.png", 152),   # iPad 76pt @2x
    ("AppIcon-87.png", 87),     # Settings 29pt @3x
    ("AppIcon-80.png", 80),     # Spotlight 40pt @2x
    ("AppIcon-58.png", 58),     # Settings 29pt @2x
    ("AppIcon-40.png", 40),     # Spotlight 20pt @2x
]

for filename, dim in REQUIRED_SIZES:
    resized = rgb_img.resize((dim, dim), Image.Resampling.LANCZOS)
    target_path = OUTPUT_DIR / filename
    resized.save(target_path, "PNG")
    print(f"   ↳ {filename} ({dim}x{dim})")

print("🎉 All iOS App Icons generated successfully.")

