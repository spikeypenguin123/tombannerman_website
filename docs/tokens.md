# Design tokens — tombannerman.com

Measured from the source on `claude/tombannerman-store-tokens-mejjp0`. Every value below
is copied verbatim from a declaration in the repo; nothing is inferred, rounded, or
converted. Where a value could not be determined from source it says so explicitly.

## How the CSS is organised (read this first)

There is **no stylesheet file in this repo**. `find . -name "*.css"` returns nothing.
All CSS lives in a single `<style>` block inside the `<head>` of each HTML page.

Three variants of that block exist:

| Variant | Pages | Notes |
| --- | --- | --- |
| Main | `index.html`, `projects.html`, `writing.html`, `gallery.html`, `store.html` | Byte-identical across all five (verified with `diff`) |
| Essay | `getting-it-right.html`, `shooting-film.html` | Shares `:root`, resets, nav, `.wrap`; drops the home/timeline/gallery/store rules; adds article rules. The two essay pages differ from each other. |
| 404 | `404.html` | Standalone. Redeclares a four-token subset of `:root` rather than sharing it. |

`store.html` is now a redirect stub to `https://shop.tombannerman.com` and carries the
same standalone shape as `404.html`, not the main variant.

Consequence: **there is no single source of truth for these tokens.** A change to a value
has to be made in up to eight places by hand. That is a fact about the current source,
not a recommendation.

---

## Colour

### Declared custom properties

Declared in `:root` in the main and essay variants. Hex casing is reproduced exactly as
written in source (the file mixes cases).

| Token | Value | Role, as used in source |
| --- | --- | --- |
| `--paper` | `#fff7e6` | Page background (`body{background:var(--paper)}`). Also the knockout colour on dark fills: active tab text, `.links a:hover` text, `.btn` text, `.tl-node` ring. |
| `--paper-deep` | `#FFEAD0` | Raised/secondary surface. Used on `.store-cta`, `.pull`, and as the `background` behind `figure img`. |
| `--ink` | `#2A1733` | Body text (`body{color:var(--ink)}`), wordmark, all `1.5px` card/button borders, active-tab and `.btn` fill. |
| `--ink-soft` | `#5a4660` | Muted/secondary text: nav tabs at rest, `.eyebrow` notes, `.cv-when`, `.lead-meta`, `.tl-date`, `figcaption`, `.colophon`, footer links. |
| `--violet` | `#922aff` | Link colour (`a{color:var(--violet)}`) and the primary accent: `.eyebrow`, `.mark b`, `.badge` fill, `.btn:hover` fill, `.abstract` left rule, section-number prefixes, first bullet in the 5-colour rotation. |
| `--periwinkle` | `#726bf3` | Accent. `::selection` background, `.tl-card .meta` text, 4th in the bullet/node rotation, gradient stops. |
| `--orange` | `#f19202` | Link hover colour (`a:hover{color:var(--orange)}`). Also `.pull` left rule, `.ctrl-top .val`, 3rd in the rotation. |
| `--red` | `#ff3939` | Accent only — 2nd in the rotation, gradient stops (timeline rule, avatar ring, footer sun). Not used for errors or state anywhere in source. |
| `--teal` | `#179f93` | Accent — 5th in the rotation, and the `.note` scope-block left rule and label colour in `shooting-film.html`. |
| `--line` | `rgba(42,23,51,.16)` | Every hairline rule: `1px` borders on nav, `.explore` rows, `.cv-row`, `.plist` rows, `footer`, plus `.empty`'s dashed border and the `.eyebrow` trailing rule. Equals `--ink` (`rgb(42,23,51)`) at 16% alpha. |

### Dark-panel tokens — `getting-it-right.html` only

Declared in that page's `:root`, absent from every other page including
`shooting-film.html`. They exist to style the interactive simulator block.

| Token | Value | Role |
| --- | --- | --- |
| `--panel` | `#160c1e` | Panel and `<canvas>` background |
| `--panel-line` | `rgba(255,255,255,.12)` | Panel divider and `.reset` button border |
| `--panel-ink` | `#ece5f4` | Text on panel |
| `--panel-soft` | `#a99fc0` | Muted text on panel |

### Literal colours used without a token

These appear as raw values in rules and have no custom property behind them.

