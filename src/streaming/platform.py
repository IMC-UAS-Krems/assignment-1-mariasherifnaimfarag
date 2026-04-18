"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from typing import   Dict , List
from streaming.sessions import ListeningSession
from streaming.tracks import Track , Song
from streaming.users import User , PremiumUser, FamilyMember
from streaming.artists import Artist
from streaming.playlists import Playlist , CollaborativePlaylist
from streaming.albums import Album
from datetime import datetime , timedelta


class StreamingPlatform:
    def __init__(self,name: str):
        self.name = name
        self._catalogue: Dict[str, Track] = {}
        self._users: Dict[str, User] = {}
        self._artists: Dict[str, Artist] = {}
        self._albums: Dict[str, Album] = {}
        self._playlists: Dict[str, Playlist] = {}
        self._sessions: List[ListeningSession]= []
#q1 total_listening_time_minutes
    def total_listening_time_minutes(self,start: datetime, end: datetime) -> float:

        total_seconds = 0.0

        for session in self._sessions:
            if hasattr(session, "timestamp") and start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds

        return float(total_seconds / 60.0)


#q2 avg_unique_tracks_per_premium_user
    def avg_unique_tracks_per_premium_user(self,days: int = 30) -> float:
        premium_users = [
            user for user in self._users.values()
            if isinstance(user, PremiumUser)
        ]

        if not premium_users:
            return 0.0

        cutoff = datetime.now() - timedelta(days=days)

        total_unique_tracks = 0

        for user in premium_users:
            unique_tracks = set()

            for session in self._sessions:
                if session.user == user and session.timestamp >= cutoff:
                    unique_tracks.add(session.track.track_id)

            total_unique_tracks += len(unique_tracks)

        return total_unique_tracks / len(premium_users)
#q3 track_with_most_distinct_listeners
    def track_with_most_distinct_listeners(self) -> Track | None:
        if not self._sessions:
            return None

        listeners = {}

        for session in self._sessions:
            track_id = session.track.track_id

            if track_id not in listeners:
                listeners[track_id] = set()

            listeners[track_id].add(session.user.user_id)

        best_track_id = max(listeners, key=lambda t: len(listeners[t]))

        return self._catalogue.get(best_track_id)
#q4 avg_session_duration_by_user_type
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        times={}
        for session in self._sessions:
            user_type = type(session.user).__name__

            if user_type not in times:
                times[user_type] = [0.0, 0]

            times[user_type][0] += session.duration_listened_seconds
            times[user_type][1] += 1

            # IMPORTANT: ensure missing types appear as 0
        all_types = ["FreeUser", "PremiumUser", "FamilyAccountUser", "FamilyMember"]

        results = []
        for t in all_types:
            if t in times and times[t][1] > 0:
                avg = times[t][0] / times[t][1]
            else:
                avg = 0.0
            results.append((t, avg))

        return sorted(results, key=lambda x: x[1], reverse=True)

#q5 total_listening_time_underage_sub_users_minutes
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        return sum(
            s.duration_listened_seconds / 60.0
            for s in self._sessions
            if isinstance(s.user, FamilyMember) and s.user.age < age_threshold
        )

#q6 top_artists_by_listening_time
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        artist_times = {}

        for s in self._sessions:
            if isinstance(s.track, Song):
                artist = s.track.artist
                artist_times[artist] = artist_times.get(artist, 0.0) + s.duration_listened_minutes()

        sorted_artists = sorted(artist_times.items(), key=lambda x: x[1], reverse=True)

        return sorted_artists[:n]
#q7 user_top_genre
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None :
        user = self._users.get(user_id)
        if not user or not user.sessions:
            return None

        genre_times = {}
        total = 0.0

        for s in user.sessions:
            minutes = s.duration_listened_seconds / 60.0
            genre = s.track.genre

            genre_times[genre] = genre_times.get(genre, 0.0) + minutes
            total += minutes

        if total == 0:
            return None

        top_genre, top_time = max(genre_times.items(), key=lambda x: x[1])

        return top_genre, (top_time / total) * 100
#q8 collaborative_playlists_with_many_artists
    def collaborative_playlists_with_many_artists(self,threshold: int = 3) -> list[CollaborativePlaylist]:

            result = []

            for playlist in self._playlists.values():
                if isinstance(playlist, CollaborativePlaylist):
                    artists_in_playlist = set()

                    for track in playlist.tracks:
                        if isinstance(track, Song):
                            artists_in_playlist.add(track.artist.artist_id)

                    if len(artists_in_playlist) > threshold:
                        result.append(playlist)

            return result


#q9 avg_tracks_per_playlist_type
    def avg_tracks_per_playlist_type(self) -> dict[str, float] :
        p_total = p_count = 0
        cp_total = cp_count = 0

        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                cp_total += len(playlist.tracks)
                cp_count += 1
            else:
                p_total += len(playlist.tracks)
                p_count += 1

        return {
            "Playlist": (p_total / p_count) if p_count > 0 else 0.0,
            "CollaborativePlaylist": (cp_total / cp_count) if cp_count > 0 else 0.0
        }
#q10 users_who_completed_albums
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        results = []
        for user in self.all_users():
            user_listened_ids = user.unique_tracks_listened()
            completed_album_titles = []

            for album in self._albums.values():
                album_track_ids = album.track_ids()

                if len(album_track_ids) > 0:
                    if album_track_ids.issubset(user_listened_ids):
                        completed_album_titles.append(album.title)

            if completed_album_titles:
                results.append((user, completed_album_titles))

        return results










    def add_track (self,track: 'Track')->None:
        self._catalogue[track.track_id]=track
    def add_user(self,user: 'User')->None:
        self._users[user.user_id]=user
    def add_artist(self,artist: 'Artist')->None:
        self._artists[artist.artist_id]=artist
    def add_album(self,album: 'Album')->None:
        self._albums[album.album_id]=album
    def add_playlist(self,playlist: 'Playlist')->None:
        self._playlists[playlist.playlist_id]=playlist
    def record_session(self,session: 'ListeningSession')->None:
        self._sessions.append(session)
        session.user.add_session(session)
    def get_track(self,track_id: str)->Track | None:
        return self._catalogue.get(track_id)
    def get_user(self,user_id: str)->User| None:
        return self._users.get(user_id)
    def get_artist(self,artist_id=None)->Artist | None:
        return self._artists.get(artist_id)
    def get_album(self,album_id)->Album | None:
        return self._albums.get(album_id)
    def all_users(self)-> List[User]:
        return list(self._users.values())
    def all_tracks(self)-> List[Track]:
        return list(self._catalogue.values())






