#!/usr/bin/env python3
"""
Generate a visual workflow diagram for the Content Distribution Engine.
Uses Pillow with the AllAboutPMM visual style.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Canvas
WIDTH, HEIGHT = 1600, 2200
BG = "#F5F2ED"
BLACK = "#1A1A1A"
DARK = "#2C2C2C"
WHITE = "#FFFFFF"

# Accent palette
YELLOW = "#F7DC6F"
PINK = "#F5B7B1"
GREEN = "#ABEBC6"
TEAL = "#5BA4A4"
LIGHT_TEAL = "#B2DFDB"
LIGHT_YELLOW = "#FFF9C4"
LIGHT_PINK = "#FCE4EC"
LIGHT_GREEN = "#E8F5E9"

# Fonts
FONT_DIR = "/System/Library/Fonts/Supplemental"
try:
    font_title = ImageFont.truetype(os.path.join(FONT_DIR, "Georgia Bold.ttf"), 42)
    font_section = ImageFont.truetype(os.path.join(FONT_DIR, "Georgia Bold.ttf"), 28)
    font_label = ImageFont.truetype(os.path.join(FONT_DIR, "Arial Bold.ttf"), 20)
    font_body = ImageFont.truetype(os.path.join(FONT_DIR, "Arial.ttf"), 17)
    font_small = ImageFont.truetype(os.path.join(FONT_DIR, "Arial.ttf"), 14)
    font_brand = ImageFont.truetype(os.path.join(FONT_DIR, "Arial Bold.ttf"), 16)
except Exception:
    font_title = ImageFont.load_default()
    font_section = font_title
    font_label = font_title
    font_body = font_title
    font_small = font_title
    font_brand = font_title

img = Image.new("RGB", (WIDTH, HEIGHT), BG)
draw = ImageDraw.Draw(img)


def draw_box(x, y, w, h, fill, outline=BLACK, outline_width=2, radius=12):
    """Draw a rounded rectangle."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=outline_width)


def draw_arrow(x1, y1, x2, y2, color=BLACK, width=2):
    """Draw a line with arrowhead."""
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    # Arrowhead
    if y2 > y1:  # downward
        draw.polygon([(x2, y2), (x2 - 6, y2 - 10), (x2 + 6, y2 - 10)], fill=color)
    elif x2 > x1:  # rightward
        draw.polygon([(x2, y2), (x2 - 10, y2 - 6), (x2 - 10, y2 + 6)], fill=color)
    elif x2 < x1:  # leftward
        draw.polygon([(x2, y2), (x2 + 10, y2 - 6), (x2 + 10, y2 + 6)], fill=color)


def center_text(text, font, y, color=BLACK):
    """Draw centered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, y), text, fill=color, font=font)


def text_in_box(text, font, x, y, w, color=BLACK):
    """Draw text centered within a box width."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + (w - tw) // 2, y), text, fill=color, font=font)


# ============================================================
# TITLE
# ============================================================
center_text("Content Distribution Engine", font_title, 30, BLACK)
center_text("AllAboutPMM — PMM Brain-Powered", font_label, 80, DARK)

# ============================================================
# ROW 1: KNOWLEDGE LAYER (y=130)
# ============================================================
y_row1 = 140
center_text("KNOWLEDGE LAYER", font_section, y_row1, TEAL)

# 3 boxes: Newsletters, PMM Brain, Obsidian Vault
box_w, box_h = 420, 140
gap = 40
start_x = (WIDTH - 3 * box_w - 2 * gap) // 2

# Box 1: Newsletter Sources
bx1 = start_x
by1 = y_row1 + 45
draw_box(bx1, by1, box_w, box_h, LIGHT_YELLOW)
text_in_box("13 Newsletter Sources", font_label, bx1, by1 + 12, box_w, BLACK)
text_in_box("865 posts scraped", font_body, bx1, by1 + 40, box_w, DARK)
text_in_box("Pierri | Kramer | Poyar | Wynter", font_small, bx1, by1 + 65, box_w, DARK)
text_in_box("PMA | Aatir | Flanagan | HTG", font_small, bx1, by1 + 83, box_w, DARK)
text_in_box("GTM Strat | Social Files | +3 more", font_small, bx1, by1 + 101, box_w, DARK)

