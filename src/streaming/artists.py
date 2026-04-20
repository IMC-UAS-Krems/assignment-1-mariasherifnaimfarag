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
    """this  for a musician or content creator on the platform."""
    def __init__(self,artist_id: str,name: str,genre: str):
        """
              Initialize an artist.

              Args:
                  artist_id: identifier(unique.
                  name: name of the artist.
                  genre: main genre.
              """
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks : List["Track"] = []

    def add_track (self, track: "Track")->None:
        """ Add a track to the artist if its not already there"""
        if track not in self.tracks:
            self.tracks.append(track)
    def track_count (self):
        """Return number of tracks for this certain  artist."""
        return len(self.tracks)



