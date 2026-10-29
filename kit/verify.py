#!/usr/bin/env python3
"""Verification suite for the Free Chess Study Kit.

Checks:
  1. build.py runs without errors and produces 4 HTML files
  2. Each HTML file is well-formed (no unclosed/mismatched tags)
  3. Each HTML file contains its expected title, sections, and checkboxes
  4. The Markdown sources contain the expected structure (tables, checkboxes)
  5. LICENSE has the exact copyright line
  6. README credits Asdale Dynamics, LLC

Run: python3 kit/verify.py
Exits 0 on success, non-zero on failure.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT = Path(__file__).resolve().parent

SHEETS = ["opening-repertoire", "tactics-log", "game-analysis-template", "endgame-checklist"]

EXPECTED = {
    "opening-repertoire": {
        "title": "Opening Repertoire Sheet",
        "sections": ["As White", "As Black", "vs 1. e4", "vs 1. d4"],
        "checkboxes_min": 8,
    },
    "tactics-log": {
        "title": "Tactics Log",
        "sections": ["Fork", "Pin", "Skewer", "X-ray"],
        "checkboxes_min": 8,
    },
    "game-analysis-template": {
        "title": "Game Analysis Template",
        "sections": ["turning point", "Engine says"],
        "checkboxes_min": 8,
    },
    "endgame-checklist": {
        "title": "Endgame Checklist",
        "sections": ["Lucena", "Philidor", "stalemate"],
        "checkboxes_min": 20,
    },
}

LICENSE_COPYRIGHT = "Copyright (c) 2026 Asdale Dynamics, LLC"

failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    if cond:
        print(f"  PASS {msg}")
    else:
        print(f"  FAIL {msg}")
        failures.append(msg)


class HTMLChecker(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.void = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                     "link", "meta", "param", "source", "track", "wbr"}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in self.void:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            self.errors.append(f"unexpected close </{tag}>")
        elif self.stack[-1] != tag:
            self.errors.append(f"mismatched: opened <{self.stack[-1]}>, closed </{tag}>")
            self.stack.pop()
        else:
            self.stack.pop()


def test_build() -> None:
    print("\n[1] Build")
    import subprocess
    result = subprocess.run(
        [sys.executable, str(KIT / "build.py")],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    check(result.returncode == 0, "build.py runs without errors")
    for name in SHEETS:
        path = KIT / f"{name}.html"
        check(path.exists(), f"{name}.html was generated")


def test_html_structure() -> None:
    print("\n[2] HTML structure")
    for name in SHEETS:
        text = (KIT / f"{name}.html").read_text(encoding="utf-8")
        checker = HTMLChecker()
        checker.feed(text)
        checker.close()
        problems = checker.errors + [f"unclosed: {t}" for t in checker.stack]
        check(not problems, f"{name}.html is well-formed ({len(problems)} problems)")
        check('charset="utf-8"' in text, f"{name}.html has charset meta")
        check("<style>" in text and "</style>" in text, f"{name}.html inlines CSS")


def test_html_content() -> None:
    print("\n[3] HTML content")
    for name, spec in EXPECTED.items():
        text = (KIT / f"{name}.html").read_text(encoding="utf-8")
        check(spec["title"] in text, f"{name}.html has title '{spec['title']}'")
        for section in spec["sections"]:
            check(section in text, f"{name}.html has section '{section}'")
        count = text.count("type='checkbox'")
        check(count >= spec["checkboxes_min"],
              f"{name}.html has >= {spec['checkboxes_min']} checkboxes (found {count})")


def test_markdown_sources() -> None:
    print("\n[4] Markdown sources")
    for name, spec in EXPECTED.items():
        text = (KIT / f"{name}.md").read_text(encoding="utf-8")
        check(spec["title"] in text, f"{name}.md has title '{spec['title']}'")
        check("- [ ]" in text, f"{name}.md has checkbox list")
        if name != "endgame-checklist":
            check("|" in text, f"{name}.md has table(s)")


def test_license() -> None:
    print("\n[5] License")
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    check(LICENSE_COPYRIGHT in license_text, "LICENSE has exact copyright line")
    check("MIT License" in license_text, "LICENSE is MIT")


def test_readme() -> None:
    print("\n[6] README")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("Asdale Dynamics, LLC" in readme, "README credits Asdale Dynamics, LLC")
    check("Free Chess Study Kit" in readme, "README names the project")
    check("python3 kit/build.py" in readme, "README documents build command")


def main() -> None:
    print(f"Verifying Free Chess Study Kit in {ROOT}")
    test_build()
    test_html_structure()
    test_html_content()
    test_markdown_sources()
    test_license()
    test_readme()

    print("\n" + ("ALL CHECKS PASSED" if not failures else f"{len(failures)} FAILURES"))
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()