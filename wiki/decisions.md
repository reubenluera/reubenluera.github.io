# Decisions

Why the site is the way it is. Each entry says what was decided, what was rejected, and who
decided. "Human" is Reuben; "agent" is Claude proposing. Newest first.

## 2026-10-08: hero carries the role, headline carries the name
Painted "AI UX RESEARCHER" centred at the top of both hero layers so the image reads as one
sentence: role, qualitative, quantitative. The `h1` under the hero became "Reuben Luera" and the
paragraph opens with "AI UX Researcher at HP." so the role is still real text and not stated twice
in a row. Human asked to try it, approved the result.

## 2026-10-08: no load-time swing, no hint pill, arrows only
The agent proposed a one-time left-right swing on load plus a "Drag" pill as affordance for the
slider, since a handle alone does not say "drag me". Human: the pill was fine but "Drag" was
enough, then that the arrows on the handle were enough on their own, then that the swing was not
needed either. Final state: a small circle with left and right arrows, no animation, no label.

## 2026-10-08: slider handle moved off the face
The Framer slider drew a 40px white disc at the vertical midpoint, which landed on the nose.
Moved to `bottom: 9%` (on the sweater) and shrunk to 34px. Alternatives listed for the human:
hollow ring, arrows only, no handle, handle at the top edge, hover-only, auto-sweep. Human took
the moved handle.

## 2026-10-08: Specialties cut from six to four
UX/UI Design, Visual and Graphic Design and Mentorship were removed. Contract UXR managers hire a
specialist; six specialties read as generalist or early-career. Kept UX Research, AI Product
Research, Research Systems, and (at the human's request) Published Research.

## 2026-10-08: Related Links reordered, "intern" demoted
Paper, CNET coverage and the Live Guide article come first. "Adobe Life: Intern Achievement
Spotlight" became "Adobe Life: Achievement Spotlight"; the Friends of Figma item leads with
"Friends of Figma Panel". The quote inside the Adobe card still says intern because it is a quote.

## 2026-10-08: prose added to the MLLM page without removing visuals
The lead case study had about 450 words against 2,300 to 4,700 on the others, with headings and
no body. Human wanted the visuals kept for skimmers. Result: a paragraph between each heading and
its figure, written from what the figure actually shows. Known inconsistency carried over from the
images: the contextual inquiry caption says 8 designers, the summary and theme counts say 10. The
prose says 10. Not resolved.

## 2026-10-08: hero split relabelled Qualitative / Quantitative
Human wanted to keep the 50/50 photo but have it say qualitative and quantitative instead of
design and research. Done by image editing rather than CSS overlay so the two typographic styles
survive. See [[hero-pipeline]].

## 2026-10-08: moved to reubenluera.github.io via an organization
Human wanted a cleaner URL without buying a domain. Options were the root site under `benluera`
(`benluera.github.io`, but that repo held an old class page), renaming the account (breaks live
HP stimulus URLs), a second personal account (against GitHub terms), or an org. Org chosen.
See [[deploy]].

## 2026-10-08: hero-overlay built on a branch, not merged
Human liked the share image and asked what it would look like as the actual hero. Agent's
position: yes, but as HTML text over a CSS gradient, not the JPEG, with the overlay dropping below
the image on phones. Human asked for a branch to look at without committing. Open.

## 2026-10-07: static rebuild instead of Framer
The Framer site at reubenluera.framer.website was converted to static HTML so it could be hosted
on GitHub Pages and edited by the agent directly. The converter and the Framer agent CLI notes
live in the saga memory, not in this repo.
