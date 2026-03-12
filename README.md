# Content Distribution Engine — AllAboutPMM

A multi-format content distribution engine for PMM leaders. Powered by a synthesized PMM Brain built from 13 newsletters (861 raw posts), 37 mental models, and 5 expert technique libraries. Produces evidence-backed, operator-credible content across LinkedIn, Twitter/X, Newsletter, and Carousel — not generic AI fluff.

## How It Works

```
13 Newsletters → 861 Raw Posts → PMM Brain (37 models, 69 stats)
                                       ↓
                              Theme + Research
                                       ↓
                         ┌─────────────────────────────┐
                         │  3-Angle Generation Engine   │
                         │  (Contrarian / Framework /   │
                         │   Story-Led × 5 Hook Types)  │
                         └─────────────┬───────────────┘
                                       ↓
                         ┌─────────────────────────────┐
                         │   Rubber Duck Escalator      │
                         │   5-Phase Quality Gate       │
                         │   (Threshold: 8+/10)         │
                         └─────────────┬───────────────┘
                                       ↓
              ┌────────────┬───────────┼───────────┬────────────┐
              ↓            ↓           ↓           ↓            ↓
          Newsletter    LinkedIn    Twitter/X   Carousel    Visual
         (1500-3000   (800-1200    (7-10       (5-10       (Pillow
          words)       chars)      tweets)     slides)      image)
```

## The Pipeline

1. **PMM Brain** — Synthesized intelligence from 13 newsletters + 2 writer DNA profiles. 37 mental models, 69 evidence stats, 11 topic depth layers. This is the thinking engine.
2. **Research** — Deep web research on any theme. Produces a Research Brief + Gap Map.
3. **3-Angle Generation** — Every theme produces 3 drafts: contrarian reframe (drives comments), framework/mental model (drives saves/shares), story-led with earned insight (drives reactions). Works across all 4 formats.
4. **Rubber Duck Escalator** — 5-phase critique (MIRROR, PROBE, CHALLENGE, ILLUMINATE, CRYSTALLIZE) with format-adapted scoring. Auto-rewrites until quality threshold met.
5. **Distribution** — Newsletter article is the pillar. Atomizes into LinkedIn post + Twitter thread + Carousel. Also supports reverse (expand LinkedIn → newsletter).
6. **Expert Techniques** — Ogilvy headlines for subject lines, GaryVee Pillar→Micro for distribution, Brunson Epiphany Bridge for storytelling, Hormozi Value Equation and Suby HVCO for on-demand topics.
7. **Visual Generation** — Pillow-based images matching AllAboutPMM visual style.

## Architecture

```
creative-writer/
├── CLAUDE.md                          # Orchestrator v3.0 — routes to skills by mode
├── skills/
│   ├── generate/SKILL.md             # Multi-format content generation
│   ├── distribute/SKILL.md           # Atomize pillar → micro (newsletter → all)
│   ├── expand/SKILL.md               # Expand micro → pillar (LinkedIn → newsletter)
│   ├── showcase/SKILL.md             # Client demo / portfolio generator
│   ├── research/SKILL.md             # Deep research on a theme
│   ├── critique/SKILL.md             # Rubber Duck Escalator
│   ├── suggest-themes/SKILL.md       # Brain-informed theme suggestions
│   ├── visual/SKILL.md               # Visual brief + image generation
│   ├── ingest/SKILL.md               # Add new content to the system
│   └── scraper/SKILL.md              # Scrape Substack/Beehiiv newsletters
├── experts/                           # Tier 3: technique libraries (max 2 per request)
│   ├── ogilvy-headlines.md           # 9 headline principles, Big Idea test
│   ├── garyvee-distribution.md       # Pillar→Micro, JJJRH, platform-native rules
│   ├── brunson-storytelling.md       # Epiphany Bridge (7-step), Hook Story Offer
│   ├── hormozi-offers.md             # Value Equation, Grand Slam Offer, MAGIC naming
│   └── suby-leadgen.md              # HVCO, Godfather Offer, Larger Market Formula
├── references/                        # Protocol docs loaded by tier
│   ├── rubber-duck-escalator.md      # [Tier 1] 5-phase critique + format calibration
│   ├── generation-angles.md          # [Tier 1] 3 angles + hooks + format adaptations
│   ├── research-protocol.md          # [Tier 2] Research pipeline
│   ├── linkedin-practices.md         # [Tier 2] LinkedIn best practices
│   ├── twitter-practices.md          # [Tier 2] Twitter/X thread practices
│   ├── newsletter-practices.md       # [Tier 2] Newsletter article practices
│   ├── carousel-practices.md         # [Tier 2] LinkedIn carousel practices
│   └── format-adaptation-matrix.md   # [Tier 2] Cross-format adaptation rules
├── data/
│   ├── brain/pmm_brain.json          # PMM Brain v3.0
│   ├── output/                       # Generated content by format
│   │   ├── linkedin/
│   │   ├── twitter/
│   │   ├── newsletter/
│   │   └── carousel/
│   ├── scraped/                      # 13 newsletter JSON files (865 posts)
│   ├── user/
│   │   ├── my_posts.docx
│   │   └── visuals/                  # 20 reference images
│   └── writers/
├── scripts/
│   ├── fetch_missing_content.py      # Fetch full-text from Substack API
│   └── create_obsidian_posts.py      # Convert JSON → Obsidian markdown notes
├── src/                              # Python utilities
│   ├── schemas/                      # Pydantic data models
│   ├── brain/                        # brain_store.py, brain_injector.py
│   ├── storage/                      # SQLite + ChromaDB
│   ├── config/                       # Settings
│   └── ingestion/                    # .docx parsing, URL scraping
└── main.py                           # Utility CLI
```

