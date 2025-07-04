import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

class SpotifyController:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
        ))

    def play_song(self, query: str):
        results = self.sp.search(q=query, limit=1, type="track")
        tracks = results.get("tracks", {}).get("items", [])
        if tracks:
            track = tracks[0]
            self.sp.start_playback(uris=[track["uri"]])
            return f"🎵 Playing: {track['name']} by {track['artists'][0]['name']}"
        return "❌ Sorry, I couldn't find that song."

    def pause(self):
        self.sp.pause_playback()
        return "⏸️ Paused Spotify playback."

    def resume(self):
        self.sp.start_playback()
        return "▶️ Resumed Spotify playback."

    def recommend_playlist(self, mood: str):
        mood_map = {
            "relaxing": "lofi chill",
            "happy": "happy hits",
            "sad": "sad songs",
            "energetic": "workout",
            "romantic": "love songs"
        }
        query = mood_map.get(mood.lower(), "chill")
        results = self.sp.search(q=query, type="playlist", limit=1)
        playlists = results.get("playlists", {}).get("items", [])
        if playlists:
            playlist = playlists[0]
            self.sp.start_playback(context_uri=playlist["uri"])
            return f"📻 Playing playlist: {playlist['name']}"
        return "❌ Couldn't find a playlist for that mood."

def control_spotify_if_needed(user_text: str):
    controller = SpotifyController()
    text = user_text.lower()

    if "pause" in text:
        return controller.pause()
    elif "resume" in text or "continue" in text:
        return controller.resume()
    elif "play" in text and "playlist" in text:
        # Extract mood keyword
        for mood in ["relaxing", "happy", "sad", "energetic", "romantic"]:
            if mood in text:
                return controller.recommend_playlist(mood)
        return controller.recommend_playlist("chill")
    elif "play" in text:
        # Try to play a specific song name
        song = text.replace("play", "").strip()
        return controller.play_song(song)

    return None  
