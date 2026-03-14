# Skill Index — Content Distribution Engine

## Data Flow

```
[research] → theme + evidence anchors
     ↓
[suggest-themes] ← Brain (mental models, value landscape)
     ↓
[generate] → draft (3 angles × format) → [critique] (Rubber Duck 5-phase)
     ↓                                         ↓
     ↓                                    pass (8+) or revise
     ↓
[distribute] → newsletter → LinkedIn + Twitter + Carousel
[expand]     → LinkedIn → newsletter (reverse)
     ↓
[visual] → framework visuals for posts

[ingest] ← new content (posts, URLs, .docx)
[scraper] ← Substack/Beehiiv newsletters → [ingest] → Brain update
```

## Skills

| Skill | Purpose | Depends On | Feeds Into |
|-------|---------|------------|------------|
| `research/` | Deep web research on a theme | Brain (value landscape, newsletter insights) | generate |
| `suggest-themes/` | Brain-informed theme suggestions | Brain (mental models, value landscape) | generate |
| `generate/` | Multi-format content generation | Tier 1 refs + Brain + research output | critique, distribute |
| `critique/` | Run Rubber Duck Escalator (5 phases) | rubber-duck-escalator.md, voice profile | generate (revision loop) |
| `distribute/` | Atomize pillar → micro formats | format-adaptation-matrix, garyvee-distribution | standalone outputs |
| `expand/` | Expand micro → pillar (LinkedIn → newsletter) | newsletter-practices, brunson, ogilvy | standalone outputs |
| `visual/` | Generate visual brief + image | Brain visual signature, reference images | post enhancement |
| `showcase/` | Client demo / portfolio generator | Brain + output examples | standalone |
| `ingest/` | Add new content to system | Current Brain (for delta) | Brain update |
| `scraper/` | Scrape Substack/Beehiiv newsletters | scraper scripts | ingest → Brain |

## Meta-Layer (Self-Improving)

| Skill | Purpose | Watches |
|-------|---------|---------|
| `observe/` | Log execution quality signals | All content skills |
| `inspect-amend/` | Propose amendments from observation patterns | observe logs → skill/reference files |
| `ship/` | Safe push with secret scanning | Git operations |

**Primary metric**: Rubber Duck first-attempt pass rate (target: >50%)

## Knowledge Tiers

- **Tier 1** (always): rubber-duck-escalator, generation-angles
- **Tier 2** (triggered): format practices, research-protocol, format-adaptation-matrix
- **Tier 3** (max 2): expert technique libraries (ogilvy, garyvee, brunson, hormozi, suby)
- **Brain**: Load relevant sections only (mental models, evidence, topics, voice)
