"""
Ye main script hai — topic se content generate karke Blogger par publish karta hai.

Chalane ka tareeqa:
    python main.py "Your Topic Here"

Agar koi topic na dein, to ye khud topics.json list se agla pending topic utha lega.
"""

import sys
import json
from datetime import datetime

from content_generator import generate_blog_post
from blogger_publish import publish_post

TOPICS_FILE = "topics.json"
LOG_FILE = "publish_log.json"


def load_next_topic():
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics = json.load(f)

    for item in topics:
        if item["status"] == "pending":
            return item, topics

    return None, topics


def mark_topic_done(topics, topic_text):
    for item in topics:
        if item["topic"] == topic_text:
            item["status"] = "published"
            item["published_at"] = datetime.now().isoformat()
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)


def log_result(topic_text, result):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log = json.load(f)
    except FileNotFoundError:
        log = []

    log.append({
        "topic": topic_text,
        "url": result.get("url"),
        "published_at": datetime.now().isoformat(),
    })

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def main():
    # Agar command line se topic diya gaya hai to wahi use karein
    if len(sys.argv) > 1:
        topic_text = " ".join(sys.argv[1:])
        topics = None
    else:
        # Warna topics.json se agla pending topic uthayein
        next_item, topics = load_next_topic()
        if next_item is None:
            print("Koi pending topic nahi mila topics.json me. Sab publish ho chuke hain!")
            return
        topic_text = next_item["topic"]

    print(f"📝 Generating content for: {topic_text}")
    post = generate_blog_post(topic_text)

    print("🚀 Publishing to Blogger...")
    result = publish_post(title=post["title"], html_content=post["html_content"], publish=True)

    print(f"✅ Published! Live URL: {result.get('url')}")

    log_result(topic_text, result)

    if topics is not None:
        mark_topic_done(topics, topic_text)


if __name__ == "__main__":
    main()