| Value | Where | Role |
| --- | --- | --- |
| `rgba(255,219,187,.82)` | `.nav` | Sticky nav background, behind `backdrop-filter:saturate(140%) blur(8px)`. **Not derived from any declared token** — the opaque colour is `#FFDBBB`, which is neither `--paper` nor `--paper-deep`. |
| `#fff` | `::selection` text, `.badge` text, `.shot .cap` text, `.btn:hover` text, `.reset:hover` text, `.product .ph` text | Pure white on saturated fills, where `--paper` is not used |
| `rgba(255,255,255,.9)` | `.ph-shot` | Placeholder label text on gradient tiles |
| `rgba(42,23,51,.06)` | `.tabs a:hover` | Inactive tab hover background — `--ink` at 6% |
| `rgba(20,8,30,.72)` | `.shot .cap` | Bottom of the gallery caption scrim gradient (`linear-gradient(transparent, …)`). Opaque form `#14081E`; close to but not equal to `--ink`. |

`404.html` redeclares `--paper`, `--ink`, `--ink-soft`, `--violet`, `--red`, `--orange`,
`--line` with the same values as above. It does **not** declare `--paper-deep`,
`--periwinkle`, or `--teal`.

The footer sun SVG is inline in each page and hard-codes `#922aff`, `#ff3939`, `#f19202`
(gradient stops), `#fff7e6` (horizon bars) and `#2A1733` (baseline) rather than
referencing the tokens.

### Shadows

All offset-only, zero-blur, `--ink`-tinted — no token, five distinct values:

- `5px 7px 0 rgba(42,23,51,.10)` — `.tl-card` at rest
- `7px 10px 0 rgba(42,23,51,.14)` — `.tl-card:hover`
- `6px 8px 0 rgba(42,23,51,.12)` — `.avatar`
- `5px 7px 0 rgba(42,23,51,.12)` — `.sim`, `figure img`
- `0 0 0 5px var(--paper)` — `.tl-node`, a knockout ring rather than a shadow

---

## Typography

### Families and loading

Three families, all from Google Fonts. Loading is identical on every page: two
`<link rel="preconnect">` (to `fonts.googleapis.com` and `fonts.gstatic.com`, the latter
`crossorigin`) followed by one `<link rel="stylesheet">` to the CSS2 API. No self-hosting,
no `@font-face` in the repo, no local font files, no JS font loader.

Request on `index.html`, `projects.html`, `writing.html`, `gallery.html`,
`getting-it-right.html`, `shooting-film.html`:

```
https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,300..700,0..100,0..1&family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap
```

`404.html` and the `store.html` redirect stub request a shorter version — Fraunces and
Space Mono only, no Space Grotesk — because neither page sets a Space Grotesk stack.

| Role | Stack | Loaded as |
| --- | --- | --- |
| Body / UI | `"Space Grotesk", system-ui, sans-serif` | Static weights 400, 500, 700 |
| Display / headings | `"Fraunces", serif` | Variable: `opsz 9..144`, `wght 300..700`, `SOFT 0..100`, `WONK 0..1` |
| Labels / meta / nav | `"Space Mono", monospace` | Static weights 400, 700 |

`display=swap` on every request. Fallback stacks are one deep for body (`system-ui`) and
generic-only for the other two (`serif`, `monospace`) — no metric-matched fallback is
specified anywhere.

Fraunces is used through `font-variation-settings`, not just weight. The exact settings
in source:

| Setting | Used on |
| --- | --- |
| `"opsz" 144,"SOFT" 40,"WONK" 1` | `.home-hero h1`, `.post-head h1`, `404 .code` |
| `"opsz" 80,"SOFT" 30,"WONK" 0` | `h2`, `.prose h2` |
| `"opsz" 60,"SOFT" 40` | `.empty h3` |
| `"opsz" 50,"SOFT" 30` | `.tl-card h3` |
| `"opsz" 40,"SOFT" 30` | `.explore .e-link`, `.prose h3` |
| `"opsz" 40,"SOFT" 40,"WONK" 1` | `.pull` |
| `"opsz" 30,"SOFT" 40,"WONK" 1` | `.mark` |

Several Fraunces rules set no variation settings at all and inherit the default axis
values: `.store-cta h3`, `.product .info h3`, `.stat .v`, `404 h1`, and `h1` in the
redirect stub.

### Size scale

Base is `17px` on `body`. There is no modular ratio — sizes are hand-picked, land on
half-pixels in six places, and are declared in `px` throughout (no `rem`, no `em` except
one relative case).

