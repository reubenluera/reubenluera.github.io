# Deploy and hosting

## Where it lives

| | |
|---|---|
| Site | https://reubenluera.github.io/ |
| Repo | https://github.com/reubenluera/reubenluera.github.io |
| Owner | GitHub organization `reubenluera`, created 2026-10-08 from the `benluera` personal account |
| Pages source | branch `main`, root folder, HTTPS enforced |
| Deploy time | 10 to 70 seconds after push |

The repo is named exactly `<owner>.github.io`, which is what makes GitHub serve it at the root
instead of under a path. The org route was chosen over renaming the `benluera` account because
Pages URLs do not redirect on an account rename and that account hosts live UserTesting stimulus
sites for HP studies.

## The old address

https://benluera.github.io/portfolio/ was the home from 2026-10-07 to 2026-10-08. The repo
`benluera/portfolio` now contains only `index.html`, `404.html` and a README. Both pages redirect
with a meta refresh and a script that rewrites the path, so `/portfolio/mllmjudge/` lands on
`/mllmjudge/` at the new address. GitHub serves `404.html` for unknown paths, which is how deep
links keep working. The old repo is attached to the local clone as remote `old`; do not push
site content there.

## Share previews

All seven pages carry `og:url`, `og:image` (1200 by 630), `twitter:card` and `twitter:image`
pointing at `assets/og.jpg?v=N` on the new domain. LinkedIn, Slack and iMessage cache by URL, so
a new image needs a new `?v=`. LinkedIn also wants a manual refresh at
https://www.linkedin.com/post-inspector/ for any URL it has already seen.

## Branches

- `main`: live.
- `hero-overlay`: poster-style hero experiment (name and companies overlaid on the slider with a
  gradient, headline block replaced by a lead paragraph, handle moved to the chest line). Built
  2026-10-08 at the human's request to evaluate, explicitly not committed to. Kept merged with
  main; version-string conflicts in the page heads resolve by keeping the branch's markup and
  bumping its own `base.css?v=hoN`.

## Remotes on the original laptop

```
origin  https://github.com/reubenluera/reubenluera.github.io.git
old     https://github.com/benluera/portfolio.git
```

A fresh clone only needs `origin`.
