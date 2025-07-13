Absolutely! Here's a well-structured and professional README.md for your Haven voice therapy assistant project, incorporating all the key features like voice input/output, Claude local model, sentiment-aware responses, and Spotify control:

---

# 🎧 Haven – Your Compassionate Voice Therapy Assistant

Haven is a real-time, voice-enabled AI therapy assistant built with LiveKit Agents, local LLMs (Claude-compatible), Whisper for STT, and sentiment-aware conversation. It also supports voice-controlled Spotify integration to provide music therapy as part of the experience.

---

## 💡 Features

* 🎤 Real-time voice input using Whisper via LiveKit Agents
* 🧠 Local LLM (e.g., Nous Hermes 2) for private, empathetic responses
* 🔈 Instant TTS (text-to-speech) responses for streaming therapy replies
* ❤️ Sentiment-aware responses: soothing tone for sadness, gentle celebration for positivity
* 🎵 Spotify integration: recommend/play/pause music using voice commands
* 🔒 Completely private – runs locally without any OpenAI or cloud dependencies

---

## 🛠️ Tech Stack

| Layer         | Technology                                   |
| ------------- | -------------------------------------------- |
| STT           | Whisper via LiveKit Agents                   |
| TTS           | ElevenLabs / local TTS engine                |
| AI Model      | Nous Hermes 2 (Claude-compatible) via Ollama |
| Voice Control | LiveKit Realtime Audio Agents                |
| Frontend      | Vite + React (App.jsx entry point)           |
| Backend       | FastAPI + Python (`api.py`, `agent.py`)      |
| Spotify       | Spotipy SDK (OAuth2 auth + playback control) |

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourname/haven-therapy.git
cd haven-therapy
```

---

### 2. Environment Setup

Create a `.env` file in both the backend and frontend folders.

#### `.env` (backend):

```env
LIVEKIT_URL=wss://your-livekit-url.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

LM_API_URL=http://localhost:11434/v1  # Ollama running Nous Hermes 2

SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

---

### 3. Run Backend

Install requirements and start the FastAPI server:

```bash
cd haven_backend
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 3000
```

To run the LiveKit agent worker:

```bash
python agent.py
```

Ensure your Claude-compatible model (e.g., Nous Hermes 2) is running with Ollama:

```bash
ollama run nous-hermes2
```

---

### 4. Run Frontend

```bash
cd haven_frontend
npm install
npm run dev
```

This should launch the app at `http://localhost:5173`.

---

## 🗣️ How It Works

* Press and hold the 🎤 "Hold to talk" button
* Whisper transcribes your voice and sends it to the LLM
* The LLM generates an emotionally aware response
* The response is converted to voice and streamed back in real time
* If you're feeling down, Haven may recommend a Spotify playlist
* You can also say:

  * “Play \[song name]”
  * “Pause music”
  * “Skip track”
  * “Play relaxing music”
  * etc.

---

## 📁 Project Structure

```
haven/
├── haven_backend/
│   ├── api.py
│   ├── agent.py
│   ├── prompts.py
│   ├── requirements.txt
│   └── .env
├── haven_frontend/
│   ├── App.jsx
│   ├── main.jsx
│   ├── components/
│   │   └── ChatWindow.jsx
│   ├── styles/
│   │   ├── app.css
│   │   └── ChatWindow.css
│   └── .env
```

---

## 🧠 Model Notes

We use `nous-hermes2:10.7b` via Ollama for empathetic dialogue. For better speed, you may switch to a smaller Claude-compatible model (e.g., TinyLlama, Mistral) and update the `LM_API_URL`.

---

## 💬 Voice Commands for Spotify

| Command                | Action                   |
| ---------------------- | ------------------------ |
| “Play \[song name]”    | Starts Spotify playback  |
| “Pause music”          | Pauses playback          |
| “Resume” or “Continue” | Resumes playback         |
| “Next” or “Skip track” | Skips to next track      |
| “Play relaxing music”  | Plays a calming playlist |

---

## 🧪 Troubleshooting

* If voice doesn’t play, check browser permissions for microphone/speaker
* Make sure your Spotify is open and playing on a device
* Use `ollama list` to verify that your model is running
* Keep responses under 10 seconds for optimal TTS streaming

---

## 📄 License

MIT – use it freely, improve it, and share the calm 💚

