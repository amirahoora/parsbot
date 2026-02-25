from flask import Flask, request, jsonify, render_template, send_file
import requests
import uuid
import os

app = Flask(__name__)

# سه توکن برای فال‌بک
TOKENS = [
    "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",
    "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",
    "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"
]

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

VOICE = "fa-IR-FaridNeural"


def send_request_with_fallback(data):
    """سیستم فال‌بک سه‌توکنی"""
    for token in TOKENS:
        try:
            response = requests.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json=data,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()

        except Exception as e:
            print("Token failed:", token, e)
            continue

    return {"error": "All tokens failed"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    result = send_request_with_fallback(data)
    return jsonify(result)


@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "")
    if not text:
        return {"error": "متن خالی است"}, 400

    filename = f"voice_{uuid.uuid4().hex}.mp3"

    os.system(
        f'edge-tts --text "{text}" --voice {VOICE} --write-media {filename}'
    )

    return send_file(filename, mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(debug=True)
