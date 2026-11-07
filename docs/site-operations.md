# tombannerman.com — operations and handover

Last updated 27 Oct 2026. Read this before working on the site. This repo is **public** and GitHub Pages serves all of it, including this file.

## How the site works

- Repo `spikeypenguin123/tombannerman_website` → **GitHub Pages** serves the repo root at tombannerman.com (`CNAME`). A push to `main` is live in about a minute. (The original tracker package assumed Cloudflare Pages; that was never used.)
- Pages are hand-written, self-contained HTML (see the local `CLAUDE.md` conventions: inline CSS/JS, tokens and nav copied into each page).
- **Nav tabs on every page:** Home · Projects · Tech Tree · Writing · AI Tracker · Gallery · Store. Adding or renaming a tab means editing every hand-written page *and* `TABS` in `tools/tech-tree/build.py`, then rebuilding the tree.

| Path | What | How it changes |
|---|---|---|
| `/ai-dashboard/` | AI Frontier Tracker | Data (`ai-dashboard/data/latest.json`) refreshed every morning by the Mac mini job. Page code changes are deliberate. Docs: `tracker/README.md`, `tracker/CHANGELOG.md`. |
| `/ai-in-october-2026/` | Beginner primer (essay styling, four interactive charts) | Static. Numbers are as of 18 Oct 2026 (task length through Claude Mythos Preview, 50% and 80%). It will drift from the tracker over time. |
| `/tech-tree.html`, `/tree/<id>.html` | Tech tree and one article per node | **Generated.** Edit `tools/tech-tree/nodes.py`, run `python3 tools/tech-tree/build.py`. Never hand-edit the generated files. |
| `/getting-it-right.html`, `/shooting-film.html`, `/three-pillars-of-value-after-agi/` | Essays | Hand-written. |

## Working copies

- **Mac mini** (`ssh vera@veras-mac-mini` over Tailscale):
  - `~/sites/tombannerman.com` — `main`. The daily job commits and pushes from here. Always `git pull` before editing, here or anywhere else.
  - `~/sites/tombannerman-demo` — git worktree on branch `claude/tech-tree-demo` (warmer home page demo `index-demo.html`, not merged). Behind `main`.
  - `~/sites/tracker-package` — the original unzipped tracker package, reference only.
- **Laptop:** `~/Documents/GitHub/tombannerman_website/tombannerman_website`. Pull before editing.

## Daily tracker job (Mac mini)

Full details: `tracker/README.md`.
- launchd agent `com.tombannerman.tracker-update`, 06:45 Brisbane, runs `tracker/deploy/macmini/tracker-update.sh` → headless `claude -p` following `tracker/update/daily-update-prompt.md` → validate → snapshot → commit → push.
- Log: `~/Library/Logs/tracker-update.log`. A healthy day ends `claude exit code: 0` with a `data: daily update YYYY-MM-DD` commit.
- Needs: user `vera` logged in (FileVault is on, so after a power cut someone must log in); `gh` logged in as `spikeypenguin123` with `gh auth setup-git`; `~/.config/tracker/token.env` holding `CLAUDE_CODE_OAUTH_TOKEN` (made 18 Oct 2026 with `claude setup-token`; lasts about a year, so **renew by about Oct 2027**).
- Failures seen so far: no network 23–25 Oct 2026 (`Could not resolve host: github.com`; recovered by itself); `cp` to `/tmp` refused (fixed 27 Oct: backup now in `tracker/.work/`).
- Unattended-run rules (in the prompt): one allowed command per Bash call (`python3`, `git`, `cp`, `date`, `ls`), no `&&`/pipes/`cd`/env prefixes, no writes outside the repo.

## Tech tree: adding content

- Each node in `tools/tech-tree/nodes.py`: `id, b (branch), t (tier, 1 = roots), title, when, req, hard, todo, text, stats [[label, value or None]], story [paragraphs], photos [{src, cap}], link`. Newest items sort to the top of each branch by the year in `when`.
- Photos: put files in `tools/tech-tree/photos/` and reference them as `{"src": "photos/name.jpg", "cap": "..."}`. The build embeds them as data URIs (site convention), so compress first (aim for ~200 KB each).
- Removing a node: delete it from `nodes.py`, fix any `req` that pointed at it, rebuild, and `git rm tree/<id>.html` (the build does not delete old pages).
- **Still to collect from Tom:** finish times (Gold Coast Marathon 2025, Guzzler 50 km 2025, Ironman 70.3 Sunshine Coast 2026), dive certifications, Bronze Medallion club and year, courses, photos for every node.

## Open items

1. **Warmer home page** (`index-demo.html` on the demo branch): waiting for Tom's decision. If approved, replace the body of `index.html`, then delete the demo worktree and branch.
2. **Tracker page has no site nav** (it has its own dark design). Offered a nav bar or a "← tombannerman.com" link; not done.
3. **AI primer is static**; refresh it or add an "as of" note when the tracker moves on.
4. Tech tree content (above).

## Lessons learned

- Everything committed here is public at `tombannerman.com/<path>`, including `docs/`, `tracker/` and `tools/`. Private material belongs in a private repo.
- After any page change, check it renders: headless Chrome with `--virtual-time-budget`, kill the process afterwards (it can hang), and remember screenshots ignore scrolling and catch `.reveal` fade-ins half-way.
- In single-line JS, never add a `//` comment mid-line: it comments out the rest of the line. Use `/* */`.
- zsh does not word-split unquoted `$var` in loops (`set -- $v` fails); use `${=v}` or separate calls.
- METR's time-horizons page is frozen (8 Sep 2026); its results file `metr.org/assets/benchmark_results_1_1.yaml` has 50% and 80% values. Newer readings come from METR's blog (evaluations, risk reports) and Epoch (MirrorCode).
- Keep comparisons on the newest models: never leave a tile, milestone or chart anchored on a superseded model when a newer one has the number.
