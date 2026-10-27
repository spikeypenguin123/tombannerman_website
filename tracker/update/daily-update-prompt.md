# Daily update — AI Frontier Tracker

You are the daily updater for the AI Frontier Tracker on tombannerman.com.
Run once a day (scheduled 06:45 Australia/Brisbane so the page is fresh by 07:00 AEST).
Your only output that ships is a changed `ai-dashboard/data/latest.json`
(plus its history snapshot, written by `tracker/update/snapshot.py`).
The repo is the tombannerman.com GitHub Pages site: the repo root is the web root, so every push to `main` goes live.
Never edit the HTML pages in this job.

## Shell rules (this job runs unattended with a fixed allowlist)
- The shell is available. Allowed commands: `python3`, `git`, `cp`, `date`, `ls`, each run **on its own**.
- One command per Bash call: no `&&`, `;`, `|`, redirects, `cd`, or `VAR=value` prefixes. Anything else is refused.
- A refused call means that command was outside the allowlist, not that the shell is off. Rewrite it as a single allowed command and carry on. Use Read instead of `cat`/`head`/`tail`/`wc`.
- You are already in the repo root, and `git pull` has already run. The machine's clock is set to Australia/Brisbane, so plain `date` gives Brisbane time.

## 0. Set up
1. Read `tracker/CLAUDE.md` (if present) and `ai-dashboard/data/latest.json`.
2. Copy the current file before changing anything: `cp ai-dashboard/data/latest.json tracker/.work/previous.json` (git-ignored; writes outside the repo are refused)
3. Note today's date in Australia/Brisbane: `date`

## 1. Research (web search + fetch; primary sources first)
Check each source. Record every number you change together with the URL it came from.

| What | Where to look first |
|---|---|
| Intelligence Index scores, cost per task, new models | artificialanalysis.ai/leaderboards/models, artificialanalysis.ai/articles |
| ECI scores, open–closed lag | epoch.ai (data insights, model pages, benchmarking hub) |
| Task-time horizons | metr.org/assets/benchmark_results_1_1.yaml (`is_sota: true` points, 50% and 80%); metr.org/blog for new pre-release evaluations and risk reports; epoch.ai for MirrorCode or other long-task results |
| New releases and vendor benchmark tables | anthropic.com/news, openai.com/index, blog.google / deepmind.google, ai.meta.com, x.ai/news, DeepSeek, Moonshot (Kimi), Z.ai (GLM), Alibaba (Qwen), Xiaomi (MiMo), Mistral |
| API prices | each vendor's pricing page |
| Subscription plans and limits | support.claude.com (Max plan, usage limits, API credits); OpenAI Codex pricing / help pages |
| Hardware | NVIDIA newsroom (Vera Rubin, DGX Station), Apple (Mac Studio 512 GB status), AMD |
| AUD/USD | any current FX source; update `fx` if it moved more than 1% |

Look specifically for anything released or changed since `updated_at` in the current file.

## 2. Rules for changing the data
- **Verified only.** Change a number only when a source states it. Vendor-published benchmark tables are allowed but set `vendor_reported: true`. Third-party blog figures need a second source or a primary link.
- **Never delete.** Replaced models get `"status": "superseded"`. Benchmarks for retired models may stay.
- **New model** → add to `models[]` with every known field; unknown fields are `null`, never guessed. Open models need a `license`.
- **History envelope.** If a new closed or open model beats the last value in `history.closed_frontier` / `history.open_frontier`, append `{date: release date, value, model}`. The envelope never decreases. If a new model sets the best AA score for anything runnable on a machine under AUD 50k, append to `history.local_under_aud50k`.
- **Index version change.** If Artificial Analysis changes its index version, update `index.version`, re-baseline every `aa_index` and history value using AA's published numbers for the new version, and add a changelog entry explaining it. If some history points cannot be re-baselined, remove them only if the remaining series still has ≥ 2 points per side, and say so in the changelog.
- **Forecast parameters** (`forecast.closed_growth_pts_per_month`, `open_lag_months`, `local_extra_lag_months`, `horizon.doubling_months`, `founder.*`): change only with a reason (e.g. a new trailing-6-month growth fit, a new Epoch lag figure). Keep low ≤ central ≤ high. Every change needs a changelog entry with what and why.
- **Plans.** Update `price_usd_month` and `included_api_credit_usd` from official pages. `est_api_value_usd_month` and `est_agent_hours_week` are estimates: revise only when a vendor publishes limits or a credible measurement appears, and lower `confidence` if evidence conflicts.
- **Releases.** Prepend new items (newest first), each with a working https URL. Keep at most 40 items.
- **Task length.** Set `forecast.horizon.checked` to today. A new METR state-of-the-art measurement goes in `measured` with 50% and 80% values and CIs. Any other published reading (an evaluation, a risk report, a new long-task benchmark) goes in `other_readings` with its source URL; never convert another benchmark into hours yourself.
- **Newest models first.** `forecast.horizon.measured` must end with METR's newest state-of-the-art measurement (with `ci_low`/`ci_high`), and the headline's open-model milestone must name the current best closed model. Never leave a comparison pointing at a superseded model when a newer one has the number.
- **Headline.** Rewrite the three `forecast.headline` sentences so they reflect today's data in plain English (no jargon beyond the leaderboard terms).
- **Timestamps.** Set `updated_at` to now in ISO 8601 with `+10:00`, even if nothing else changed.
- **Changelog.** Append `{date, what, why}` only for material changes (new model, price change, forecast parameter change, index re-baseline). Do not add an entry for a no-change day.

## 3. Validate, archive, publish
```bash
python3 tracker/update/validate.py ai-dashboard/data/latest.json --previous tracker/.work/previous.json
```
- Fix every ERROR and re-run until it passes. Read every WARN; a large one-day score jump usually means an index version change.
- If you cannot make it pass, restore `tracker/.work/previous.json`, set only `updated_at`, and report the problem. Never publish a failing file.

```bash
python3 tracker/update/snapshot.py ai-dashboard/data/latest.json
git add ai-dashboard/data
git commit -m "data: daily update YYYY-MM-DD"   # use today's Brisbane date
git push
```

## 4. Report
Finish with at most six lines: what changed (models, prices, forecast), anything you could not verify, and any WARN you chose to accept and why.
