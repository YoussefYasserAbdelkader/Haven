import os
import asyncio
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from agent import ClaudeRealtimeModel
from gtts import gTTS
import whisper
from spotify_control import control_spotify_if_needed  

load_dotenv()

app = Flask(__name__)
CORS(app)

AUDIO_FOLDER = os.path.join(os.getcwd(), "audio")
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Load env vars properly
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")

# Load Whisper model
whisper_model = whisper.load_model("base")

# Init Claude voice agent
model = ClaudeRealtimeModel(
    instructions="You are Haven, a compassionate voice therapist.",
    voice="shimmer",
    temperature=0.7,
    modalities=["audio", "text"]
)

@app.route("/start", methods=["POST"])
def start():
    print("🎙️ Conversation started from frontend.")

    # Save uploaded audio
    audio_file = request.files['audio']
    audio_path = os.path.join(AUDIO_FOLDER, "user_audio.webm")
    audio_file.save(audio_path)

    # Transcribe audio
    result = whisper_model.transcribe(audio_path)
    user_text = result['text']
    print("📝 Transcribed:", user_text)

    # AI reply
    session = model.sessions[0]
    session.conversation.create({"role": "user", "content": user_text})
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        reply = loop.run_until_complete(
            asyncio.wait_for(session.response.create(), timeout=10)
        )
    except asyncio.TimeoutError:
        reply = "Sorry, I couldn't respond in time. Please try again."

    # TTS reply
    tts = gTTS(reply)
    audio_reply_path = os.path.join(AUDIO_FOLDER, "last_reply.mp3")
    tts.save(audio_reply_path)

    # Spotify
    control_spotify_if_needed(user_text)

    return jsonify({
        "user_text": user_text,
        "reply": reply,
        "audio_url": "/audio/last_reply.mp3"
    })

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == "__main__":
    app.run(port=3000, debug=True)
