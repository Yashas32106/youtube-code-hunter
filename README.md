# YouTube Code Hunter 🎯

Watches a YouTube channel, scans new videos frame-by-frame using OCR,
detects promo codes in XXXX-XXXXXX-XXXX format, and emails them to you instantly.

---

## 📋 Claude Code Prompt

Copy and paste the following prompt into Claude Code:

---

I have a YouTube promo code hunter project ready to deploy. The project watches
a YouTube channel, downloads new videos, extracts frames, runs OCR to find promo
codes in XXXX-XXXXXX-XXXX format, and emails them to me automatically.

Please do the following steps in order:

1. Install all Python dependencies from requirements.txt
2. Install system dependencies: ffmpeg and tesseract-ocr
3. Ask me for my credentials and fill in the .env file:
   - EMAIL_ADDRESS (my Gmail address)
   - EMAIL_PASSWORD (my Gmail App Password)
   - RECIPIENT_EMAIL (where to send found codes)
   - CHANNEL_ID (the YouTube channel ID to monitor)
4. Test the OCR pipeline on a YouTube video URL I will provide
5. Initialize a git repo, create a GitHub repository, and push the project
6. Deploy to Railway and get the public webhook URL
7. Update CALLBACK_URL in the Railway environment variables with the live URL
8. Run the webhook subscription to register with YouTube's PubSubHubbub hub
9. Confirm everything is live by checking the Railway logs

---

## 📁 Project Files

- main.py           — Flask webhook server + pipeline orchestrator
- monitor.py        — YouTube RSS feed watcher + WebSub subscription
- extractor.py      — Video downloader via yt-dlp
- frame_extractor.py — Smart frame extraction via OpenCV
- code_finder.py    — OCR + regex code detection
- notifier.py       — Gmail email sender
- logger.py         — Results logging
- requirements.txt  — Python dependencies
- Procfile          — Railway start command
- .env              — Your credentials (fill this in)

---

## 🔐 Getting Your Gmail App Password

1. Go to myaccount.google.com
2. Security → 2-Step Verification (must be enabled)
3. Search "App Passwords" → Generate one for "Mail"
4. Use that 16-character password as EMAIL_PASSWORD

## 🔍 Finding a YouTube Channel ID

1. Go to the YouTube channel page
2. Right-click → View Page Source
3. Search for "channelId" → copy the value (starts with UC...)
