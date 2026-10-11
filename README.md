# Reuben Luera Portfolio

Live at https://reubenluera.github.io/ (GitHub Pages, branch `main`, root).

Static site: `index.html` plus one folder per case study (`mllmjudge/`, `aiftv-2/`, `optimizing/`,
`aiftv/`, `survey/`, `stasis/`). Shared styles in `assets/base.css`, generated figure sizing in
`assets/figures.css`, the small amount of JS in `assets/site.js`. Fonts load from Google Fonts.

Start here:

- `CLAUDE.md` is the contract for the agent that maintains the site: rules, workflows, pitfalls.
- `wiki/index.md` is the knowledge base entry point (structure, hero pipeline, QA, deploy,
  decisions, backlog, log). The `wiki/` folder opens as an Obsidian vault.
- `tools/` holds the generators and QA helpers. Python 3 with Pillow and NumPy.

Serve locally with any static server, e.g. `python -m http.server 8765`, or use the `portfolio`
entry in `.claude/launch.json`.
