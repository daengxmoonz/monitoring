from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/", methods=["POST"])
def receive_alert():
    data = request.json
    # Build a concise message
    alerts = data.get("alerts", [])
    messages = []
    for a in alerts:
        status = a.get("status", "firing")
        labels = a.get("labels", {})
        annotations = a.get("annotations", {})
        summary = annotations.get("summary", "")
        description = annotations.get("description", "")
        msg = f"[{status.upper()}] {labels.get('alertname','')}\n{summary}\n{description}"
        messages.append(msg)

    text = "\n\n".join(messages)[:4000]  # Telegram limit safety
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    r = requests.post(TELEGRAM_API, json=payload)
    return jsonify({"status": "ok", "telegram_status": r.status_code}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
