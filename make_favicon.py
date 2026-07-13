from PIL import Image, ImageDraw
import os
import math

# =====================================================
# Favicon generator for Mohammad Tabatabaei website
# Same topology:
# one large central node + three connected smaller nodes

# =====================================================

os.makedirs("assets", exist_ok=True)

# Colors
GOLD = (240, 200, 120, 255)      # warm gold
BLUE = (125, 211, 252, 255)      # cyan blue
LINE = (58, 58, 58, 255)         # dark grey connectors
BG = (0, 0, 0, 0)                # transparent background


def draw_network_icon(size, output_path):
    """
    Draw one favicon PNG at a given size.
    The geometry is optimized to look clear even at 16x16.
    """

    # Draw larger first, then shrink for smooth edges
    scale = 8
    S = size * scale

    img = Image.new("RGBA", (S, S), BG)
    draw = ImageDraw.Draw(img)

    def sc(v):
        return int(v * scale)

    # Coordinates are designed on a 64x64 canvas
    # Then scaled to requested size.
    factor = size / 64

    def p(x, y):
        return (sc(x * factor), sc(y * factor))

    def r(value):
        return sc(value * factor)

    # Same topology as your original icon
    center = (25, 36)
    top = (25, 9)
    right = (51, 27)
    bottom = (43, 55)

    hub_radius = 13.5
    leaf_radius = 7.0

    hub_outline = 2.8
    leaf_outline = 2.6
    line_width = 4.3

    def draw_trimmed_line(a, b, radius_a, radius_b):
        ax, ay = a
        bx, by = b

        dx = bx - ax
        dy = by - ay
        dist = math.sqrt(dx * dx + dy * dy)

        ux = dx / dist
        uy = dy / dist

        start = (
            ax + ux * radius_a,
            ay + uy * radius_a
        )

        end = (
            bx - ux * radius_b,
            by - uy * radius_b
        )

        draw.line(
            [p(*start), p(*end)],
            fill=LINE,
            width=r(line_width)
        )

    # Draw connectors first
    for node in [top, right, bottom]:
        draw_trimmed_line(center, node, hub_radius, leaf_radius)

    # Draw central node: gold fill, blue outline
    cx, cy = center
    draw.ellipse(
        (
            p(cx - hub_radius, cy - hub_radius)[0],
            p(cx - hub_radius, cy - hub_radius)[1],
            p(cx + hub_radius, cy + hub_radius)[0],
            p(cx + hub_radius, cy + hub_radius)[1],
        ),
        fill=GOLD,
        outline=BLUE,
        width=r(hub_outline)
    )

    # Draw outer nodes: blue fill, gold outline
    for node in [top, right, bottom]:
        x, y = node
        draw.ellipse(
            (
                p(x - leaf_radius, y - leaf_radius)[0],
                p(x - leaf_radius, y - leaf_radius)[1],
                p(x + leaf_radius, y + leaf_radius)[0],
                p(x + leaf_radius, y + leaf_radius)[1],
            ),
            fill=BLUE,
            outline=GOLD,
            width=r(leaf_outline)
        )

    # Smooth downsampling
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    img.save(output_path, "PNG")
    print("Saved:", output_path)


# Create favicon PNG sizes
draw_network_icon(16, "assets/favicon-16.png")
draw_network_icon(32, "assets/favicon-32.png")
draw_network_icon(48, "assets/favicon-48.png")
draw_network_icon(64, "assets/favicon1.png")

# Also create a larger logo version if you want to use it in the navbar
draw_network_icon(256, "assets/logo-network.png")


# Create SVG favicon too
svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <line x1="25" y1="22.5" x2="25" y2="16" stroke="#3a3a3a" stroke-width="4.3" stroke-linecap="round"/>
  <line x1="37.5" y1="31.2" x2="44.4" y2="29.4" stroke="#3a3a3a" stroke-width="4.3" stroke-linecap="round"/>
  <line x1="34.0" y1="46.3" x2="38.6" y2="49.5" stroke="#3a3a3a" stroke-width="4.3" stroke-linecap="round"/>

  <circle cx="25" cy="36" r="13.5" fill="#f0c878" stroke="#7dd3fc" stroke-width="2.8"/>
  <circle cx="25" cy="9" r="7" fill="#7dd3fc" stroke="#f0c878" stroke-width="2.6"/>
  <circle cx="51" cy="27" r="7" fill="#7dd3fc" stroke="#f0c878" stroke-width="2.6"/>
  <circle cx="43" cy="55" r="7" fill="#7dd3fc" stroke="#f0c878" stroke-width="2.6"/>
</svg>
"""

with open("assets/favicon.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Saved: assets/favicon.svg")