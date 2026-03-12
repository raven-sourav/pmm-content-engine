#!/usr/bin/env python3
"""
Convert scraped newsletter JSON files into individual Obsidian markdown notes.
Creates a Raw Posts/{Newsletter Name}/ folder structure in the Obsidian vault.
"""

import json
import os
import re
import sys
from datetime import datetime
from html.parser import HTMLParser

VAULT_BASE = os.path.expanduser(
    "~/Documents/Knowledge-brain-Obsidian/Knowledge Brain/PMM Brain/Raw Posts"
)

# Map scraped JSON files to newsletter display names
NEWSLETTER_MAP = {
    "anthonypierri_full.json": "Anthony Pierri - In The Kitchen",
    "mkt1_full.json": "Emily Kramer - MKT1",
    "kylepoyar_full.json": "Kyle Poyar - Growth Unhinged",
    "peeplaja_full.json": "Peep Laja - Wynter",
    "nathanbaugh_full.json": "Nathan Baugh - World Builders",
    "pma_full.json": "Richard King - PMA",
    "aatir_full.json": "Aatir Abdul Rauf",
    "strategicnerds_full.json": "Prashant Sridharan - Strategic Nerds",
    "punchy_full.json": "Emma Stratton - Punchy",
    "howtheygrow_20260310_235216.json": "How They Grow",
    "gtmstrategist_20260310_235218.json": "GTM Strategist",
    "kieran_flanagan_20260310_235202.json": "Kieran Flanagan",
    "socialfiles_20260310_235221.json": "Social Files",
}

# Map to newsletter source note names for wiki-links
SOURCE_NOTE_MAP = {
    "Anthony Pierri - In The Kitchen": "Newsletter Sources/aatir_abdul_rauf",  # will fix below
    "Emily Kramer - MKT1": "Newsletter Sources/emily_kramer_mkt1",
    "Kyle Poyar - Growth Unhinged": "Newsletter Sources/kyle_poyar_growth_unhinged",
    "Peep Laja - Wynter": "Newsletter Sources/wynter",
    "Nathan Baugh - World Builders": "Newsletter Sources/nathan_baugh",
    "Richard King - PMA": "Newsletter Sources/richard_king_pma",
    "Aatir Abdul Rauf": "Newsletter Sources/aatir_abdul_rauf",
    "Prashant Sridharan - Strategic Nerds": "Newsletter Sources/strategic_nerds_prashant_sridharan",
    "Emma Stratton - Punchy": "Newsletter Sources/punchy_emma_stratton",
    "How They Grow": "Newsletter Sources/How They Grow (Jaryd Hermann)",
    "GTM Strategist": "Newsletter Sources/GTM Strategist (Maja Voje)",
    "Kieran Flanagan": "Newsletter Sources/Kieran Flanagan",
    "Social Files": "Newsletter Sources/Social Files (Tommy Clark)",
}


class HTMLToMarkdown(HTMLParser):
    """Simple HTML to markdown converter."""

    def __init__(self):
        super().__init__()
        self.result = []
        self.current_tag = None
        self.in_pre = False
        self.list_type = []  # stack of 'ul' or 'ol'
        self.ol_counter = []

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        if tag in ("h1", "h2", "h3", "h4"):
            level = int(tag[1])
            self.result.append("\n" + "#" * level + " ")
        elif tag == "p":
            self.result.append("\n\n")
        elif tag == "br":
            self.result.append("\n")
        elif tag == "strong" or tag == "b":
            self.result.append("**")
        elif tag == "em" or tag == "i":
            self.result.append("*")
        elif tag == "a":
            href = attrs_dict.get("href", "")
            self.result.append("[")
            self._pending_href = href
        elif tag == "ul":
            self.list_type.append("ul")
            self.result.append("\n")
        elif tag == "ol":
            self.list_type.append("ol")
            self.ol_counter.append(0)
            self.result.append("\n")
        elif tag == "li":
            if self.list_type and self.list_type[-1] == "ol":
                self.ol_counter[-1] += 1
                self.result.append(f"{self.ol_counter[-1]}. ")
            else:
                self.result.append("- ")
        elif tag == "blockquote":
            self.result.append("\n> ")
        elif tag == "pre":
            self.in_pre = True
            self.result.append("\n```\n")
        elif tag == "code" and not self.in_pre:
            self.result.append("`")
        elif tag == "img":
            alt = attrs_dict.get("alt", "")
            src = attrs_dict.get("src", "")
            self.result.append(f"![{alt}]({src})")

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "h4"):
            self.result.append("\n")
        elif tag == "strong" or tag == "b":
            self.result.append("**")
        elif tag == "em" or tag == "i":
            self.result.append("*")
        elif tag == "a":
            href = getattr(self, "_pending_href", "")
            self.result.append(f"]({href})")
        elif tag == "li":
            self.result.append("\n")
        elif tag == "ul":
            if self.list_type:
                self.list_type.pop()
        elif tag == "ol":
            if self.list_type:
                self.list_type.pop()
            if self.ol_counter:
                self.ol_counter.pop()
        elif tag == "pre":
            self.in_pre = False
            self.result.append("\n```\n")
        elif tag == "code" and not self.in_pre:
            self.result.append("`")
        self.current_tag = None

    def handle_data(self, data):
        self.result.append(data)

    def get_markdown(self):
        text = "".join(self.result)
        # Clean up excessive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def html_to_markdown(html):
    """Convert HTML to markdown."""
    if not html:
        return ""
    parser = HTMLToMarkdown()
    try:
        parser.feed(html)
        return parser.get_markdown()
    except Exception:
        # Fallback: strip tags
        return re.sub(r"<[^>]+>", "", html)


