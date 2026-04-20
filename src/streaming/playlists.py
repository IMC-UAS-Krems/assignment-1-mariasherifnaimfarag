"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
from .tracks import Track
from .users import User
from typing import List
class Playlist:
    def __init__(self,playlist_id: str,name: str,owner: User):
        """
                  Initialize a playlist.

                  Args:
                      playlist_id: identifier(unique).
                      name: name of the playlist.
                      owner: the owner(user) of the playlist.
                  """
        self.playlist_id=playlist_id
        self.name=name
        self.owner=owner
        self.tracks : List[Track] = []

    def add_track(self,track)->None:
       """Add a track if it does not exist already in the playlist."""
       if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self,track_id)->None:
        """ Remove a track with its certain ID"""
        for track in self.tracks:
            if track.track_id == track_id:
                self.tracks.remove(track)
                break

    def total_duration_seconds(self)->int:
        """Calculate total duration in seconds of all tracks."""
        return sum(track.duration_seconds for track in self.tracks)

class CollaborativePlaylist(Playlist):
    """A playlist that lets multiple users to contribute."""
    def __init__(self, playlist_id: str, name: str, owner: User):
        """initializing a collaborative playlist."""
        super().__init__(playlist_id, name, owner)
        self.contributors: List[User] = [owner]

    def add_contributor(self,user)->None:
       """ add a contributor to the playlist."""
       if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self,user)->None:
        """ Remove a contributor but the owner can not be removed"""
        if user == self.owner:
            return
        if user in self.contributors:
            self.contributors.remove(user)

