#!/usr/bin/env python3
"""
Fetch missing full-text content for newsletter posts using Substack API.
For posts without body_html, tries the /api/v1/posts/{slug} endpoint.
For Beehiiv posts, fetches the HTML page and extracts content.
"""

import json
import os
import re
import sys
import time
import requests
from html.parser import HTMLParser

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/json",
}

SCRAPED_DIR = "/Users/sourav/creative-writer/data/scraped"


class TextExtractor(HTMLParser):
    """Extract text from HTML, focusing on article body content."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
        self.skip_tags = {"script", "style", "nav", "header", "footer", "aside"}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag in self.skip_tags:
            self.skip = True
        if tag in ("p", "br", "h1", "h2", "h3", "h4", "li"):
            self.text.append("\n")

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip = False
        if tag in ("p", "h1", "h2", "h3", "h4", "div", "blockquote"):
            self.text.append("\n")
        self.current_tag = None

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)

    def get_text(self):
        return re.sub(r"\n{3,}", "\n\n", "".join(self.text)).strip()


def extract_text_from_html(html):
    """Extract clean text from HTML."""
    parser = TextExtractor()
    try:
        parser.feed(html)
        return parser.get_text()
    except Exception:
        return re.sub(r"<[^>]+>", " ", html).strip()


def get_substack_base(url):
    """Extract the Substack base URL from a post URL."""
    # e.g. https://foo.substack.com/p/bar -> https://foo.substack.com
    m = re.match(r"(https?://[^/]+)", url)
    return m.group(1) if m else None


def fetch_substack_post(url, slug=None):
    """Try to fetch full content from Substack API."""
    base = get_substack_base(url)
    if not base:
        return None

    if not slug:
        # Extract slug from URL
        m = re.search(r"/p/([^/?#]+)", url)
        if m:
            slug = m.group(1)

    if not slug:
        return None

    try:
        api_url = f"{base}/api/v1/posts/{slug}"
        r = requests.get(api_url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            body = data.get("body_html", "")
            if body and len(body) > 100:
                return body
    except Exception:
        pass
    return None


def fetch_page_text(url):
    """Fetch a URL and extract article text from HTML."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            html = r.text
            # Try to find article/post body specifically
            # Look for common article containers
            for pattern in [
                r'<article[^>]*>(.*?)</article>',
                r'<div[^>]*class="[^"]*post-content[^"]*"[^>]*>(.*?)</div>',
                r'<div[^>]*class="[^"]*body[^"]*"[^>]*>(.*?)</div>',
            ]:
                m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
                if m:
                    text = extract_text_from_html(m.group(1))
                    if len(text) > 200:
                        return text

            # Fallback: extract all text
            text = extract_text_from_html(html)
            if len(text) > 200:
                return text
    except Exception as e:
        pass
    return None


def process_file(filename):
    """Process a single scraped JSON file and fetch missing content."""
    filepath = os.path.join(SCRAPED_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  File not found: {filepath}")
        return

    with open(filepath) as f:
        data = json.load(f)

    posts = data if isinstance(data, list) else data.get("posts", [])

    missing = [(i, p) for i, p in enumerate(posts) if not p.get("body_html") and not p.get("body_text")]
    print(f"  {len(posts)} total posts, {len(missing)} missing content")

    if not missing:
        return

    fetched = 0
    failed = 0

    for idx, post in missing:
        url = post.get("url", "")
        slug = post.get("slug", "")
        title = post.get("title", "?")
        platform = post.get("platform", "substack")

        if not url:
            continue

        # Try Substack API first
        body_html = None
        if platform == "substack" or "substack.com" in url:
            body_html = fetch_substack_post(url, slug)

        if body_html:
            post["body_html"] = body_html
            fetched += 1
            print(f"    [{fetched}] API: {title[:60]}")
        else:
            # Fallback: fetch page and extract text
            text = fetch_page_text(url)
            if text and len(text) > 100:
                post["body_text"] = text
                fetched += 1
                print(f"    [{fetched}] Web: {title[:60]}")
            else:
                failed += 1
                if failed <= 3:
                    print(f"    FAIL: {title[:60]} ({url})")

        time.sleep(0.3)  # Be polite

    # Write back
    with open(filepath, "w") as f:
        json.dump(posts if isinstance(data, list) else data, f, indent=2)

    print(f"  Done: {fetched} fetched, {failed} failed")


def main():
    files = [
        ("howtheygrow_20260310_235216.json", "How They Grow"),
        ("gtmstrategist_20260310_235218.json", "GTM Strategist"),
        ("mkt1_full.json", "MKT1"),
        ("kylepoyar_full.json", "Kyle Poyar"),
        ("kieran_flanagan_20260310_235202.json", "Kieran Flanagan"),
        ("anthonypierri_full.json", "Anthony Pierri"),
        ("strategicnerds_full.json", "Strategic Nerds"),
        ("socialfiles_20260310_235221.json", "Social Files"),
        ("aatir_full.json", "Aatir Abdul Rauf"),
    ]

    for filename, name in files:
        print(f"\n=== {name} ===")
        process_file(filename)

    print("\n\nAll done!")


if __name__ == "__main__":
    main()
