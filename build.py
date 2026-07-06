#!/usr/bin/env python3
"""Build: generate all derived artifacts from canonical sources.

Reads data.js (handwritten org data) and agent HTML pages, then generates:
  - agents.js      — merged runtime data (id, name, status, developer, version, dates, path, order)
  - search-index.json  — full-text search index
  - rss.xml             — RSS 2.0 feed
  - sitemap.xml         — XML sitemap

Usage: python3 build.py
"""

import os
import re
import json
import datetime
from email.utils import formatdate

ROOT = os.path.dirname(os.path.abspath(__file__))

MONTH_MAP = {
    'January': '01', 'February': '02', 'March': '03', 'April': '04',
    'May': '05', 'June': '06', 'July': '07', 'August': '08',
    'September': '09', 'October': '10', 'November': '11', 'December': '12',
}

STATUS_PRIORITY = {'Active': 0, 'Occasional': 1, 'Archived': 2}
SITEMAP_PRIORITY = {'Active': '0.7', 'Occasional': '0.6', 'Archived': '0.5'}

# ── HTML helpers ──────────────────────────────────────────────────────────

def extract_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    return m.group(1).strip() if m else ''


def extract_meta(html, name):
    m = re.search(
        rf'<meta\s+name=["\']{name}["\']\s+content=(["\'])(.*?)\1',
        html, re.IGNORECASE | re.DOTALL
    )
    if m:
        return m.group(2).strip()
    m = re.search(
        rf'<meta\s+content=(["\'])(.*?)\1\s+name=["\']{name}["\']',
        html, re.IGNORECASE | re.DOTALL
    )
    return m.group(2).strip() if m else ''


def strip_tags(text):
    return re.sub(r'<[^>]+>', '', text)


def clean_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()


def extract_dl_field(html, field_name):
    """Extract a <dd> value from a definition list by <dt> field name."""
    m = re.search(
        r'<dt>\s*' + re.escape(field_name) + r'\s*</dt>\s*<dd>(.*?)</dd>',
        html, re.IGNORECASE | re.DOTALL
    )
    return clean_whitespace(strip_tags(m.group(1))) if m else ''


def parse_date_to_ym(text):
    """Convert 'July 2026' → '2026-07'."""
    m = re.match(r'(\w+)\s+(\d{4})', text.strip())
    if m:
        month = MONTH_MAP.get(m.group(1), '01')
        return f"{m.group(2)}-{month}"
    return text.strip()


def month_year_to_rfc2822(text):
    """Convert 'July 2026' → RFC 2822 date string."""
    m = re.match(r'(\w+)\s+(\d{4})', text.strip())
    if not m:
        return ''
    month = MONTH_MAP.get(m.group(1), 1)
    year = int(m.group(2))
    month_num = int(month)
    dt = datetime.date(year, month_num, 1)
    return formatdate(timeval=(dt - datetime.date(1970, 1, 1)).total_seconds(), localtime=False, usegmt=True)


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


def extract_agent_name(html):
    h1 = re.search(r'<h1>(.*?)</h1>', html)
    return h1.group(1).strip() if h1 else ''


# ── Org data parsing ─────────────────────────────────────────────────────