# Box 2: PMM Brain
bx2 = start_x + box_w + gap
draw_box(bx2, by1, box_w, box_h, YELLOW)
text_in_box("PMM Brain v3.0", font_label, bx2, by1 + 12, box_w, BLACK)
text_in_box("37 mental models", font_body, bx2, by1 + 42, box_w, DARK)
text_in_box("69 evidence stats", font_body, bx2, by1 + 64, box_w, DARK)
text_in_box("11 topic depth layers", font_body, bx2, by1 + 86, box_w, DARK)
text_in_box("26 emerging beliefs", font_body, bx2, by1 + 108, box_w, DARK)

# Box 3: Obsidian Vault
bx3 = start_x + 2 * (box_w + gap)
draw_box(bx3, by1, box_w, box_h, LIGHT_GREEN)
text_in_box("Obsidian Vault", font_label, bx3, by1 + 12, box_w, BLACK)
text_in_box("861 raw post notes", font_body, bx3, by1 + 42, box_w, DARK)
text_in_box("37 mental model notes", font_body, bx3, by1 + 64, box_w, DARK)
text_in_box("6 evidence bank notes", font_body, bx3, by1 + 86, box_w, DARK)
text_in_box("Canvas maps + wiki-links", font_body, bx3, by1 + 108, box_w, DARK)

