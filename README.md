# Free Chess Study Kit

A free, printable, large-print-friendly chess study kit for beginners and
club players. No account, no signup, no tracking — just print and play.

This is a fan project by **Asdale Dynamics, LLC** (Indiana, formed October
2026), the company behind Dylan Asdale's *The Massive AI Manual* and the hub
site dylanasdale.github.io. Asdale Dynamics makes beginner-friendly AI
education, books, guides, and practical tools — plus fun extras like chess
tools. Everything here is education-only and never medical advice.

## What's inside

| Sheet | What it's for |
|-------|---------------|
| `kit/opening-repertoire.md` / `.html` | One-page opening repertoire planner: your White and Black repertoire, key lines, and notes |
| `kit/tactics-log.md` / `.html` | Log tactical motifs you spot (fork, pin, skewer, etc.) with date, result, and notes |
| `kit/game-analysis-template.md` / `.html` | Step-by-step template for analyzing your own games after you play them |
| `kit/endgame-checklist.md` / `.html` | Endgame fundamentals checklist: king activity, opposition, pawn races, and common mating patterns |

Each sheet exists as **Markdown** (easy to copy/edit) and as **print-ready HTML**
(formatted for large-print, high-contrast printing).

## Quick start

```bash
# 1. Clone or download this folder
# 2. Build the printable HTML sheets
python3 kit/build.py

# 3. Open any .html file in your browser and print (Ctrl+P / Cmd+P)
#    For best results: 100% scale, background graphics ON, margins: default
```

**No Python?** Just open the `.html` files directly in your browser — they're
already built and self-contained (CSS is inlined).

## Print tips for best results

- **Paper size**: Sheets use US Letter by default. For A4, edit `kit/styles.css`
  and change `@page { size: Letter; }` to `@page { size: A4; }`.
- **Large print**: Body text is 15px (~14pt) with 1.8 line height — designed
  for readability at arm's length.
- **Writing space**: Table rows have 46px minimum height so you can write in
  them after printing.
- **Checkboxes**: Render as printable square boxes (22×22px) with space to tick.
- **Background graphics**: Enable "Background graphics" in your print dialog so
  table borders and checkboxes print correctly.
- **Double-sided**: Sheets are designed to work well printed double-sided.

## File structure

```
free-chess-study-kit/
├── LICENSE                    # MIT License
├── README.md                  # This file
├── STATUS.md                  # Build/verification status
├── kit/
│   ├── build.py               # Markdown → HTML generator (stdlib only)
│   ├── styles.css             # Print stylesheet (inlined into HTML)
│   ├── opening-repertoire.md  # Source
│   ├── opening-repertoire.html
│   ├── tactics-log.md
│   ├── tactics-log.html
│   ├── game-analysis-template.md
│   ├── game-analysis-template.html
│   ├── endgame-checklist.md
│   └── endgame-checklist.html
```

## Rebuild the HTML

```bash
python3 kit/build.py
```

Requires only **Python 3** — no external packages, no account, no network.
The script reads each `.md` file, converts basic Markdown to HTML, inlines
`styles.css`, and writes a standalone `.html` file.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## Credit

Created and published by **Asdale Dynamics, LLC**. Fan project — not
affiliated with any chess organization.

## Accessibility

- High contrast (black on white)
- Large default font size (15px)
- Semantic HTML structure (headings, lists, tables)
- Checkboxes use native `<input type="checkbox">` for screen readers
- No JavaScript, no animations, no tracking