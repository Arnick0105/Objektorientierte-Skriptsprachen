import json
import os

LEADERBOARD_FILE = "leaderboard.json"

def load_scores():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        scores = json.load(f)

    scores.sort(key = lambda entry: entry["Score"], reverse = True)
    return scores

def save_score(name, score):
    scores = load_scores()
    scores.append({"name": name, "Score": score})
    scores = sorted(scores, key=lambda x: x["Score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(scores, f, indent=4)
