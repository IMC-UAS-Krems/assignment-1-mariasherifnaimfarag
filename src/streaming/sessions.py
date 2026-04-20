"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""
from .users import User
from .tracks import Track
from datetime import datetime

class ListeningSession:
    """Its for a single listening event of a user that plays a track"""
    def __init__(self,session_id: str,user: User,track: Track,timestamp: datetime,duration_listened_seconds: int):
        """
              Initializes a listening session

              Arguments:
                  session_id: identifier(unique)
                  user: user who listens to the session
                  track: played track
                  timestamp: the certain time of the listening session
                  duration_listened_seconds: time in seconds
              """

        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_listened_seconds

    def duration_listened_minutes (self)->float:
        """Converts duration  to minutes"""
        return self.duration_listened_seconds / 60
