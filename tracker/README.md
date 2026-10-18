# AI Frontier Tracker

A public AI tracker on tombannerman.com and the daily job that keeps it current.

| Page | URL | Updates |
|---|---|---|
| AI Frontier Tracker | `/ai-dashboard/` | Data refreshed daily at 06:45 Brisbane by the Mac mini |
| Where AI stands in October 2026 | `/ai-in-october-2026/` | Static article |

Both are listed on `writing.html`.

## Folder map

```
ai-dashboard/
├── index.html             ← tracker (renders from data/latest.json)
├── methodology.html
└── data/
    ├── latest.json        ← the ONLY file the daily job edits
    └── history/           ← one snapshot per day + index.json
ai-in-october-2026/index.html
tracker/
├── README.md              ← this file
├── CHANGELOG.md           ← code / method changes (what + why)
├── update/
│   ├── daily-update-prompt.md  ← the full instructions for the daily run
│   ├── validate.py             ← blocks bad data from publishing (stdlib only)
│   └── snapshot.py             ← archives the day into data/history/
├── deploy/macmini/        ← job script + launchd plist
└── docs/data-schema.md    ← every field in latest.json
```

`tracker/CLAUDE.md` (house rules for Claude Code sessions) and `founder/` (the private calculator) are git-ignored and live only on the machines that need them. The repo is public, so nothing personal is committed.

## Preview locally
```bash
python3 -m http.server 8000      # from the repo root
# open http://localhost:8000/ai-dashboard/
```

## Mac mini
The Mac mini (`vera@veras-mac-mini`, over Tailscale) runs the job from `~/sites/tombannerman.com` and pushes to `main`; GitHub Pages redeploys on push. The site stays up when the Mac is off.

- Job: `tracker/deploy/macmini/tracker-update.sh`, scheduled by `~/Library/LaunchAgents/com.tombannerman.tracker-update.plist` at 06:45 local (Australia/Brisbane).
- Needs: `vera` logged in (launchd agent), `gh auth setup-git` done, and `~/.config/tracker/token.env` containing `export CLAUDE_CODE_OAUTH_TOKEN=…` (from `claude setup-token`, mode 600).
- Manual run: `zsh ~/sites/tombannerman.com/tracker/deploy/macmini/tracker-update.sh; tail -40 ~/Library/Logs/tracker-update.log`
- Install the schedule: `sed "s#__HOME__#$HOME#g" ~/sites/tombannerman.com/tracker/deploy/macmini/com.tombannerman.tracker-update.plist > ~/Library/LaunchAgents/com.tombannerman.tracker-update.plist && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.tombannerman.tracker-update.plist`

**Safety net.** `validate.py` refuses a broken or inconsistent file and compares with yesterday's. The job restores the last committed file if validation fails after the run. The tracker shows a warning dot if the data is more than 30 hours old.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Tracker shows a red dot / old date | Read `~/Library/Logs/tracker-update.log` on the Mac mini. Re-run the script by hand. |
| `no CLAUDE_CODE_OAUTH_TOKEN` | Run `claude setup-token` on the Mac mini and save it to `~/.config/tracker/token.env`; the token lasts about a year. |
| `git pull` or `git push` fails in the job | `gh auth status` on the Mac mini; re-run `gh auth login` and `gh auth setup-git`. |
| `latest.json fails validation` | The job already restored the last good file. Run `python3 tracker/update/validate.py` to see why. |
| Job never runs | `vera` was logged out or the Mac slept: check `pmset -g` and `launchctl print gui/$(id -u)/com.tombannerman.tracker-update`. FileVault is on, so after a power cut someone must log in before the job can run. |
