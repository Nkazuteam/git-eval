#!/usr/bin/env bash
set -e

SESSION="git-eval"

# Kill existing session if any
tmux kill-session -t "$SESSION" 2>/dev/null || true

# Start new tmux session with bot
tmux new-session -d -s "$SESSION" \
  "cd $(dirname "$0") && source .venv/bin/activate && python -m bot.main"

echo "Started in tmux session '$SESSION'"
echo "  Attach:  tmux attach -t $SESSION"
echo "  Detach:  Ctrl+B, D"
echo "  Stop:    tmux kill-session -t $SESSION"
