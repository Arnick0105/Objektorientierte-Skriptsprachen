import json
import os

LEADERBOARD_FILE = "leaderboard.json"

def load_scores():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_score(name, time_left):
    scores = load_scores()
    scores.append({"name": name, "time": time_left})
    scores = sorted(scores, key=lambda x: x["time"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(scores, f, indent=4)
