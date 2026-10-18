#!/bin/zsh
# tracker-update.sh — daily AI Frontier Tracker update, run by launchd at 06:45 Brisbane on the Mac mini.
# Pulls the site repo, runs tracker/update/daily-update-prompt.md headless, and lets
# that run validate, snapshot, commit and push. GitHub Pages redeploys on push.
#
# One-time setup: see tracker/README.md, "Mac mini".

REPO="${TRACKER_REPO:-$HOME/sites/tombannerman.com}"
LOG="$HOME/Library/Logs/tracker-update.log"
TOKEN_FILE="$HOME/.config/tracker/token.env"      # contains: export CLAUDE_CODE_OAUTH_TOKEN=...

export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
[ -f "$TOKEN_FILE" ] && source "$TOKEN_FILE"

{
  echo "=== $(date '+%Y-%m-%d %H:%M %Z') ==="
  if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
    echo "ERROR: no CLAUDE_CODE_OAUTH_TOKEN (run: claude setup-token, save to $TOKEN_FILE)"; exit 1
  fi
  cd "$REPO" || { echo "ERROR: repo not found at $REPO"; exit 1; }
  git pull --ff-only || { echo "ERROR: git pull failed"; exit 1; }

  claude -p "Follow every step in tracker/update/daily-update-prompt.md exactly. Today's run is for the date in Australia/Brisbane." \
    --permission-mode dontAsk \
    --permission-prompts none \
    --allowedTools "Read,Edit,Write,WebSearch,WebFetch,Bash(python3 *),Bash(git *),Bash(cp *),Bash(date *),Bash(ls *)"
  rc=$?
  echo "claude exit code: $rc"

  # Safety net: never leave a failing data file in the working tree.
  if ! python3 tracker/update/validate.py ai-dashboard/data/latest.json >/dev/null; then
    echo "ERROR: latest.json fails validation after the run; restoring last committed version"
    git checkout -- ai-dashboard/data/latest.json
  fi
  echo
} >> "$LOG" 2>&1
