"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""


from abc import ABC
"""https://www.geeksforgeeks.org/python/abstract-classes-in-python/"""
from .artists import Artist
from datetime import date
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .albums import Album



class Track(ABC):
    """Base class for all music content (songs, podcasts, audiobooks)."""
    def __init__(self,track_id:str,title: str,duration_seconds: int,genre:str):
        """
              Initialize a track.

              Args:
                  track_id: identifier (unique).
                  title: track title.
                  duration_seconds: time in seconds.
                  genre: type of music.
              """
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    """Convert the seconds to minutes."""
    def duration_minutes(self) -> float:
        return self.duration_seconds / 60.0

    """if the ids match the tracks are equal"""
    def __eq__(self,other)->bool:
        if not isinstance(other,Track):
            return False
        return self.track_id == other.track_id

class Song(Track):
    """A music track made by an artist."""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist: Artist):
        """for initializing the song"""
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist



class SingleRelease(Song):
    """A song release is not part of an album."""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str,
                 artist: Artist, release_date: date):
        """initializes a single release."""
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date

class AlbumTrack(Song):
    """song that belongs to an album."""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str,artist: Artist,track_number: int,album:"Optional[Album]" = None):
        """initializes an album track."""
        super().__init__(track_id, title, duration_seconds, genre,artist)
        self.track_number = track_number
        self.album = album

class Podcast(Track):
    """Base class for the episodes of the podcast."""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str,host: str,description: str=""):
        """initializes a podcast."""
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description

class InterviewEpisode(Podcast):
    """Podcast episode that focuses on an interview with a guest."""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str,host: str,guest: str,description: str=""):
        """initializes a interview episode."""
        super().__init__(track_id, title, duration_seconds,genre,host,description)
        self.guest = guest
class NarrativeEpisode(Podcast):
    """ podcast with a story style episode with season/episode numbering."""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str,host: str,season: int,episode_number: int,description: str=""):
        """initializes a narrative episode."""
        super().__init__(track_id, title, duration_seconds, genre,host,description)
        self.season = season
        self.episode_number = episode_number

class AudiobookTrack(Track):
    """A style of an audiobook."""
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, author: str,narrator: str):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator













