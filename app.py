import asyncio
import uuid
from flask import Flask, request, send_file, render_template
import edge_tts

app = Flask(__name__)

# ---------- صدای پیش‌فرض ----------
VOICE = "fa-IR-FaridNeural"  # صدای مرد فارسی، خودش چندزبانه را تقریبا پشتیبانی می‌کند

# ---------- تولید صدا ----------
async def generate_voice(text, filename):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

# ---------- روت HTML ----------
@app.route("/")
def index():
    return render_template("index.html")  # HTML پلیر خودت

# ---------- روت TTS ----------
@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")

    if not text:
        return {"error": "متن خالی است"}, 400

    filename = f"voice_{uuid.uuid4().hex}.mp3"
    asyncio.run(generate_voice(text, filename))
    return send_file(filename, mimetype="audio/mpeg")

# ---------- اجرا سرور ----------
app.run(host="0.0.0.0", port=5001, debug=True)
