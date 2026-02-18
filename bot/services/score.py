import json
import os
from typing import Any

from bot.config import USERS_FILE, RANKS, RANK_THRESHOLDS


def _load_users() -> dict[str, Any]:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_users(data: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user(discord_id: str) -> dict[str, Any] | None:
    users = _load_users()
    return users.get(discord_id)


def register_user(discord_id: str, github_username: str) -> dict[str, Any]:
    users = _load_users()
    users[discord_id] = {
        "github_username": github_username,
        "rank": "G",
        "score": 0,
    }
    _save_users(users)
    return users[discord_id]


def find_by_github(github_username: str) -> tuple[str, dict[str, Any]] | None:
    users = _load_users()
    for did, data in users.items():
        if data.get("github_username", "").lower() == github_username.lower():
            return did, data
    return None


def determine_rank(score: int) -> str:
    current = "G"
    for rank in RANKS:
        if score >= RANK_THRESHOLDS[rank]:
            current = rank
    return current


def score_for_next_rank(current_rank: str, current_score: int) -> int | None:
    idx = RANKS.index(current_rank)
    if idx >= len(RANKS) - 1:
        return None  # Already S
    next_rank = RANKS[idx + 1]
    return RANK_THRESHOLDS[next_rank] - current_score


SKIP_GRADE_THRESHOLD = 70  # Score needed to trigger skip-grade


def add_score(
    discord_id: str, points: int, eval_rank: str | None = None
) -> tuple[str, str, int]:
    """Add points, check skip-grade, return (old_rank, new_rank, new_score)."""
    users = _load_users()
    user = users[discord_id]
    old_rank = user["rank"]

    user["score"] += points

    # Skip-grade: if evaluated at a higher rank and scored well, jump there
    if eval_rank and eval_rank in RANKS:
        old_idx = RANKS.index(old_rank)
        eval_idx = RANKS.index(eval_rank)
        if eval_idx > old_idx and points >= SKIP_GRADE_THRESHOLD:
            threshold = RANK_THRESHOLDS[eval_rank]
            if user["score"] < threshold:
                user["score"] = threshold + points

    user["rank"] = determine_rank(user["score"])
    _save_users(users)
    return old_rank, user["rank"], user["score"]
