import uuid
import subprocess
from flask import Flask, request, render_template, send_file, jsonify

app = Flask(name)

VOICE = "fa-IR-FaridNeural"

# =========================
# صفحه اصلی
# =========================

@app.route("/")
def index():
    return render_template("index.html")

# =========================
# فقط TTS
# =========================

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "متن خالی است"}), 400

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

# اجرای لوکال
if name == "main":
    app.run(host="0.0.0.0", port=5000)
