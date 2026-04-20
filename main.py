from flask import Flask, request
import schedule
import threading
import time
import os
import shutil
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

from monitor import subscribe_to_channel, load_seen, save_seen
from extractor import download_video
from frame_extractor import extract_frames
from code_finder import scan_all_frames
from notifier import send_email
from logger import log_result

load_dotenv()

app = Flask(__name__)

CHANNEL_ID = os.getenv("CHANNEL_ID")
CALLBACK_URL = os.getenv("CALLBACK_URL")


def process_video(video):
    print(f"\n🎬 Processing: {video['title']}")
    video_path = None
    try:
        video_path = download_video(video["url"])
        frame_paths = extract_frames(video_path)
        codes = scan_all_frames(frame_paths)
        log_result(video, codes)

        if codes:
            send_email(video["title"], video["url"], codes)
        else:
            print("   ⏭️ No codes found — skipping notification")

    except Exception as e:
        print(f"   ❌ Error processing video: {e}")
    finally:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
        shutil.rmtree("frames", ignore_errors=True)


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # YouTube verifies endpoint on subscription
    if request.method == "GET":
        return request.args.get("hub.challenge", ""), 200

    # New video notification received
    if request.method == "POST":
        try:
            data = request.data.decode("utf-8")
            root = ET.fromstring(data)
            ns = {
                "yt": "http://www.youtube.com/xml/schemas/2015",
                "atom": "http://www.w3.org/2005/Atom"
            }

            for entry in root.findall("atom:entry", ns):
                video_id = entry.find("yt:videoId", ns).text
                title = entry.find("atom:title", ns).text
                url = entry.find("atom:link", ns).attrib.get("href")

                seen = load_seen()
                if video_id not in seen:
                    seen.add(video_id)
                    save_seen(seen)
                    video = {"id": video_id, "title": title, "url": url}
                    threading.Thread(target=process_video, args=(video,)).start()

        except Exception as e:
            print(f"❌ Webhook parse error: {e}")

        return "OK", 200


def renew_subscription():
    print("🔄 Renewing YouTube subscription...")
    subscribe_to_channel(CHANNEL_ID, CALLBACK_URL)


def run_scheduler():
    schedule.every(9).days.do(renew_subscription)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    print("🚀 YouTube Code Hunter is running...")
    subscribe_to_channel(CHANNEL_ID, CALLBACK_URL)
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
