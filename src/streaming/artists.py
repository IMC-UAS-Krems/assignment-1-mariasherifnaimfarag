"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""
from __future__ import annotations # MUST be the first line of the file
from typing import TYPE_CHECKING , List
if TYPE_CHECKING:
    from .tracks import Track



class Artist:
    def __init__(self,artist_id: str,name: str,genre: str):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks : List["Track"] = []

    def add_track (self, track: "Track")->None:
        if track not in self.tracks:
            self.tracks.append(track)
    def track_count (self):
        return len(self.tracks)



