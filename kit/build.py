#!/usr/bin/env python3
"""Build self-contained printable HTML sheets from Markdown sources.

Reads kit/*.md, writes kit/*.html. Each HTML inlines kit/styles.css so a
printed sheet needs only a printer: no fonts, no network, no account.
Standard library only.
"""

from __future__ import annotations

import re
from pathlib import Path

KIT = Path(__file__).resolve().parent
CSS = (KIT / "styles.css").read_text(encoding="utf-8")

SHEETS = [
    "opening-repertoire",
    "tactics-log",
    "game-analysis-template",
    "endgame-checklist",
]


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline(text: str) -> str:
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def is_separator(cells: list[str]) -> bool:
    return all(cell.strip() and set(cell.strip()) <= set("-: ") for cell in cells)


def convert(markdown: str) -> str:
    lines = markdown.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    in_list = False
    list_tag = ""
    table_rows: list[list[str]] = []
    in_table = False

    def flush_list() -> None:
        nonlocal in_list, list_tag
        if in_list:
            out.append(f"</{list_tag}>")
            in_list = False
            list_tag = ""

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if in_table and table_rows:
            out.append("<table>")
            for r_idx, row in enumerate(table_rows):
                tag = "th" if r_idx == 0 else "td"
                cells = "".join(f"<{tag}>{cell}</{tag}>" for cell in row)
                out.append(f"<tr>{cells}</tr>")
            out.append("</table>")
        in_table = False
        table_rows = []

    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        # Horizontal rule
        if re.fullmatch(r"-{3,}(?:\s+|$)", stripped):
            flush_list()
            flush_table()
            out.append("<hr>")
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if m:
            flush_list()
            flush_table()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # Table row
        if "|" in stripped and not stripped.startswith(" "):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if is_separator(cells):
                i += 1
                continue
            table_rows.append(cells)
            in_table = True
            i += 1
            continue

        flush_table()

        # Task list item
        m = re.match(r"^-\s+\[([xX ])\]\s+(.+)$", stripped)
        if m:
            if not in_list:
                out.append("<ul class='task'>")
                in_list = True
                list_tag = "ul"
            checked = "checked" if m.group(1) in "xX" else ""
            out.append(
                f"<li><input type='checkbox' disabled {checked}>"
                f" {inline(m.group(2))}</li>"
            )
            i += 1
            continue

        # Bullet list item
        m = re.match(r"^-\s+(.+)$", stripped)
        if m:
            if not in_list:
                out.append("<ul>")
                in_list = True
                list_tag = "ul"
            out.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue

        # Paragraph / blank line
        flush_list()
        if stripped == "":
            out.append("")
        else:
            out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    flush_list()
    flush_table()

    body = "\n".join(line for line in out if line != "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Free Chess Study Kit — Asdale Dynamics, LLC</title>
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>"""


def main() -> None:
    for name in SHEETS:
        md_path = KIT / f"{name}.md"
        html_path = KIT / f"{name}.html"
        markdown = md_path.read_text(encoding="utf-8")
        html_path.write_text(convert(markdown), encoding="utf-8")
        print(f"wrote {html_path}")


if __name__ == "__main__":
    main()
