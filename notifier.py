import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime


def send_email(video_title, video_url, codes):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL")

    code_list = "\n".join(f"  • {code}" for code in codes)

    body = f"""
🎬 New Video: {video_title}
🔗 {video_url}
🕐 Detected at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

🎟️ Codes Found:
{code_list}

Good luck! 🤞
    """

    msg = MIMEText(body)
    msg["Subject"] = f"[Code Hunter] {len(codes)} code(s) found in: {video_title}"
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"   📧 Email sent with {len(codes)} code(s)")