def parse_org_data():
    """Read handwritten data.js and return list of agent org dicts."""
    path = os.path.join(ROOT, 'data.js')
    with open(path) as f:
        content = f.read()
    m = re.search(r'var\s+agentOrg\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not m:
        print("Error: could not find agentOrg in data.js")
        return []
    array_text = m.group(1)

    agents = []
    obj_pattern = re.compile(r'\{\s*(.*?)\s*\}', re.DOTALL)
    for obj_match in obj_pattern.finditer(array_text):
        obj_text = obj_match.group(1)
        fields = {}
        for kv in re.finditer(r"(\w+)\s*:\s*(?:'([^']*)'|(\d+))", obj_text):
            key = kv.group(1)
            val = kv.group(2) if kv.group(2) is not None else int(kv.group(3))
            fields[key] = val
        if 'id' in fields:
            agents.append(fields)
    return agents


# ── Agent metadata extraction ────────────────────────────────────────────

def extract_agent_meta(html):
    """Extract review metadata from agent HTML."""
    name = extract_agent_name(html)
    developer = extract_dl_field(html, 'Developer')

    # version reviewed (field name may vary in case)
    version_reviewed = extract_dl_field(html, 'Version Reviewed')
    if not version_reviewed:
        version_reviewed = extract_dl_field(html, 'Version reviewed')

    # last updated (differs between templates)
    last_reviewed = extract_dl_field(html, 'Last reviewed')
    if last_reviewed:
        last_updated = parse_date_to_ym(last_reviewed)
    else:
        last_updated_text = extract_dl_field(html, 'Last Updated')
        last_updated = parse_date_to_ym(last_updated_text) if last_updated_text else ''

    return {
        'name': name,
        'developer': developer,
        'versionReviewed': version_reviewed,
        'lastUpdated': last_updated,
    }


def scan_agent_dirs():
    """Return list of agent IDs from filesystem."""
    agents_path = os.path.join(ROOT, 'agents')
    return sorted([
        d for d in os.listdir(agents_path)
        if os.path.isdir(os.path.join(agents_path, d))
        and os.path.exists(os.path.join(agents_path, d, 'index.html'))
    ])


# ── Generators ───────────────────────────────────────────────────────────

def build_agents():
    """Merge org data with extracted HTML metadata → list of merged dicts."""

    org_map = {a['id']: a for a in parse_org_data()}
    agent_ids = scan_agent_dirs()

    merged = []
    seen = set()

    for aid in agent_ids:
        filepath = os.path.join(ROOT, 'agents', aid, 'index.html')
        with open(filepath) as f:
            html = f.read()

        meta = extract_agent_meta(html)
        org = org_map.get(aid, {})

        merged.append({
            'id': aid,
            'name': meta['name'] or aid.replace('-', ' ').title(),
            'status': org.get('status', 'Archived'),
            'developer': meta['developer'] or '',
            'versionReviewed': meta['versionReviewed'] or '',
            'lastUpdated': meta['lastUpdated'] or '',
            'addedDate': org.get('addedDate', ''),
            'path': f"/agents/{aid}/",
            'order': org.get('order', 99),
        })
        seen.add(aid)

    # sort by status group then order
    def sort_key(a):
        return (STATUS_PRIORITY.get(a['status'], 99), a['order'])

    merged.sort(key=sort_key)
    return merged


def generate_search_index(all_pages, agents_data):
    """Build search-index.json from page HTML files."""
    index = []

    for page in all_pages:
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

        if sections:
            entry["sections"] = sections

        index.append(entry)

    # agent pages (extracted from generated agents_data)
    for a in agents_data:
        filepath = os.path.join(ROOT, 'agents', a['id'], 'index.html')
        if not os.path.exists(filepath):
            continue

        with open(filepath) as f:
            html = f.read()

        title = extract_title(html)
        summary = extract_meta(html, 'description')
        sections = extract_sections(html)

        entry = {
            "url": a['path'],
            "title": title,
            "breadcrumb": f"Agents / {a['name']}",
            "summary": summary,
        }

        if sections:
            entry["sections"] = sections

        index.append(entry)

    outpath = os.path.join(ROOT, "search-index.json")
    with open(outpath, 'w') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"  search-index.json: {len(index)} pages, "
          f"{sum(len(e.get('sections', [])) for e in index)} sections")


def generate_rss(agents_data):
    """Generate rss.xml from agent metadata."""
    site_url = "https://bniladridas.github.io"

    items = []
    for a in agents_data:
        filepath = os.path.join(ROOT, 'agents', a['id'], 'index.html')
        if not os.path.exists(filepath):
            continue
        with open(filepath) as f:
            html = f.read()

        description = extract_meta(html, 'description')
        title = f"{a['name']} review"
        link = f"{site_url}{a['path']}"
        pub_date = month_year_to_rfc2822(
            extract_dl_field(html, 'Reviewed') or
            extract_dl_field(html, 'Last Updated')
        )

        items.append({
            'title': title,
            'link': link,
            'description': description,
            'pubDate': pub_date,
            'guid': link,
        })

    # sort by pubDate descending
    items.sort(key=lambda x: x['pubDate'], reverse=True)

    now = formatdate(localtime=False, usegmt=True)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        '    <title>Palmshed</title>',
        f'    <link>{site_url}/</link>',
        '    <description>Thoughtful engineering, honest evaluation, and enduring craft.</description>',
        '    <language>en</language>',
        f'    <lastBuildDate>{now}</lastBuildDate>',
        f'    <atom:link href="{site_url}/rss.xml" rel="self" type="application/rss+xml"/>',
    ]
    for item in items:
        lines.extend([
            '    <item>',
            f'      <title>{item["title"]}</title>',
            f'      <link>{item["link"]}</link>',
            f'      <description>{item["description"]}</description>',
            f'      <pubDate>{item["pubDate"]}</pubDate>',
            f'      <guid>{item["guid"]}</guid>',
            '    </item>',
        ])
    lines.extend([
        '  </channel>',
        '</rss>',
    ])

    outpath = os.path.join(ROOT, 'rss.xml')
    with open(outpath, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"  rss.xml: {len(items)} items")


