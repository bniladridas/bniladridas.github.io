#!/usr/bin/env python3
"""Extract content from all HTML pages and generate search-index.json.

Usage: python3 build-index.py
"""

import os
import re
import json

ROOT = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    {"url": "/", "file": "index.html", "breadcrumb": "Home"},
    {"url": "/about/", "file": "about/index.html", "breadcrumb": "About"},
    {"url": "/ethos/", "file": "ethos/index.html", "breadcrumb": "Ethos"},
    {"url": "/methodology/", "file": "methodology/index.html", "breadcrumb": "Methodology"},
    {"url": "/auth/", "file": "auth/index.html", "breadcrumb": "Sign in"},
    {"url": "/agents/", "file": "agents/index.html", "breadcrumb": "Agents"},
]

AGENT_IDS = sorted([
    d for d in os.listdir(os.path.join(ROOT, 'agents'))
    if os.path.isdir(os.path.join(ROOT, 'agents', d))
    and os.path.exists(os.path.join(ROOT, 'agents', d, 'index.html'))
])

for aid in AGENT_IDS:
    PAGES.append({
        "url": f"/agents/{aid}/",
        "file": f"agents/{aid}/index.html",
        "breadcrumb": f"Agents / {aid.replace('-', ' ').title()}",
    })


def extract_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    return m.group(1).strip() if m else ''


def extract_meta(html, name):
    m = re.search(
        rf'<meta\s+name=["\']{name}["\']\s+content=["\'](.*?)["\']',
        html, re.IGNORECASE
    )
    if not m:
        m = re.search(
            rf'<meta\s+content=["\'](.*?)["\']\s+name=["\']{name}["\']',
            html, re.IGNORECASE
        )
    return m.group(1).strip() if m else ''


def strip_tags(text):
    return re.sub(r'<[^>]+>', '', text)


def clean_whitespace(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_sections(html):
    """Extract h1/h2/h3 headings and their following content from <main>."""
    main_m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if not main_m:
        return []
    main_html = main_m.group(1)

    sections = []
    pattern = re.compile(r'<h([123])[^>]*>(.*?)</h\1>')

    prev_end = None
    prev_heading = None

    for m in pattern.finditer(main_html):
        heading_text = clean_whitespace(strip_tags(m.group(2)))
        start = m.end()

        if prev_heading is not None and prev_end is not None:
            content_html = main_html[prev_end:m.start()]
            content_text = clean_whitespace(strip_tags(content_html))
            if content_text and content_text != prev_heading:
                sections.append({
                    "heading": prev_heading,
                    "content": content_text
                })

        prev_heading = heading_text
        prev_end = start

    if prev_heading is not None and prev_end is not None:
        content_html = main_html[prev_end:]
        content_text = clean_whitespace(strip_tags(content_html))
        if content_text and content_text != prev_heading:
            sections.append({
                "heading": prev_heading,
                "content": content_text
            })

    return sections


def extract_all_text(html):
    """Extract all visible text from the page body."""
    main_m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if not main_m:
        return ''
    text = strip_tags(main_m.group(1))
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_agent_name(html):
    h1 = re.search(r'<h1>(.*?)</h1>', html)
    return h1.group(1).strip() if h1 else ''


def extract_verdict(html):
    m = re.search(r'<span class="verdict-badge">(.*?)</span>', html)
    return m.group(1).strip() if m else ''


def main():
    index = []

    for page in PAGES:
        filepath = os.path.join(ROOT, page["file"])
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found")
            continue

        with open(filepath) as f:
            html = f.read()

        title = extract_title(html)
        summary = extract_meta(html, 'description')
        sections = extract_sections(html)

        entry = {
            "url": page["url"],
            "title": title,
            "breadcrumb": page["breadcrumb"],
            "summary": summary,
        }

        # Add verdict as a tag for agent pages
        if page["url"].startswith("/agents/") and page["url"] != "/agents/":
            verdict = extract_verdict(html)
            if verdict:
                entry["tags"] = [verdict]

        if sections:
            entry["sections"] = sections

        index.append(entry)

    outpath = os.path.join(ROOT, "search-index.json")
    with open(outpath, 'w') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"Index written to {outpath}")
    print(f"Pages indexed: {len(index)}")
    total_sections = sum(len(e.get("sections", [])) for e in index)
    print(f"Total sections: {total_sections}")


if __name__ == "__main__":
    main()
