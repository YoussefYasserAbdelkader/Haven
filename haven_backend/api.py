import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re

class AssistantFnc:
    def __init__(self):
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
        ))

    def should_play_music(self, text: str) -> bool:
        music_keywords = ["play music", "music", "song", "tune", "playlist"]
        return any(kw in text.lower() for kw in music_keywords)

    def extract_song_name(self, text: str) -> str | None:
        match = re.search(r"play (.+)", text.lower())
        return match.group(1) if match else None

    def analyze_sentiment(self, text: str) -> str:
        # Placeholder sentiment logic
        sad_keywords = ["sad", "down", "depressed", "tired", "lonely"]
        happy_keywords = ["happy", "great", "excited", "good"]
        if any(word in text.lower() for word in sad_keywords):
            return "sad"
        elif any(word in text.lower() for word in happy_keywords):
            return "happy"
        return "neutral"

    def recommend_music(self, mood: str):
        if mood == "sad":
            query = "calm acoustic"
        elif mood == "happy":
            query = "energetic hits"
        else:
            query = "ambient focus"
        results = self.spotify.search(q=query, type='playlist', limit=1)
        if results["playlists"]["items"]:
            uri = results["playlists"]["items"][0]["uri"]
            self.spotify.start_playback(context_uri=uri)

    def handle_user_text(self, text: str):
        mood = self.analyze_sentiment(text)
        print(f"[Sentiment] Detected mood: {mood}")
        if self.should_play_music(text):
            song = self.extract_song_name(text)
            if song:
                results = self.spotify.search(q=song, type='track', limit=1)
                if results["tracks"]["items"]:
                    uri = results["tracks"]["items"][0]["uri"]
                    self.spotify.start_playback(uris=[uri])
                    print(f"[Spotify] Playing song: {song}")
            else:
                self.recommend_music(mood)
