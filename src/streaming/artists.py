"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

from .tracks import  Track
from typing import List


class Artist:
    def __init__(self,artist_id: str,name: str,genre: str):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks : List[Track] = []

    def add_track (self, track: Track)->None:
        if track not in self.tracks:
            self.tracks.append(track)
    def track_count (self):
        return len(self.tracks)