Fixed sizes, ascending, with where each is used:

| Size | Used on |
| --- | --- |
| `10px` | `.badge`, `.ph-shot`, `.stat .k` |
| `10.5px` | `.legend`, `.note .label` |
| `11px` | `.tl-card .meta`, `.shot .cap`, `.product .ph`, `.reset`, `.colophon` |
| `11.5px` | `.explore span.note`, `figcaption` |
| `12px` | `.tabs a`, `.eyebrow`, `.lead-meta`, `.tl-date`, `.post-meta`, `.foot-links a` |
| `12.5px` | `.links a`, `.cv-when` |
| `13px` | `.btn`, `.product .info p`, `.ctrl-top .val`, `.stat .v small` |
| `13.5px` | `.map` |
| `14px` | `.plist li span` |
| `15px` | `.tl-card p`, `.store-cta p` |
| `15.5px` | `.cv-what`, `.plist li`, `.note` |
| `16px` | `.bio .stars` |
| `17px` | `body` — the base |
| `18px` | `.bio p:first-of-type`, `.lead`, `.product .info h3`, `.closer` |
| `18.5px` | `.abstract` |
| `19px` | `.mark`, `.pull` |
| `21px` | `.explore .e-link`, `.tl-card h3`, `.prose h3` |
| `24px` | `.store-cta h3` |
| `25px` | `.empty h3` |
| `26px` | `.stat .v` |

One relative size: `.prose h2 .num` at `.5em` (the section-number prefix, half its
heading).

Fluid sizes, all `clamp(min, vw, max)`:

| Rule | Element |
| --- | --- |
| `clamp(38px,7vw,62px)` | `.home-hero h1` |
| `clamp(34px,6vw,58px)` | `.post-head h1` (essay pages) |
| `clamp(26px,3.6vw,36px)` | `h2` (main variant) |
| `clamp(24px,3.4vw,33px)` | `.prose h2` (essay pages) |
| `clamp(72px,18vw,150px)` | `.code` (404 only) |
| `clamp(22px,4vw,30px)` | `h1` (404 and the redirect stub) |

### Weights

Four values in use: `400`, `500`, `600`, `700`.

- Space Grotesk — 400 default, `500` on `.cv-what .org` and `.map b`, `700` on
  `.cv-what b`, `.plist li b`, `.prose strong`
- Fraunces — `500` on `h2` / `.prose h2` / `.empty h3` / `404 h1`; `600` on `.mark`,
  `.home-hero h1`, `.post-head h1`, `.explore .e-link`, `.tl-card h3`, `.prose h3`,
  `.store-cta h3`, `.product .info h3`, `.stat .v`, `.code`
- Space Mono — 400 default; `400` set explicitly on `.stat .v small`, `.post-meta b` and
  `figcaption b` to cancel inherited bold. Weight 700 is requested from Google Fonts but
  **no rule in the repo sets `font-weight:700` on a Space Mono element** — it is loaded
  and unused.

### Line-height

`body` sets `1.65` and everything inherits it unless overridden.

| Value | Used on |
| --- | --- |
| `.9` | `404 .code` |
| `.95` | `.home-hero h1` |
| `1` | `.stat .v` |
| `1.0` | `.post-head h1` (written with the trailing zero) |
| `1.05` | `h2` |
| `1.08` | `.prose h2` |
| `1.1` | `.tl-card h3` |
| `1.15` | `.prose h3` |
| `1.5` | `.map`, `.pull` |
| `1.6` | `figcaption` |
| `1.62` | `.note` |
| `1.65` | `body` — the base |
| `1.72` | `.abstract` |

Display type tightens below 1.1; long-form prose loosens above the base. Nothing between
1.15 and 1.5 is used.

### Letter-spacing

Two systems: negative `em` on Fraunces display type, positive `px` on Space Mono labels.

| Value | Used on |
| --- | --- |
| `-.03em` | `404 .code` |
| `-.025em` | `.home-hero h1`, `.post-head h1` |
| `-.01em` | `h2`, `.prose h2`, `404 h1` |
| `-.005em` | `.prose h3` |
| `0` | `.prose h2 .num` — explicitly cancels the inherited tracking |
| `.3px` | `.mark`, `.explore span.note`, `.cv-when`, `figcaption` |
| `.5px` | `.links a`, `.tl-card .meta`, `.shot .cap`, `.legend`, `.colophon`, `404 p`, `404 .links a` |
| `1px` | `.tabs a`, `.lead-meta`, `.tl-date`, `.badge`, `.btn`, `.ph-shot`, `.product .ph`, `.post-meta`, `.stat .k`, `.ctrl-top label`, `.reset`, `.pull .who`, `.foot-links a` |
| `1.5px` | `.note .label` |
| `3px` | `.eyebrow` — the widest, on the section kicker |

