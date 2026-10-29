# STATUS

## What was built

Free Chess Study Kit — a fan project by Asdale Dynamics, LLC. Four printable,
large-print-friendly chess study sheets, each as Markdown source and as a
self-contained print-ready HTML file:

- `kit/opening-repertoire.md` + `.html` — White and Black opening repertoire planner, key variations, traps, principles checklist
- `kit/tactics-log.md` + `.html` — Log tactics by motif (fork, pin, skewer, discovered attack, double check, deflection, decoy, overloading, interference, X-ray) with result and notes
- `kit/game-analysis-template.md` + `.html` — Game info, opening review, move-by-move critical moments, turning point, lessons, homework
- `kit/endgame-checklist.md` + `.html` — King and pawn, rook (Lucena, Philidor), minor piece endgames, basic checkmates, stalemate traps, pre-resign/draw checks

Shared print CSS (`kit/styles.css`) inlined into every HTML sheet: 15px body
type (~large print), 46px table rows for writing space, checkboxes, page
numbers in the footer, Letter-size @page margins. `kit/build.py` (standard
library only) regenerates all HTML from Markdown. No account, no signup, no
network, no fonts to install, no secrets or personal data anywhere.

## How to run

```bash
# Clone/copy this folder, then:
python3 kit/build.py
```

This writes `kit/*.html` next to the Markdown sources. Open any `.html` in a
browser and print (`Ctrl+P` / `Cmd+P`) at 100% with background graphics
enabled. The Markdown files are plain text and can be copied into any notes
app.

## Verification results

- `python3 kit/build.py` — ran clean, wrote all 4 HTML files
- HTML structure check (html.parser) — all 4 files: no unclosed/mismatched tags, charset meta present, embedded CSS present
- Content check — each sheet contains its expected title, sections, motifs, and checkboxes (10, 10, 9, 27 checkboxes respectively)
- LICENSE — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`
- README — credits Asdale Dynamics, LLC

## Known gaps

- No automated test suite; verification above is a one-off script run manually
- HTML is not passed through an external CSS/HTML validator
- Print appearance depends on the browser/printer; @page rules are standard but not universally honored
- Sheets are US Letter sized
