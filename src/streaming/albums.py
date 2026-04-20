"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
from .artists import Artist
from typing import List , Set
from .tracks import AlbumTrack



class Album :
    """ tracks released together by an artist."""
    def __init__(self,album_id: str,title: str, artist: Artist,release_year: int):
        """
              Initialize an album.

              Args:
                  album_id: identifier(unique)
                  title: Album title.
                  artist: Artist who made the album.
                  release_year: release of the year.
              """
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks: List[AlbumTrack] =[]

    def add_track(self,track: AlbumTrack)->None:
        """ Add a track to the album and keep it in an order."""
        track.album = self #this for the album that it always belongs to the track
        self.tracks.append(track)
        self.tracks.sort(key=lambda t: t.track_number)



    def track_ids(self)->Set[str]:
        """Return all the track IDs in the album."""
        return {track.track_id for track in self.tracks}

    def duration_seconds(self)->int:
        """Calculate total duration in seconds of the album."""
        return sum(track.duration_seconds for track in self.tracks)





