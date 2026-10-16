"""
OmniStream Pro - Professional Icon Generator
Generates high-definition application icons with modern squircle, gradient flow,
and dynamic multi-audio stream wave aesthetics.
"""

import math
from PIL import Image, ImageDraw, ImageFilter

def create_omnistream_icon(size=512):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Background Rounded Squircle with Subtle Neon Border
    padding = size * 0.06
    r = size * 0.22
    box = [padding, padding, size - padding, size - padding]

    # Create base squircle with radial gradient effect
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    bg_draw.rounded_rectangle(box, radius=r, fill=(15, 23, 42, 255)) # Slate 900 base

    # Subtle gradient overlay
    for i in range(int(box[1]), int(box[3])):
        ratio = (i - box[1]) / (box[3] - box[1])
        # From Deep Obsidian (#0B0F19) to Deep Indigo/Violet (#1E1B4B)
        cr = int(11 + ratio * 20)
        cg = int(15 + ratio * 12)
        cb = int(25 + ratio * 55)
        # Draw horizontal slice masked by squircle
        # We can draw line on gradient layer
        box_w = int(box[2] - box[0])
        slice_img = Image.new("RGBA", (box_w, 1), (cr, cg, cb, 255))
        bg.paste(slice_img, (int(box[0]), i, int(box[0]) + box_w, i + 1), mask=None)

    # Re-apply squircle mask for crisp edges
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(box, radius=r, fill=255)
    bg.putalpha(mask)

    # Draw neon outer border glow
    border_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(border_img)
    b_draw.rounded_rectangle(box, radius=r, outline=(99, 102, 241, 180), width=int(size * 0.016))
    
    # Outer glow layer
    glow = border_img.filter(ImageFilter.GaussianBlur(size * 0.03))
    img = Image.alpha_composite(img, glow)
    img = Image.alpha_composite(img, bg)
    img = Image.alpha_composite(img, border_img)

    # 2. Dynamic Central Emblem: OmniStream Ring + Multi-Audio Waves + Forward Stream Arrow
    center_x = size / 2
    center_y = size / 2

    emblem_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    e_draw = ImageDraw.Draw(emblem_layer)

    # Outer Arc Ring (representing Omni / Global stream loop)
    ring_radius = size * 0.28
    ring_width = int(size * 0.038)
    ring_box = [center_x - ring_radius, center_y - ring_radius,
                center_x + ring_radius, center_y + ring_radius]
    
    # Draw arc with electric cyan / indigo styling
    e_draw.arc(ring_box, start=35, end=325, fill=(6, 182, 212, 240), width=ring_width)

    # Inner Glow Stream Waves (3 audio frequency / stream velocity bars)
    bar_width = int(size * 0.035)
    bars = [
        # (offset_x, height, color)
        (-size * 0.12, size * 0.16, (14, 165, 233, 240)),  # Sky Blue
        (-size * 0.04, size * 0.24, (99, 102, 241, 255)),  # Indigo
        (size * 0.04, size * 0.18, (168, 85, 247, 245)),   # Purple
    ]

    for bx, bh, bcolor in bars:
        bar_box = [
            center_x + bx - bar_width / 2,
            center_y - bh / 2,
            center_x + bx + bar_width / 2,
            center_y + bh / 2
        ]
        e_draw.rounded_rectangle(bar_box, radius=bar_width / 2, fill=bcolor)

    # Forward Arrow / Stream Jet Point (on the right)
    arrow_pts = [
        (center_x + size * 0.12, center_y - size * 0.13),
        (center_x + size * 0.23, center_y),
        (center_x + size * 0.12, center_y + size * 0.13),
    ]
    e_draw.polygon(arrow_pts, fill=(236, 72, 153, 255)) # Vibrant Pink / Magenta

    # Dot satellite nodes for modern tech vibe
    e_draw.ellipse([center_x + size * 0.25 - 8, center_y - size * 0.15 - 8,
                    center_x + size * 0.25 + 8, center_y - size * 0.15 + 8],
                   fill=(34, 211, 238, 255))
    e_draw.ellipse([center_x - size * 0.24 - 7, center_y + size * 0.18 - 7,
                    center_x - size * 0.24 + 7, center_y + size * 0.18 + 7],
                   fill=(129, 140, 248, 255))

    # Add soft blur to emblem for radiant glow
    emblem_glow = emblem_layer.filter(ImageFilter.GaussianBlur(size * 0.025))
    img = Image.alpha_composite(img, emblem_glow)
    img = Image.alpha_composite(img, emblem_layer)

    return img

if __name__ == "__main__":
    icon = create_omnistream_icon(512)
    icon.save("app_icon.png", "PNG")
    print("Saved app_icon.png (512x512)")

    # Save Windows multi-resolution ICO
    icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icon.save("app_icon.ico", format="ICO", sizes=icon_sizes)
    print("Saved app_icon.ico with multi-resolution layers.")