`text-transform:uppercase` accompanies every use of `1px` and above.

---

## Spacing

**There is no spacing scale.** Values are hand-picked per rule; consecutive integers
(`9`, `10`, `11`, `12`, `13`, `14`) all appear, so no consistent base unit — 4px or
otherwise — can be recovered from source. What follows is the complete measured
inventory, not a system.

Vertical rhythm — the load-bearing values:

| Value | Rule |
| --- | --- |
| `54px 0` | `section` on the main variant |
| `40px 0` | `section` on the essay variant |
| `46px 0` | `footer` |
| `46px 0 6px` | `.home-hero` |
| `48px 0 6px` | `.post-head` |
| `0 24px` | `.wrap` — the horizontal page gutter, the same at every breakpoint |
| `13px 24px` | `.nav-in` |

The two inventories below cover the main and essay variants; `404.html` and the redirect
stub add `gap:18px` / `gap:9px` and `padding:40px 24px` / `padding:9px 16px`.

All `gap` values in use: `0`, `2px`, `6px`, `9px`, `10px`, `12px`, `14px`, `16px`, `18px`,
`20px`, `22px`, `24px`, `34px`, and `0 36px` (row/column split, on `.plist`).

All `padding` values in use: `0`, `5px`, `6px`, `9px 0`, `14px`, `15px 2px`, `3px 8px`,
`7px 13px`, `7px 14px`, `8px 16px`, `8px 18px`, `11px 8px`, `13px 22px`, `13px 24px`,
`14px 16px`, `16px 20px`, `15px 20px 14px`, `18px 20px 20px`, `24px 14px 11px`, `30px`,
`46px 28px`, `0 0 0 22px`, `4px 0 4px 22px`, `0 0 30px 58px`, `0 24px`, `40px 0`,
`46px 0`, `46px 0 6px`, `48px 0 6px`, `54px 0`.

Block margins, mostly `0 0 Npx`: `3`, `5`, `8`, `9`, `10`, `12`, `14`, `16`, `18`, `22`,
`28`. Article rules use asymmetric forms: `8px 0 18px` (`.prose h2`),
`32px 0 12px` (`.prose h3`), `30px 0 26px` (`figure`), `34px 0 8px` (`.fig-hero`),
`26px 0 6px` (`.sim`), `26px 0 4px` (`.note`), `20px 0 18px` (`.pull`),
`30px 0 8px` (`.abstract`).

---

## Layout

### Content width

| Token | Value | Applies to |
| --- | --- | --- |
| `--w` | `760px` | `.wrap` — the default column for prose and most sections |
| `--w-wide` | `1080px` | `.wide` (a modifier on `.wrap`) and `.nav-in` — the nav always spans the wide width even when content below it does not |

Both tokens are declared in `:root` on the main **and** essay variants, but `.wide` itself
is only defined in the main variant. `404.html` declares neither and centres with flexbox
instead.

Measure is capped independently of the column, in `ch`:

| Cap | Applies to |
| --- | --- |
| `48ch` | `.empty p` |
| `52ch` | `.map` |
| `54ch` | `.bio p` |
| `60ch` | `figcaption` |
| `62ch` | `.lead` |
| `64ch` | `.prose p`, `.prose ul`, `.note`, `.pull`, `.closer p` — the long-form default |
| `46ch` | `404 p` and the redirect stub's `p` |

`.note p` and `.pull p` set `max-width:none` to opt out of the inherited `64ch`.

### Border-radius

No radius token exists; every value is a literal.

| Value | Used on |
| --- | --- |
| `8px` | `.tabs a` below 820px only — the mobile drawer's tap targets |
| `16px` | The card radius: `.tl-card`, `.product`, `.store-cta`, `.shot`, `.empty`, `figure img` |
| `18px` | `.sim` — the one card that is not 16px |
| `20px` | `.badge` |
| `30px` | Pills: `.tabs a` (desktop), `.links a`, `.reset`, `404 .links a` |
| `40px` | `.btn` — the largest pill |
| `50%` | Circles: `.avatar`, `.avatar img`, `.tl-node`, `.dot`, `.legend .sw`, `.prose ul li::before` |
| `0 14px 14px 0` | `.note`, `.pull` — square left edge against the 3px accent rule |

