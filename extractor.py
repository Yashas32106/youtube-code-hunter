import yt_dlp


def download_video(video_url, output_path="video"):
    ydl_opts = {
        "format": "best[height<=720][ext=mp4]/best[ext=mp4]/best",
        "outtmpl": f"{output_path}.mp4",
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return f"{output_path}.mp4"