# Arrows from newsletters to brain, brain to vault
draw_arrow(bx1 + box_w, by1 + box_h // 2, bx2, by1 + box_h // 2, TEAL, 2)
draw_arrow(bx2 + box_w, by1 + box_h // 2, bx3, by1 + box_h // 2, TEAL, 2)

# ============================================================
# ROW 2: ORCHESTRATOR (y=350)
# ============================================================
y_row2 = 350
center_text("ORCHESTRATOR", font_section, y_row2, TEAL)

orch_w, orch_h = 900, 80
orch_x = (WIDTH - orch_w) // 2
orch_y = y_row2 + 40
draw_box(orch_x, orch_y, orch_w, orch_h, TEAL)
text_in_box("CLAUDE.md v3.0 — Mode Router", font_label, orch_x, orch_y + 10, orch_w, WHITE)
text_in_box("Routes to 11 skills | Loads refs by tier | Injects Brain sections", font_body, orch_x, orch_y + 38, orch_w, WHITE)

# Arrow down from Brain to orchestrator
draw_arrow(bx2 + box_w // 2, by1 + box_h, bx2 + box_w // 2, orch_y, TEAL, 2)

# ============================================================
# ROW 3: TRIGGER MODES (y=490)
# ============================================================
y_row3 = 490
center_text("TRIGGER MODES", font_section, y_row3, TEAL)

modes = [
    ("Generate", "Write about X\nfor any format", LIGHT_YELLOW),
    ("Distribute", "Atomize\npillar \u2192 micro", LIGHT_TEAL),
    ("Expand", "LinkedIn \u2192\nnewsletter", LIGHT_GREEN),
    ("Research", "Deep research\n+ gap map", LIGHT_PINK),
    ("Suggest", "Theme ideas\nfrom Brain", LIGHT_YELLOW),
    ("Showcase", "Client demo\n+ portfolio", LIGHT_TEAL),
]

mode_w, mode_h = 200, 80
mode_gap = 20
mode_start_x = (WIDTH - len(modes) * mode_w - (len(modes) - 1) * mode_gap) // 2
mode_y = y_row3 + 40

for i, (name, desc, color) in enumerate(modes):
    mx = mode_start_x + i * (mode_w + mode_gap)
    draw_box(mx, mode_y, mode_w, mode_h, color)
    text_in_box(name, font_label, mx, mode_y + 8, mode_w, BLACK)
    for j, line in enumerate(desc.split("\n")):
        text_in_box(line, font_small, mx, mode_y + 34 + j * 16, mode_w, DARK)

# Arrow from orchestrator to modes
draw_arrow(WIDTH // 2, orch_y + orch_h, WIDTH // 2, mode_y, TEAL, 2)

# ============================================================
# ROW 4: GENERATION ENGINE (y=640)
# ============================================================
y_row4 = 650
center_text("GENERATION ENGINE", font_section, y_row4, TEAL)

# 3 Angles
angle_w, angle_h = 380, 100
angle_gap = 30
angle_start = (WIDTH - 3 * angle_w - 2 * angle_gap) // 2
angle_y = y_row4 + 45

angles = [
    ("Angle 1: Opinionated Reframe", "Highest comment potential\nChallenge common view + evidence", PINK),
    ("Angle 2: Framework / Model", "Highest save/share potential\nReusable tool + specific example", GREEN),
    ("Angle 3: Story-Led Insight", "Highest reaction potential\nDrop into moment + earned lesson", LIGHT_TEAL),
]

for i, (title, desc, color) in enumerate(angles):
    ax = angle_start + i * (angle_w + angle_gap)
    draw_box(ax, angle_y, angle_w, angle_h, color)
    text_in_box(title, font_label, ax, angle_y + 10, angle_w, BLACK)
    for j, line in enumerate(desc.split("\n")):
        text_in_box(line, font_small, ax, angle_y + 38 + j * 18, angle_w, DARK)

# Arrow down
draw_arrow(WIDTH // 2, mode_y + mode_h, WIDTH // 2, angle_y, TEAL, 2)

# ============================================================
# ROW 5: 5 HOOK TYPES (y=810)
# ============================================================
y_row5 = 810
center_text("5 HOOK TYPES", font_section, y_row5, TEAL)

hooks = [
    ("Stat Drop", "\u201c94% of B2B\nbrands lack...\""),
    ("Scene Drop", "\u201cVP of Sales\nslid a battlecard...\""),
    ("Name+Claim", "\u201cCanva is giving\nus a masterclass.\""),
    ("Before/After", "\u201c'We help teams' \u2192\n'Ship 2x faster'\""),
    ("How-To Claim", "\u201cHow to run\nwin/loss that...\""),
]

hook_w, hook_h = 240, 70
hook_gap = 20
hook_start = (WIDTH - len(hooks) * hook_w - (len(hooks) - 1) * hook_gap) // 2
hook_y = y_row5 + 40

for i, (name, example) in enumerate(hooks):
    hx = hook_start + i * (hook_w + hook_gap)
    draw_box(hx, hook_y, hook_w, hook_h, WHITE)
    text_in_box(name, font_label, hx, hook_y + 6, hook_w, BLACK)
    for j, line in enumerate(example.split("\n")):
        text_in_box(line, font_small, hx, hook_y + 30 + j * 16, hook_w, DARK)

# Arrow down
draw_arrow(WIDTH // 2, angle_y + angle_h, WIDTH // 2, hook_y, TEAL, 2)

# ============================================================
# ROW 6: EXPERT TECHNIQUES (y=950)
# ============================================================
y_row6 = 950
center_text("EXPERT TECHNIQUE LENSES (Tier 3 — max 2 per request)", font_section, y_row6, TEAL)

experts = [
    ("Ogilvy", "Headlines\nSubject lines", LIGHT_YELLOW),
    ("GaryVee", "Distribution\nPillar\u2192Micro", LIGHT_TEAL),
    ("Brunson", "Storytelling\nEpiphany Bridge", LIGHT_GREEN),
    ("Hormozi", "Value Equation\nOffer structure", LIGHT_PINK),
    ("Suby", "Lead gen\nHVCO rules", LIGHT_YELLOW),
]

exp_w, exp_h = 240, 65
exp_gap = 20
exp_start = (WIDTH - len(experts) * exp_w - (len(experts) - 1) * exp_gap) // 2
exp_y = y_row6 + 40

for i, (name, desc, color) in enumerate(experts):
    ex = exp_start + i * (exp_w + exp_gap)
    draw_box(ex, exp_y, exp_w, exp_h, color)
    text_in_box(name, font_label, ex, exp_y + 6, exp_w, BLACK)
    for j, line in enumerate(desc.split("\n")):
        text_in_box(line, font_small, ex, exp_y + 28 + j * 16, exp_w, DARK)

# Arrow down
draw_arrow(WIDTH // 2, hook_y + hook_h, WIDTH // 2, exp_y, TEAL, 2)

# ============================================================
# ROW 7: QUALITY GATE (y=1090)
# ============================================================
y_row7 = 1090
center_text("QUALITY GATE: RUBBER DUCK ESCALATOR", font_section, y_row7, TEAL)

phases = [
    ("MIRROR", "Experiential\nauthenticity"),
    ("PROBE", "Courage &\nhard truths"),
    ("CHALLENGE", "Logic &\nevidence rigor"),
    ("ILLUMINATE", "Insight quality\n& novelty"),
    ("CRYSTALLIZE", "Voice match\n+ AI decontam"),
]

ph_w, ph_h = 230, 75
ph_gap = 25
ph_start = (WIDTH - len(phases) * ph_w - (len(phases) - 1) * ph_gap) // 2
ph_y = y_row7 + 40

for i, (name, desc) in enumerate(phases):
    px = ph_start + i * (ph_w + ph_gap)
    draw_box(px, ph_y, ph_w, ph_h, WHITE, TEAL, 2)
    text_in_box(name, font_label, px, ph_y + 8, ph_w, TEAL)
    for j, line in enumerate(desc.split("\n")):
        text_in_box(line, font_small, px, ph_y + 32 + j * 16, ph_w, DARK)
    # Arrow between phases
    if i < len(phases) - 1:
        draw_arrow(px + ph_w, ph_y + ph_h // 2, px + ph_w + ph_gap, ph_y + ph_h // 2, TEAL, 2)

# Threshold label
center_text("Threshold: 8+/10 per phase | Max 3 rewrites | 24 AI pattern bans", font_body, ph_y + ph_h + 10, DARK)

# Arrow down
draw_arrow(WIDTH // 2, exp_y + exp_h, WIDTH // 2, ph_y, TEAL, 2)

# ============================================================
# ROW 8: OUTPUT FORMATS (y=1260)
# ============================================================
y_row8 = 1280
center_text("OUTPUT FORMATS", font_section, y_row8, TEAL)

fmt_y = y_row8 + 45

# Newsletter (pillar - larger)
nw_w, nw_h = 320, 170
nw_x = 80
draw_box(nw_x, fmt_y, nw_w, nw_h, YELLOW)
text_in_box("Newsletter", font_label, nw_x, fmt_y + 8, nw_w, BLACK)
text_in_box("PILLAR", font_small, nw_x, fmt_y + 30, nw_w, TEAL)
nw_lines = ["1500-3000 words", "3+ evidence anchors", "Subject line (Ogilvy)", "Epiphany Bridge stories", "Practitioner callout", "P.S. + single CTA"]
for j, line in enumerate(nw_lines):
    text_in_box(line, font_small, nw_x, fmt_y + 50 + j * 17, nw_w, DARK)

# Other 3 formats
other_formats = [
    ("LinkedIn", ["800-1200 chars", "1+ evidence anchor", "5 hook types", "White space + fragments", "No hashtags"], PINK),
    ("Twitter/X", ["7-10 tweets", "280 chars/tweet", "4 thread types", "Hook tweet = 80% effort", "1/ 2/ 3/ numbering"], GREEN),
    ("Carousel", ["5-10 slides", "1080x1080px", "1 point per slide", "AllAboutPMM brand", "Pillow-generated"], LIGHT_TEAL),
]

other_start_x = nw_x + nw_w + 60
other_gap = 30
other_w = 260
other_h = 140

for i, (name, lines, color) in enumerate(other_formats):
    ox = other_start_x + i * (other_w + other_gap)
    draw_box(ox, fmt_y + 15, other_w, other_h, color)
    text_in_box(name, font_label, ox, fmt_y + 23, other_w, BLACK)
    for j, line in enumerate(lines):
        text_in_box(line, font_small, ox, fmt_y + 47 + j * 17, other_w, DARK)
    # Arrow from newsletter to this format
    draw_arrow(nw_x + nw_w, fmt_y + 30 + i * 40, ox, fmt_y + 15 + other_h // 2, TEAL, 2)

# Arrow down from quality gate to output
draw_arrow(WIDTH // 2, ph_y + ph_h + 30, WIDTH // 2, fmt_y, TEAL, 2)

# "Distribute" label on arrows
draw.text((nw_x + nw_w + 10, fmt_y + 5), "Distribute", fill=TEAL, font=font_small)

# ============================================================
# ROW 9: REVERSE FLOW (y=1510)
# ============================================================
y_row9 = 1530
reverse_w, reverse_h = 700, 50
reverse_x = (WIDTH - reverse_w) // 2
draw_box(reverse_x, y_row9, reverse_w, reverse_h, LIGHT_TEAL)
text_in_box("Reverse: LinkedIn post \u2192 Expand skill \u2192 Full newsletter article", font_body, reverse_x, y_row9 + 14, reverse_w, BLACK)

# ============================================================
# ROW 10: AI DECONTAMINATION (y=1600)
# ============================================================
y_row10 = 1610
center_text("AI DECONTAMINATION LAYER", font_section, y_row10, TEAL)

decon_y = y_row10 + 40
col_w = 430
col_gap = 40
col_start = (WIDTH - 3 * col_w - 2 * col_gap) // 2

# Word level
draw_box(col_start, decon_y, col_w, 110, WHITE, TEAL, 1)
text_in_box("Word-Level Bans", font_label, col_start, decon_y + 8, col_w, TEAL)
text_in_box("Additionally, Furthermore, Moreover", font_small, col_start, decon_y + 32, col_w, DARK)
text_in_box("testament, landscape, showcasing, delve", font_small, col_start, decon_y + 50, col_w, DARK)
text_in_box("crucial, pivotal, robust, comprehensive", font_small, col_start, decon_y + 68, col_w, DARK)
text_in_box("streamline, harness, navigate, realm", font_small, col_start, decon_y + 86, col_w, DARK)

# Sentence level
draw_box(col_start + col_w + col_gap, decon_y, col_w, 110, WHITE, TEAL, 1)
text_in_box("Sentence-Level Bans", font_label, col_start + col_w + col_gap, decon_y + 8, col_w, TEAL)
text_in_box("\"It's not just X, it's Y\"", font_small, col_start + col_w + col_gap, decon_y + 32, col_w, DARK)
text_in_box("Synonym cycling (3+ names for same thing)", font_small, col_start + col_w + col_gap, decon_y + 50, col_w, DARK)
text_in_box("Forced rule-of-three lists", font_small, col_start + col_w + col_gap, decon_y + 68, col_w, DARK)
text_in_box("Hedging stacks, significance inflation", font_small, col_start + col_w + col_gap, decon_y + 86, col_w, DARK)

# Structure level
draw_box(col_start + 2 * (col_w + col_gap), decon_y, col_w, 110, WHITE, TEAL, 1)
text_in_box("Structure-Level Bans", font_label, col_start + 2 * (col_w + col_gap), decon_y + 8, col_w, TEAL)
text_in_box("Balanced hedging + \"it depends\" close", font_small, col_start + 2 * (col_w + col_gap), decon_y + 32, col_w, DARK)
text_in_box("Generic conclusions (\"time will tell\")", font_small, col_start + 2 * (col_w + col_gap), decon_y + 50, col_w, DARK)
text_in_box("Setup-payoff padding bookends", font_small, col_start + 2 * (col_w + col_gap), decon_y + 68, col_w, DARK)
text_in_box("Sniff test: could ChatGPT say this?", font_small, col_start + 2 * (col_w + col_gap), decon_y + 86, col_w, DARK)

# ============================================================
# ROW 11: CONNECTED SYSTEMS (y=1790)
# ============================================================
y_row11 = 1790
center_text("CONNECTED SYSTEMS", font_section, y_row11, TEAL)

conn_y = y_row11 + 40
conn_w = 600
conn_gap = 60
conn_start = (WIDTH - 2 * conn_w - conn_gap) // 2

# skills-test
draw_box(conn_start, conn_y, conn_w, 120, LIGHT_YELLOW)
text_in_box("skills-test Project", font_label, conn_start, conn_y + 10, conn_w, BLACK)
text_in_box("5 expert personas (full voice + frameworks)", font_small, conn_start, conn_y + 36, conn_w, DARK)
text_in_box("AI Super Team advisory board", font_small, conn_start, conn_y + 54, conn_w, DARK)
text_in_box("PMM Brain Showcase skill (client demos)", font_small, conn_start, conn_y + 72, conn_w, DARK)
text_in_box("41 goose-skills capabilities", font_small, conn_start, conn_y + 90, conn_w, DARK)

# Obsidian feedback
draw_box(conn_start + conn_w + conn_gap, conn_y, conn_w, 120, LIGHT_GREEN)
text_in_box("Obsidian Vault Feedback Loop", font_label, conn_start + conn_w + conn_gap, conn_y + 10, conn_w, BLACK)
text_in_box("Generated content \u2192 synthesis notes", font_small, conn_start + conn_w + conn_gap, conn_y + 36, conn_w, DARK)
text_in_box("Theme, models used, evidence cited", font_small, conn_start + conn_w + conn_gap, conn_y + 54, conn_w, DARK)
text_in_box("Critique scores + raw post links", font_small, conn_start + conn_w + conn_gap, conn_y + 72, conn_w, DARK)
text_in_box("Vault \u2192 Brain \u2192 Generation \u2192 Vault", font_small, conn_start + conn_w + conn_gap, conn_y + 90, conn_w, DARK)

# ============================================================
# ROW 12: STATS BAR (y=1960)
# ============================================================
y_row12 = 1980
stats_w = 1400
stats_h = 60
stats_x = (WIDTH - stats_w) // 2
draw_box(stats_x, y_row12, stats_w, stats_h, TEAL)
text_in_box("13 Sources  |  861 Notes  |  37 Models  |  69 Stats  |  4 Formats  |  5 Experts  |  24 AI Bans  |  5-Phase Gate", font_label, stats_x, y_row12 + 18, stats_w, WHITE)

# ============================================================
# BRAND MARK
# ============================================================
brand_w, brand_h = 160, 30
brand_x = WIDTH - brand_w - 30
brand_y = HEIGHT - brand_h - 20
draw_box(brand_x, brand_y, brand_w, brand_h, DARK, DARK, 1, 15)
text_in_box("AllAboutPMM", font_brand, brand_x, brand_y + 6, brand_w, WHITE)

# Version
draw.text((30, HEIGHT - 30), "Content Distribution Engine v3.0 | 2026-03-11", fill=DARK, font=font_small)

# Save
output_path = "/Users/sourav/creative-writer/data/output/workflow-diagram.png"
img.save(output_path, "PNG", quality=95)
print(f"Saved to {output_path}")
print(f"Size: {WIDTH}x{HEIGHT}px")
