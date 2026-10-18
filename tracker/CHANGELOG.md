# Changelog

Code and method changes. Daily data changes are logged inside `ai-dashboard/data/latest.json` → `changelog`.

## 2026-10-18 — v1.7
- **What:** Task length shows 80% success next to 50% (chart series, projection bands, tile, tooltips), a "current reading" (last measurement plus today's estimate at both rates), and an "Other readings" list. Schema: `minutes_80`/`ci80_*` on `horizon.measured`, `horizon.checked`, `horizon.other_readings`; validator checks them. The daily prompt now checks METR's blog and Epoch for new readings.
  **Why:** The chart only showed one success rate and stopped at the last METR point with no sign of newer evaluations; readers need both rates and what has (and hasn't) been measured since.

## 2026-10-18 — v1.6
- **What:** `ai-in-october-2026/` rebuilt in the site's essay styling with the site nav; task-length data and outlook brought in line with the tracker; compute chart gains a selector for six published brain estimates and a sources panel.
  **Why:** The article read as a separate site, still cited Claude Opus 4.6 and Opus 5, and gave one brain figure without showing where it came from.

## 2026-10-18 — v1.5
- **What:** The tracker now compares the newest models. The "Open vs closed gap" tile names both models; the "Task length" tile names today's frontier and the last METR-measured model with its date; the milestones follow the current best closed model instead of a hard-coded Claude Opus 5; horizon tooltips show METR's 95% CI. Schema: optional `ci_low`/`ci_high` on `horizon.measured`. The daily prompt now reads METR's results file and must keep comparisons on the newest models.
  **Why:** The page still anchored task length on Claude Opus 4.6 and two milestones on Claude Opus 5 after newer models had landed.

## 2026-10-18 — v1.4
- **What:** Added "Shell rules" to `tracker/update/daily-update-prompt.md` (one allowed command per call, what a refusal means, exact setup commands) and allowed `ls` in the job.
  **Why:** The first unattended run chained commands with `&&` and `|` (`wc`, `tail`), so the allowlist refused them; the agent then decided the shell was off and stopped without updating.

## 2026-10-18 — v1.3
- **What:** Moved into the tombannerman.com GitHub Pages repo: pages at `ai-dashboard/` and `ai-in-october-2026/` (repo root = web root), tooling under `tracker/`; listed both on `writing.html` and in `sitemap.xml`. All script and prompt paths updated; the job script now runs `tracker/update/daily-update-prompt.md` directly instead of the `/update-dashboard` slash command. Dropped `DEPLOY.md` (Cloudflare runbook), the founder page, `docs/founder-dashboard-questions.md` and `archive/` from the repo.
  **Why:** The site is already served by GitHub Pages from a public repo, so Cloudflare Pages isn't needed. A public repo can't protect `/founder/`, so it stays local and git-ignored, along with anything personal. The repo git-ignores `CLAUDE.md` and `.claude/`, so the job can't rely on a committed slash command.

## 2026-10-18 — v1.2
- **What:** Added `DEPLOY.md` (SSH runbook with checks and [TOM] hand-off steps), `docs/founder-dashboard-questions.md`; launchd commands switched to `bootstrap`/`kickstart`.
  **Why:** Deployment is being done by a Claude Code session over SSH; `launchctl load` is unreliable from SSH, `bootstrap gui/<uid>` targets the logged-in session.

## 2026-10-18 — v1.1
- **What:** Added `deploy/macmini/` (job script + launchd plist) and Mac mini deploy steps; calculator defaults now hold the owner's weekly schedule.
  **Why:** The Mac mini runs the daily job and pushes to Cloudflare Pages, so the site stays up when the Mac is off; browser-saved schedules do not move between sites, so the defaults carry them.

## 2026-10-18 — v1
- **What:** Split the single brain-equivalence dashboard into (1) a public AI Frontier Tracker driven by one data file and (2) a private founder calculator that reads the same file. Added a daily update prompt, a stdlib validator, a snapshot/archiver that also refreshes the calculator's offline copy, and the beginner article.
  **Why:** The public page must refresh every morning without anyone touching page code, and the calculator should always use the latest capability, pricing and plan data as its reference point.
- **What:** Subscription value and plan capacity shipped as labelled estimate ranges (`est_api_value_usd_month`, `est_agent_hours_week`, `confidence`).
  **Why:** Anthropic and OpenAI do not publish token budgets for Claude Max or Codex plans, so a single number would be false precision.
- **What:** Swarm model uses an Amdahl curve (60% parallel work, 3% coordination loss per extra agent).
  **Why:** Anthropic's agent-team docs report linear token cost, diminishing returns and a recommended 3–5 teammates; the curve flattens in that range.
- **What:** Calculator health score with a hard daily 60-minute exercise check and a one-click fix.
  **Why:** Owner requirement: at least one hour of exercise every day, scheduled, to protect work quality.
