# Log

Newest at the bottom. One entry per change batch, with the commit where useful.

## [2026-10-07] rebuild
Framer portfolio converted to static HTML and pushed to `benluera/portfolio`, live at
benluera.github.io/portfolio. Outcome summaries, project nav, WebP images, favicon, Open Graph
tags, phone nav, responsive QA fixes (see git history before 2b1a81a).

## [2026-10-08] diagnosis
Portfolio read as designer and intern while the LinkedIn title said AI UX Researcher. Findings:
no text headline, HP absent, six specialties, intern-labelled links, MLLM page body in images,
inconsistent footers. Recorded in [[decisions]] and [[backlog]].

## [2026-10-08] reposition the home page (2b1a81a)
Hero relabelled Qualitative / Quantitative, text headline, meta descriptions, four specialties,
Related Links reordered and retitled, footers unified, MLLM prose, new share image. Four QA passes.

## [2026-10-08] slider handle (d8f2844, 8e9402c, 3a4d2b3, a97d4ba)
Handle moved off the face with arrows. Demo swing and "Drag" pill added, then removed at the
human's request. Final: arrows only, no animation.

## [2026-10-08] role in the hero (5f46389)
"AI UX Researcher" painted across the top of both layers; headline became the name; first attempt
clipped under the nav, moved from y 38 to y 60. Share image rebuilt.

## [2026-10-08] share image caption and cache-busting (0baab25)
Caption restored to "AI UX Researcher | HP, Adobe Research, Amazon Fire TV". `og.jpg?v=2` on all
pages so previews refresh.

## [2026-10-08] hero-overlay branch (72dbe5e, then merges)
Poster-style hero experiment built on a branch at the human's request. Unmerged.

## [2026-10-08] project highlights rows (0b94d42)
Second row container was 730px at tablet widths versus 1000px for the first; cards shrank. Both
rows now 1000px and centred. Verified identical widths at 900, 1000, 1180, 1400.

## [2026-10-08] move to reubenluera.github.io (c6f6ba8)
Org created, repo imported and renamed, Pages on. Absolute URLs updated on all pages and README.
Old repo replaced with redirect pages (`benluera/portfolio` 10f24a4). Local remote repointed.

## [2026-10-08] phone nav links (d6b2912)
Resume and LinkedIn in the phone nav inherited dark grey; forced white.

## [2026-10-08] LinkedIn review
Full profile read and audited. Items in [[linkedin-review-2026-10-08]].

## [2026-10-10] wiki and tools
`CLAUDE.md`, `wiki/`, generator and QA scripts moved from the agent's scratchpad into `tools/`,
preview config added, so the project can be picked up from any machine. LinkedIn checklist (13
items) ingested into [[linkedin-review-2026-10-08]] from the human's saved HTML checklist.

## [2026-10-10] no cropped figures at any width
Human reported case study images clipped top and bottom when the window narrows. Cause: Framer
figures are background images with `cover` in boxes whose per-breakpoint shape does not match the
image. Added `tools/fix_figures.py` and the generated `assets/figures.css` (85 figures, per media
block, width- and height-driven handled). Audited all six case study pages at 375, 1000 and 1280:
zero clipped, zero collapsed. Three iterations were needed: Framer's own `aspect-ratio` values
were not trustworthy (1:1 boxes on 766 by 929 images), column flex items with `flex-basis: 0`
collapsed until `flex-basis: auto`, and height-driven filmstrip and slideshow boxes collapsed
until width was left alone.

## [2026-10-11] Google Analytics
GA4 tag (G-T4V0NG46T8, stream "GH Portfolio") added right after `<head>` on all seven pages. No visual change. Load-checked every page at 1280 and 375.

## [2026-10-17] Copy fixes and new resume
MLLM: the four-themes figure caption said 8 designers; repainted as `mllm-themes-10-designers.webp` by `tools/fig_themes_caption.py` (source image untouched). Study Scale card and "What happened" now split qual (10 designers, 30 interfaces) from quant (500 raters per design, 15,000 responses). Stasis: tools are Figma only. AI on Fire TV Search: "(video below)" is now "(video attached)". Resume links on all seven pages point to `assets/Reuben_Luera_Resume.pdf` (the 2-page resume with the phone number removed from the PDF text) instead of the old Google Drive file.

## [2026-10-17] Google Scholar in the top nav
"Google Scholar" (https://scholar.google.com/citations?user=Ov2HGFQAAAAJ) added after LinkedIn in the desktop and tablet nav on all seven pages, and as "Scholar" in the phone nav. Phone nav now shrinks the wordmark and links at 420px and 360px so three links fit. Fixed an older bug: on the five case studies with the white phone header (variant JL91ug0ci) the phone nav links were white on white; they are now navy. base.css bumped to nv2.
