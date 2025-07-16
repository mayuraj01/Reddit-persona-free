import os
from typing import List, Dict
from dotenv import load_dotenv
import praw

load_dotenv()

def _reddit() -> praw.Reddit:
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "persona-script"),
    )

def fetch_history(username: str, limit: int) -> List[Dict]:
    """Return last `limit` comments + last `limit` posts as a list of dicts."""
    reddit = _reddit()
    redditor = reddit.redditor(username)
    items: List[Dict] = []

    for c in redditor.comments.new(limit=limit):
        print(f"[{c.author}] {c.body[:200]}")
        items.append({
            "type": "comment",
            "body": c.body,
            "permalink": f"https://www.reddit.com{c.permalink}",
    })

    for s in redditor.submissions.new(limit=limit):
        items.append(
            {
                "type": "post",
                "body": f"{s.title}\n{s.selftext}",
                "permalink": f"https://www.reddit.com{s.permalink}",
            }
        )
    return items