def generate_sitemap(agents_data):
    """Generate sitemap.xml."""
    site_url = "https://bniladridas.github.io"

    static_pages = [
        ('/', 'weekly', '1.0'),
        ('/agents/', 'weekly', '0.8'),
        ('/methodology/', 'monthly', '0.7'),
        ('/about/', 'monthly', '0.7'),
        ('/ethos/', 'monthly', '0.7'),
        ('/privacy/', 'monthly', '0.3'),
        ('/search/', 'monthly', '0.2'),
        ('/auth/', 'monthly', '0.3'),
        ('/auth/callback/', 'monthly', '0.1'),
    ]

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for loc, freq, priority in static_pages:
        lines.extend([
            '  <url>',
            f'    <loc>{site_url}{loc}</loc>',
            f'    <changefreq>{freq}</changefreq>',
            f'    <priority>{priority}</priority>',
            '  </url>',
        ])

    for a in agents_data:
        priority = SITEMAP_PRIORITY.get(a['status'], '0.5')
        lines.extend([
            '  <url>',
            f'    <loc>{site_url}{a["path"]}</loc>',
            '    <changefreq>monthly</changefreq>',
            f'    <priority>{priority}</priority>',
            '  </url>',
        ])

    lines.append('</urlset>')

    outpath = os.path.join(ROOT, 'sitemap.xml')
    with open(outpath, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"  sitemap.xml: {len(static_pages) + len(agents_data)} URLs")


def generate_agents_js(agents_data):
    """Generate agents.js — merged runtime data."""
    lines = [
        '// Generated by build.py. Do not edit.',
        'var agents = [',
    ]
    for i, a in enumerate(agents_data):
        comma = ',' if i < len(agents_data) - 1 else ''
        lines.append(f"  {{")
        lines.append(f'    id: {json.dumps(a["id"])},')
        lines.append(f'    name: {json.dumps(a["name"])},')
        lines.append(f'    status: {json.dumps(a["status"])},')
        lines.append(f'    developer: {json.dumps(a["developer"])},')
        lines.append(f'    versionReviewed: {json.dumps(a["versionReviewed"])},')
        lines.append(f'    lastUpdated: {json.dumps(a["lastUpdated"])},')
        lines.append(f'    addedDate: {json.dumps(a["addedDate"])},')
        lines.append(f'    path: {json.dumps(a["path"])},')
        lines.append(f'    order: {a["order"]}')
        lines.append(f"  }}{comma}")
    lines.append('];')
    lines.append('')

    outpath = os.path.join(ROOT, 'agents.js')
    with open(outpath, 'w') as f:
        f.write('\n'.join(lines))
    print(f"  agents.js: {len(agents_data)} agents")


# ── Non-agent pages for search index ─────────────────────────────────────

PAGES = [
    {"url": "/", "file": "index.html", "breadcrumb": "Home"},
    {"url": "/about/", "file": "about/index.html", "breadcrumb": "About"},
    {"url": "/ethos/", "file": "ethos/index.html", "breadcrumb": "Ethos"},
    {"url": "/methodology/", "file": "methodology/index.html", "breadcrumb": "Methodology"},
    {"url": "/agents/", "file": "agents/index.html", "breadcrumb": "Agents"},
    {"url": "/auth/", "file": "auth/index.html", "breadcrumb": "Sign in"},
    {"url": "/search/", "file": "search/index.html", "breadcrumb": "Search"},
]

# ── Main ─────────────────────────────────────────────────────────────────

def main():
    print("Build started\n")

    print("1. Merging agent data...")
    agents_data = build_agents()
    print(f"   {len(agents_data)} agents processed\n")

    print("2. Generating search index...")
    generate_search_index(PAGES, agents_data)
    print()

    print("3. Generating RSS feed...")
    generate_rss(agents_data)
    print()

    print("4. Generating sitemap...")
    generate_sitemap(agents_data)
    print()

    print("5. Generating agents.js...")
    generate_agents_js(agents_data)
    print()

    print("Build complete.")


if __name__ == "__main__":
    main()
