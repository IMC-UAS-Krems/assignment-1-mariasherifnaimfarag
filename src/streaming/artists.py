"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

from .tracks import Track


class Artist:
    def __init__(self,artist_id: str,name: str,genre: str):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = []

    def add_track (self, track: Track)->None:
        self.tracks.append(track)
    def track_count (self):
        return len(self.tracks)