`14px` appears **only** inside that last shorthand; it is not used as a uniform radius
anywhere.

### Border widths

Four widths, used consistently by role:

- `1px` — hairline rules, always `var(--line)`: nav bottom, `.explore li`, `.cv-row` and
  `.plist li` separators, `.shot`, `.closer` top, `footer` top, and the mobile drawer
- `1.5px` — structural borders. `1.5px solid var(--ink)` on `.links a`, `.tl-card`,
  `.tl-card .pic` (bottom only), `.product`, `.store-cta`, `.sim`, `figure img`. Three
  variants: `1.5px dashed var(--line)` on `.empty`, `1.5px solid var(--line)` on `.note`
  (its left edge then overridden to 3px teal), and `1.5px solid var(--panel-line)` on
  `.sim-panel` and `.reset`
- `2px` — the `.timeline::before` spine
- `3px` — `.tl-node`'s ring, and the left accent rules on `.abstract` (violet), `.note`
  (teal), `.pull` (orange)
- `4px` — the `--paper` ring inside `.avatar img`

### Breakpoints

Four, all `max-width`, all in the main or essay variant only:

| Breakpoint | Effect |
| --- | --- |
| `820px` | Nav collapses to the burger drawer; `.tabs` becomes an absolutely-positioned column animating `max-height` 0 → `340px` |
| `600px` | `.home-hero` stacks; masonry 3 → 2 columns; products 3 → 2 columns; sim stats left-align (essay) |
| `560px` | `.fig-pair` gap 14px → 9px (`shooting-film.html` only) |
| `520px` | `.cv-row` and `.plist` go single-column; `.explore span.note` hides; masonry → 1 column; products → 1 column; `.store-cta` stacks |

`.fig-pair` stays two-up at every width by design — see commit `bc840e6`.

---

## Motion

| Value | Used on |
| --- | --- |
| `.2s` | `.links a`, `.btn`, `.reset`, `.tl-card` (`transform`, `box-shadow`), `.explore .arrow` (`transform`), `404 .links a` |
| `.25s` | `.burger span`, `.shot .cap` opacity |
| `.3s ease` | `.tabs` `max-height` (drawer open/close) |
| `.7s ease` | `.reveal` opacity and transform — the scroll-in animation |

No easing function is named other than `ease`; no custom cubic-bezier and no motion
tokens exist.

`prefers-reduced-motion:reduce` is honoured in two places: it disables
`html{scroll-behavior:smooth}` and it disables the `.reveal` animation entirely
(`opacity:1;transform:none;transition:none`). The `.2s`/`.25s` hover transitions are
**not** covered by the reduced-motion query.

---

## Texture

`body::before` overlays a fixed, non-interactive fractal-noise SVG at
`opacity:.05`, `mix-blend-mode:multiply`, `z-index:9`, tile size `160×160`,
`baseFrequency='0.85'`, `numOctaves='2'`. Present on the main and essay variants;
absent from `404.html` and the redirect stub.

---

## Not determinable from source

- **Icon sizing and elevation scales.** `z-index` takes exactly two values per page —
  `9` on the `body::before` noise overlay and `20` on `.nav` — which is not enough to
  recover a layering scale.
- **Any semantic state colours.** There is no success, warning, error, disabled, or focus
  colour anywhere in the CSS. `--red` is used decoratively (bullets, gradients), never for
  errors. No `:focus` or `:focus-visible` rule is defined on any page, so focus rendering
  is entirely the browser default.
- **Dark mode.** No `prefers-color-scheme` query and no `data-theme` hook exists. The
  `--panel*` tokens are a dark *component*, not a theme.
- **The intended relationship between `rgba(255,219,187,.82)` (nav) and the paper tokens.**
  The opaque colour `#FFDBBB` matches neither `--paper` nor `--paper-deep`, and no comment
  explains it.
- **Whether the loaded Space Mono 700 and the Fraunces `wght` range below 500 are
  intentional headroom or leftovers.** They are requested from Google Fonts but never
  referenced by a rule.