## How Claude Code Uses This

This is NOT a traditional Python app with API calls. **Claude Code IS the LLM engine.** The `CLAUDE.md` file acts as an orchestrator that routes requests to skills, loads the right references and expert techniques, and injects the right Brain sections into each task.

### Content Formats

| Format | Target | Key Feature |
|--------|--------|-------------|
| **LinkedIn** | 800-1200 characters | 3 angles, 5 hook types, visual for frameworks |
| **Twitter/X** | 7-10 tweets, 280 chars each | 4 thread types, character validation per tweet |
| **Newsletter** | 1500-3000 words | Deep pillar format, 3+ evidence anchors, subject lines |
| **Carousel** | 5-10 slides | 1080x1080, AllAboutPMM visual design, 1 point per slide |

### Usage (via Claude Code)

```
# Generation
"Write about {theme}"                    → LinkedIn (default, 3 angles)
"Write a newsletter about {theme}"       → Newsletter article
"Write a thread about {theme}"           → Twitter/X thread
"Write about {theme} for all formats"    → Newsletter first, then distribute to all
"Create a carousel about {theme}"        → Carousel brief + visual

# Distribution
"Distribute this"                        → Atomize newsletter → LinkedIn + Twitter + Carousel
"Expand this into a newsletter"          → Turn LinkedIn post → full newsletter article

# Research & Ideation
"Research {theme}"                       → Deep research → Brief + Gap Map
"What should I write about?"             → Brain-informed theme suggestions
"Critique this: {draft}"                → Run Rubber Duck Escalator

# System
"Add this content: {url}"               → Ingest into Brain
"Create client showcase"                 → Portfolio demo for prospects
```

## PMM Brain (v3.0)

| Dimension | Count |
|-----------|-------|
| Newsletter sources | 13 |
| Raw post notes (Obsidian) | 861 |
| Synthesized mental models | 37 |
| Evidence bank stats | 69 |
| Topic depth layers | 11 |
| Emerging beliefs tracked | 26 |

## Expert Technique Libraries

Extracted techniques (no voice mimicry) from 5 marketing experts:

| Expert | Techniques | Use Case |
|--------|-----------|----------|
| **David Ogilvy** | 9 headline principles, Big Idea test, Research-First Discipline | Newsletter subject lines, carousel covers |
| **Gary Vaynerchuk** | Pillar→Micro model, Context > Content, JJJRH ratio | Distribution, multi-format generation |
| **Russell Brunson** | Epiphany Bridge (7-step), Hook Story Offer, Attractive Character | Story-led angles, newsletter expansion |
| **Alex Hormozi** | Value Equation, Grand Slam Offer, MAGIC naming | Posts about pricing, packaging, offers |
| **Sabri Suby** | HVCO rules, Godfather Offer, Larger Market Formula | Posts about lead gen, acquisition |

## Quality Gate: Rubber Duck Escalator

5-phase critique with format-adapted scoring:

| Phase | Lens | What It Catches |
|-------|------|----------------|
| MIRROR | Experiential authenticity | "Is this lived or Googled?" |
| PROBE | Courage | "What uncomfortable truth is being dodged?" |
| CHALLENGE | Rigor | "Where is the logic soft?" |
| ILLUMINATE | Insight quality | "Is the insight earned and non-obvious?" |
| CRYSTALLIZE | Voice + AI decontamination | "Does it sound like THIS person (not AI)?" |

- Threshold: All 5 phases must score 8+/10
- Max 3 rewrite iterations before flagging to user
- AI decontamination: 24 banned patterns (word, sentence, structure level)
- Format calibration: Newsletter demands more evidence, Twitter checks character counts, Carousel checks visual consistency

## Obsidian Vault

All research lives in an Obsidian vault at `~/Documents/Knowledge-brain-Obsidian/Knowledge Brain/PMM Brain/`:
- **Raw Posts/** — 861 full-text newsletter notes with YAML frontmatter and wiki-links
- **Mental Models/** — 37 synthesis notes
- **Evidence Bank/** — 6 category notes
- **Topic Layers/** — 11 depth notes
- **Canvas Maps/** — Visual theme clusters, contrarian views, newsletter synergy

## Connected: skills-test Project

The PMM Brain connects to `/Users/sourav/skill-test/` which has:
- 5 expert marketing personas (Ogilvy, GaryVee, Brunson, Hormozi, Suby) with full voice + frameworks
- AI Super Team advisory board mode
- PMM Brain Showcase skill for client demos and freelance outreach
- 41 goose-skills capabilities

## Utility CLI

```bash
python main.py init-db          # Initialize SQLite + ChromaDB
python main.py parse-docs       # Parse .docx files into structured data
python main.py scrape-urls      # Scrape URLs from data/writers/urls.txt
python main.py show-brain       # Display current Brain stats
```