def sanitize_filename(title):
    """Make a safe filename from a post title."""
    # Remove or replace unsafe characters
    safe = re.sub(r'[<>:"/\\|?*]', "", title)
    safe = re.sub(r"\s+", " ", safe).strip()
    # Truncate to reasonable length
    if len(safe) > 80:
        safe = safe[:80].rsplit(" ", 1)[0]
    return safe


def create_post_note(post, newsletter_name, source_note):
    """Create an Obsidian markdown note for a single post."""
    title = post.get("title", "Untitled")
    subtitle = post.get("subtitle", "")
    date = post.get("date", "")
    url = post.get("url", "")
    author = post.get("author", "")
    tags = post.get("tags", [])

    # Get content - prefer body_html converted to markdown, then body_text
    body_html = post.get("body_html", "")
    body_text = post.get("body_text", "")

    if body_html:
        content = html_to_markdown(body_html)
    elif body_text:
        content = body_text
    else:
        content = "*Content not available — [read original post](" + url + ")*"

    # Parse date
    date_str = ""
    if date:
        try:
            dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
            date_str = dt.strftime("%Y-%m-%d")
        except Exception:
            date_str = date[:10] if len(date) >= 10 else date

    # Build frontmatter
    frontmatter = "---\n"
    safe_title = title.replace('"', "'")
    frontmatter += f"title: \"{safe_title}\"\n"
    frontmatter += f"source: \"{newsletter_name}\"\n"
    if author:
        frontmatter += f"author: \"{author}\"\n"
    if date_str:
        frontmatter += f"date: {date_str}\n"
    if url:
        frontmatter += f"url: \"{url}\"\n"
    if tags:
        frontmatter += "tags:\n"
        for t in tags:
            frontmatter += f"  - {t}\n"
    frontmatter += "---\n\n"

    # Build note body
    note = frontmatter
    note += f"# {title}\n\n"
    if subtitle:
        note += f"*{subtitle}*\n\n"
    note += f"**Source:** [[{source_note}|{newsletter_name}]]"
    if date_str:
        note += f" | **Date:** {date_str}"
    if url:
        note += f" | [Original]({url})"
    note += "\n\n---\n\n"
    note += content
    note += "\n"

    return note


def process_newsletter(json_file, newsletter_name, source_note):
    """Process a single newsletter JSON file and create Obsidian notes."""
    scraped_dir = "/Users/sourav/creative-writer/data/scraped"
    filepath = os.path.join(scraped_dir, json_file)

    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return 0

    with open(filepath) as f:
        data = json.load(f)

    posts = data if isinstance(data, list) else data.get("posts", [])

    # Create newsletter folder
    folder = os.path.join(VAULT_BASE, newsletter_name)
    os.makedirs(folder, exist_ok=True)

    created = 0
    for post in posts:
        title = post.get("title", "")
        if not title:
            continue

        filename = sanitize_filename(title) + ".md"
        filepath = os.path.join(folder, filename)

        note = create_post_note(post, newsletter_name, source_note)
        with open(filepath, "w") as f:
            f.write(note)
        created += 1

    return created


def create_index_note():
    """Create an index note that links to all newsletter raw post folders."""
    index = "---\ntags:\n  - index\n---\n\n"
    index += "# Raw Posts Index\n\n"
    index += "Full-text newsletter posts organized by source. "
    index += "For synthesized insights, see [[PMM Brain v3.0]].\n\n"

    for json_file, name in sorted(NEWSLETTER_MAP.items(), key=lambda x: x[1]):
        folder = os.path.join(VAULT_BASE, name)
        if os.path.exists(folder):
            count = len([f for f in os.listdir(folder) if f.endswith(".md")])
            source = SOURCE_NOTE_MAP.get(name, "")
            index += f"## [[{source}|{name}]]\n"
            index += f"- **{count} posts** in `Raw Posts/{name}/`\n\n"

    index_path = os.path.join(VAULT_BASE, "Raw Posts Index.md")
    with open(index_path, "w") as f:
        f.write(index)
    print(f"  Created index note")


def main():
    os.makedirs(VAULT_BASE, exist_ok=True)

    total = 0
    for json_file, name in NEWSLETTER_MAP.items():
        source_note = SOURCE_NOTE_MAP.get(name, name)
        print(f"Processing {name}...")
        count = process_newsletter(json_file, name, source_note)
        print(f"  Created {count} notes")
        total += count

    create_index_note()
    print(f"\nDone! Created {total} total Obsidian notes in {VAULT_BASE}")


if __name__ == "__main__":
    main()
