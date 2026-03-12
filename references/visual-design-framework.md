# Visual Design Framework — AllAboutPMM

Derived from analysis of 29 reference visuals (Anthony Pierri "In The Kitchen" + Sourav "pmm camp").

---

## 1. CANVAS

- **Size:** 1080x1080px (square, LinkedIn optimal) or 1080x1350px (portrait)
- **Background:** Off-white/cream (#F5F2ED) or pure white (#FFFFFF)
- **Margins:** 60-80px on all sides — generous whitespace is non-negotiable
- **No gradients, no textures, no decorative elements**

## 2. TYPOGRAPHY

### Title (top of canvas)
- **Font:** Bold serif or heavy sans-serif display
- **Size:** 52-72px (dominant, takes 15-25% of canvas height)
- **Weight:** Black/ExtraBold for key words, Regular for connecting words
- **Color:** Black (#1A1A1A)
- **Keyword highlighting:** 1-2 key words get a colored background pill (green #C8F7C5, teal #5BA4A4, yellow #F7DC6F) or a box outline

### Subtitle (optional, below title)
- **Font:** Regular weight serif or sans-serif
- **Size:** 22-28px
- **Color:** Dark gray (#4A4A4A)
- **Style:** Italic serif for editorial feel, or light sans-serif

### Body/Labels
- **Font:** Sans-serif (clean, modern)
- **Size:** 18-24px for labels, 14-18px for descriptions
- **Weight:** Bold for labels/headers inside boxes, Regular for descriptions
- **Color:** Black for labels, dark gray (#555) for descriptions

## 3. COLOR PALETTE

### Primary (use for 80% of design)
- Background: #F5F2ED (warm cream) or #FFFFFF (white)
- Text: #1A1A1A (near-black)
- Outlines: #2A2A2A (dark, thin)

### Accent colors (use sparingly, 1-3 per visual)
- **Yellow/Amber:** #F7DC6F / #FFF3CD (warm, muted)
- **Pink/Salmon:** #F5B7B1 / #FADBD8 (soft, not hot)
- **Green/Mint:** #ABEBC6 / #D5F5E3 (light, calming)
- **Teal/Blue-green:** #5BA4A4 / #A3D9D9 (muted, sophisticated)
- **Blue/Indigo:** #3B5998 / #AED6F1 (rare, for emphasis)

### Rules
- Never more than 3 accent colors per visual
- Colors are always MUTED/PASTEL — never saturated
- Use color to encode meaning (e.g., good/better/best progression)
- Black + white + ONE accent color is the safest combination

## 4. STRUCTURAL ELEMENTS

### Boxes/Cards
- **Thin black outlines:** 1.5-2px stroke, no fill or light pastel fill
- **Corner radius:** 0px (sharp) or 4-8px (slight round) — never fully rounded
- **Padding inside:** 20-30px
- **No drop shadows, no 3D effects**

### Lines/Arrows
- **Weight:** 1.5-2px
- **Style:** Solid for connections, occasional curved/organic lines for flow
- **Arrows:** Simple, thin, minimal arrowheads
- **Brackets:** Thin right-bracket to group items with annotation

### Dividers
- Thin horizontal lines (1px, gray) to separate sections
- OR alternating light background bands (white/cream alternation)

## 5. LAYOUT PATTERNS

### Pattern A: Stacked Rows
- Vertical stack of 3-6 rectangular boxes, left-aligned
- Each box: bold label + description to the right
- Annotations/descriptions float to the right of boxes
- Best for: lists, zones, sequential steps

### Pattern B: Matrix/Grid
- 3 columns (e.g., Good/Better/Best) x 3-5 rows
- Column headers get colored backgrounds
- Cell fills get progressively lighter tints of header color
- Best for: comparison frameworks, progression

### Pattern C: Concentric Circles
- 2-4 nested circles, centered
- Labels inside each ring
- Annotations with thin lines pointing outward
- Best for: targeting, narrowing focus, nested concepts

### Pattern D: Flow/Branch
- Central concept with 2-3 branches
- Thin curved lines connecting nodes
- Leaf nodes are colored blocks (different pastel per branch)
- Best for: decision trees, category approaches

### Pattern E: Two-Column Compare
- Left/right split with clear visual separator
- Each side has its own color scheme or icon treatment
- Best for: before/after, old way/new way, vs. comparisons

### Pattern F: Quote/Statement Card
- Large bold text (36-48px) centered on colored background
- 1-2 keywords highlighted in contrasting color pill
- Minimal — just the statement and brand mark
- Best for: single powerful insight, hook reinforcement

## 6. BRAND MARK

- **Text:** "AllAboutPMM"
- **Position:** Bottom-right corner
- **Style:** Bold sans-serif in a dark rounded rectangle pill, or simple bold text
- **Size:** Small (16-20px) — present but not dominant
- **Color:** Dark background (#1A1A1A) with white text, or just dark text on canvas

## 7. INFORMATION HIERARCHY

1. **Title** — largest, boldest, top of canvas (what is this about?)
2. **Subtitle/Context** — smaller, lighter, immediately below title
3. **Framework/Diagram** — the visual structure, center of canvas (60% of space)
4. **Labels/Content** — inside or beside the framework elements
5. **Annotations** — small text, descriptions, sources (smallest, peripheral)
6. **Brand mark** — bottom-right, smallest element

## 8. ANTI-PATTERNS (Never Do These)

- Bright/saturated colors (red, electric blue, neon green)
- Gradients or color transitions
- Icons, clipart, stock imagery (except rare intentional pixel art)
- Drop shadows or 3D effects
- More than 3 accent colors
- Cramped layouts — if it feels tight, remove content
- Centered body text (left-align or structured in boxes)
- Decorative borders or ornaments
- Rounded pill-shaped content boxes (only for brand mark/highlights)
- Small title text — the title should be readable from a phone thumbnail

## 9. FONT STACK (Pillow Implementation)

Since Pillow has limited font access, use system fonts:
- **Title:** Georgia Bold or Arial Black (serif display feel)
- **Body:** Helvetica or Arial (clean sans-serif)
- **Fallback:** Load .ttf files if available
- For keyword highlighting: draw a colored rectangle behind the text
