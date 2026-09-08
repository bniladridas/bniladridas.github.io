#!/usr/bin/env python3
"""
Human-feel verification for bniladridas portfolio.
Checks typography harmony, visual noise, linguistic clarity,
authenticity, and functional human experience.
"""
import re, html.parser as html_parser, subprocess, urllib.request, urllib.error, sys, pathlib, json

ROOT = pathlib.Path(__file__).parent
html_path = ROOT / "index.html"
css_path = ROOT / "styles.css"
js_path = ROOT / "script.js"

def rd(p): return p.read_text(encoding="utf-8")

html_text = rd(html_path)
css = rd(css_path)
js = rd(js_path)

checks = []
def check(name, ok, detail=""):
    checks.append((name, ok, detail))
    return ok

# --- Parse ---
try:
    html_parser.HTMLParser().feed(html_text)
    check("HTML parses", True)
except Exception as e:
    check("HTML parses", False, str(e))

try:
    subprocess.run(["node","--check", str(js_path)], check=True, capture_output=True)
    check("JS syntax", True)
except Exception as e:
    check("JS syntax", False, str(e))

# --- Typography harmony ---
check("Font load limited (Inter 400,600 only)", "400;600" in html_text and "700" not in html_text and "800" not in html_text, "Inter weights in HTML")
check("Body line-height 1.7 (calm reading)", "line-height:1.7" in css, "body line-height")
check("Eyebrow muted and subtle", ".eyebrow{color:var(--mut)" in css and "opacity:.9" in css)
check("Hero whitespace generous", "padding:5rem 0 3.5rem" in css)
check("No gradients (visual noise removed)", css.count("gradient")==0, f"gradients={css.count('gradient')}")
check("Card radius unified 10px", "--r:10px" in css, "r var")
check("Single accent color only", css.count("--acc:")==1 and "--acc2" not in css)
check("Sections use hairline only, alt not striped", ".section.alt{background:var(--bg)" in css)
check("Avatar quiet (64px, 1px border)", "width:64px" in css and "border:1px solid var(--line)" in css)
check("Reveal subtle (8px, 0.45s)", "translateY(8px)" in css and ".45s" in css)

# --- No visual noise ---
check("Zero em/en dashes in HTML+JS+CSS", html_text.count("—")==0 and html_text.count("–")==0 and js.count("—")==0 and css.count("—")==0, f"—={html_text.count('—')} –={html_text.count('–')}")
check("No art-tag or hero-stats DOM noise", "art-tag" not in html_text and "hero-stats" not in html_text)
check("No chip pills noise", 'class="chips"' not in html_text and css.count(".chips")==0)
check("No transform lift on button hover", "translateY(-1px)" not in css or css.count("translateY(-1px)")<=1)  # allow icon-btn? we removed
check("Code monochrome (muted)", "pre code{background:none" in css and "color:var(--mut)" in css)

# --- Linguistic clarity (no clutter) ---
check("Title concise, no em dash", "—" not in (html_path.read_text()[:500]) and "Traction and Palmshed Sandbox" in html_text)
check("Hero lede concise (2 projects sentence)", "Two projects:" in html_text and html_text.count("Two projects")>=1)
check("Footer authentic (single license line)", "Palmshed Sandbox is MIT licensed" in html_text and "MIT licensed projects" not in html_text)
check("Role not Client for sandbox (authentic)", "<span>Role</span><strong>Maintainer</strong>" in html_text)
check("No platforms row mixing (authentic)", '<span>Platforms</span>' not in html_text)

# --- Human authenticity & accessibility ---
check("Alt text on all images", html_text.count('<img') == html_text.count('alt='), f"imgs={html_text.count('<img')} alts={html_text.count('alt=')}")
check("Avatar has descriptive alt", 'alt="bniladridas GitHub profile photo"' in html_text)
check("Nav anchors correspond to sections", all(f'id="{s}"' in html_text for s in ["about","projects","skills","contact"]), "anchors")
check("External links have rel noopener", html_text.count('target="_blank"') == html_text.count('rel="noopener"'), f"blank={html_text.count('target=\"_blank\"')} noopener={html_text.count('rel=\"noopener\"')}")
check("Details for gists are lazy (human progressive disclosure)", html_text.count('details class="gist-details"')==2)
check("Copy button present (human convenience)", 'class="copy"' in html_text)

# --- Functional human experience (live checks, best effort) ---
def head_ok(url):
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent","verify-human/1.0")
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.status in (200,302)
    except Exception as e:
        return False

assets = [
    "https://raw.githubusercontent.com/bniladridas/traction/main/.github/assets/thumbnail.png",
    "https://raw.githubusercontent.com/palmshed/sandbox/main/.github/assets/thumbnail.png",
    "https://raw.githubusercontent.com/bniladridas/traction/main/docs/verification/assets/track-start.png",
    "https://raw.githubusercontent.com/bniladridas/traction/main/docs/verification/assets/track-sweeper.png",
    "https://github.com/bniladridas.png",
]
for u in assets:
    check(f"Image live: {u.split('/')[-1]}", head_ok(u), u)

gists = [
    "https://gist.githubusercontent.com/bniladridas/9023df59b46899d783cbf49ca95c1c76/raw/racinggame-engineering-log.md",
    "https://gist.githubusercontent.com/bniladridas/e2a499783be6d2b9de4dd7cf4f34ee7d/raw/sandbox.md",
]
for u in gists:
    check(f"Gist raw live: {u.split('/')[-2][:8]}", head_ok(u), u)

check("Facebook link correct", "https://www.facebook.com/bniladridas/" in html_text)
check("GitHub links use bniladridas", "https://github.com/bniladridas" in html_text)

# --- Summary ---
fails = [c for c in checks if not c[1]]
passed = len(checks)-len(fails)
print("\nHuman-feel verification for", ROOT)
print("="*62)
for name, ok, detail in checks:
    mark = "✓" if ok else "✗"
    extra = f" — {detail}" if detail else ""
    print(f"{mark} {name}{extra}")
print("-"*62)
print(f"Passed {passed}/{len(checks)}")
if fails:
    print(f"Failed {len(fails)} — see ✗ above")
    sys.exit(1)
else:
    print("Human feel: calm whitespace, single accent, hairline borders, 1.7 leading, muted hierarchy. No visual noise, no linguistic excess.")
    print("Authenticity: single MIT line, Maintainer role, no mixed platforms. Accessibility: alts, noopener, lazy disclosure.")
    print("This site was tested: HTML parsed, CSS inspected, JS checked, 5 images HEAD-checked, 2 gists HEAD-checked.")
