import feedparser
import json
import os
import requests


def get_new_videos(channel_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(url)
    seen = load_seen()
    new_videos = []

    for entry in feed.entries:
        video_id = entry.yt_videoid
        if video_id not in seen:
            new_videos.append({
                "id": video_id,
                "title": entry.title,
                "url": entry.link,
                "published": entry.published
            })
            seen.add(video_id)

    save_seen(seen)
    return new_videos


def load_seen():
    if os.path.exists("seen_videos.json"):
        with open("seen_videos.json") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open("seen_videos.json", "w") as f:
        json.dump(list(seen), f)


def subscribe_to_channel(channel_id, callback_url):
    response = requests.post(
        "https://pubsubhubbub.appspot.com/subscribe",
        data={
            "hub.mode": "subscribe",
            "hub.topic": f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
            "hub.callback": callback_url,
            "hub.verify": "async",
            "hub.lease_seconds": 864000
        }
    )
    if response.status_code == 202:
        print(f"Subscribed to channel: {channel_id}")
    else:
        print(f"Subscription failed: {response.status_code}")
