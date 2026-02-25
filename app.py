import threading
import asyncio
import uuid
import webview
from flask import Flask, request, send_file, render_template
import edge_tts

app = Flask(__name__)

VOICE = "fa-IR-FaridNeural"

# ---------- تولید صدا ----------
async def generate_voice(text, filename):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

def run_async(coro):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        return asyncio.run_coroutine_threadsafe(coro, loop).result()
    else:
        return loop.run_until_complete(coro)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")

    if not text:
        return {"error": "متن خالی است"}, 400

    filename = f"voice_{uuid.uuid4().hex}.mp3"
    run_async(generate_voice(text, filename))
    return send_file(filename, mimetype="audio/mpeg")

# ---------- اجرای Flask در بکگراند ----------
def start_flask():
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)

flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()

webview.create_window(
    "پارس بات",
    "http://127.0.0.1:5001",
    width=1200,
    height=800
)

webview.start()
