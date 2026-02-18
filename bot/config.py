import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN: str = os.environ["DISCORD_TOKEN"]
GUILD_ID: int = int(os.environ["GUILD_ID"])
WEBHOOK_SECRET: str = os.environ["WEBHOOK_SECRET"]

NOTIFICATION_CHANNEL_ID: int = int(os.environ.get("NOTIFICATION_CHANNEL_ID", "0"))

DATA_DIR: str = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE: str = os.path.join(DATA_DIR, "users.json")

RANKS: list[str] = ["G", "F", "E", "D", "C", "B", "A", "S"]

RANK_THRESHOLDS: dict[str, int] = {
    "G": 0,
    "F": 100,
    "E": 250,
    "D": 500,
    "C": 1000,
    "B": 2000,
    "A": 4000,
    "S": 8000,
}

RANK_NAMES: dict[str, str] = {
    "G": "Generalist",
    "F": "Foundation",
    "E": "Emerging",
    "D": "Developer",
    "C": "Competent",
    "B": "Builder",
    "A": "Architect",
    "S": "Specialist",
}
