#!/usr/bin/env python3
"""One-shot migration: LockAid → LockDirect + swap SVG brand mark for PNG logo."""

import re
from pathlib import Path

ROOT = Path(__file__).parent

SVG_BLOCK = re.compile(
    r'<div class="brand__mark">\s*'
    r'<svg viewBox="0 0 24 24"[^>]*>'
    r'<circle cx="7" cy="14" r="5"/><path d="M11 14L20 5l-3-3"/><path d="M16 9l-3-3"/>'
    r'</svg>\s*</div>',
    re.DOTALL,
)
NAME_SPAN = re.compile(r'\s*<span class="brand__name">[^<]*</span>')

CSS_MARK_INLINE = re.compile(
    r'\.brand__mark \{ width: 44px; height: 44px; border-radius: 12px; '
    r'background: linear-gradient\(135deg, var\(--red\), var\(--red-bright\)\); '
    r'display: grid; place-items: center; color: white; '
    r'box-shadow: 0 6px 18px rgba\(225,29,42,0\.35\); \}'
)
CSS_MARK_SVG_INLINE = re.compile(r'\.brand__mark svg \{ width: 22px; height: 22px; \}')

CSS_MARK_MULTILINE = re.compile(
    r'\.brand__mark \{\s*'
    r'width: 44px;\s*'
    r'height: 44px;\s*'
    r'border-radius: 12px;\s*'
    r'background: linear-gradient\(135deg, var\(--red\) 0%, var\(--red-bright\) 100%\);\s*'
    r'display: grid;\s*'
    r'place-items: center;\s*'
    r'color: white;\s*'
    r'box-shadow: 0 6px 18px rgba\(225, 29, 42, 0\.35\);\s*'
    r'position: relative;\s*\}'
)
CSS_MARK_SVG_MULTILINE = re.compile(
    r'\.brand__mark svg \{ width: 22px; height: 22px; \}'
)


def rel_prefix(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    depth = len(parts) - 1
    return "../" * depth


def migrate(text: str, rel: str) -> str:
    img = (
        f'<img src="{rel}assets/lockdirect-logo.png" '
        f'alt="LockDirect" class="brand__logo">'
    )
    text = SVG_BLOCK.sub(img, text)
    text = NAME_SPAN.sub("", text)

    # Brand renaming
    text = text.replace("LockAid", "LockDirect")
    text = text.replace("lockaid", "lockdirect")

    # CSS rewrites — drop old .brand__mark rules, introduce .brand__logo sizing
    new_logo_rule = ".brand__logo { height: 44px; width: auto; display: block; }"
    text = CSS_MARK_INLINE.sub(new_logo_rule, text)
    text = CSS_MARK_SVG_INLINE.sub("", text)

    new_logo_rule_multi = (
        ".brand__logo {\n  height: 44px;\n  width: auto;\n  display: block;\n}"
    )
    text = CSS_MARK_MULTILINE.sub(new_logo_rule_multi, text)
    text = CSS_MARK_SVG_MULTILINE.sub("", text)

    return text


for html in sorted(ROOT.rglob("*.html")):
    if "assets" in html.parts:
        continue
    original = html.read_text(encoding="utf-8")
    updated = migrate(original, rel_prefix(html))
    if updated != original:
        html.write_text(updated, encoding="utf-8")
        print(f"✓ {html.relative_to(ROOT)}")
    else:
        print(f"·  {html.relative_to(ROOT)} (no change)")

# Update the area-page generator so future runs use the new brand
gen = ROOT / "_generate_areas.py"
gen_text = gen.read_text(encoding="utf-8")
gen_updated = migrate(gen_text, "../")
if gen_updated != gen_text:
    gen.write_text(gen_updated, encoding="utf-8")
    print(f"✓ {gen.name}")

print("\nRebrand complete.")
