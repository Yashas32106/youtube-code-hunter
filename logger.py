import json
from datetime import datetime


def log_result(video, codes):
    entry = {
        "title": video["title"],
        "url": video["url"],
        "processed_at": datetime.now().isoformat(),
        "codes_found": codes,
        "notified": len(codes) > 0
    }
    with open("results_log.json", "a") as f:
        json.dump(entry, f)
        f.write("\n")

    status = f"✅ {len(codes)} code(s)" if codes else "⏭️ No codes"
    print(f"   {status} — {video['title']}")
