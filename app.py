import uuid
import subprocess
from flask import Flask, request, render_template, send_file, jsonify

app = Flask(__name__)

VOICE = "fa-IR-FaridNeural"

# =========================
# صفحه اصلی (HTML شما)
# =========================
@app.route("/")
def index():
    return render_template("index.html")

# =========================
# TTS فقط برای صدا
# =========================
@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "متن خالی است"}), 400

    # مسیر مخصوص Render (باید /tmp باشد)
    filename = f"/tmp/voice_{uuid.uuid4().hex}.mp3"

    try:
        subprocess.run(
            [
                "edge-tts",
                "--text", text,
                "--voice", VOICE,
                "--write-media", filename
            ],
            check=True
        )
    except Exception as e:
        print("TTS Error:", e)
        return jsonify({"error": "خطا در تولید صدا"}), 500

    return send_file(filename, mimetype="audio/mpeg")
