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
        return sum(session.duration_listened_minutes()
                   for session in self._sessions
                    if start<= session.timestamp <= end)
#q2 avg_unique_tracks_per_premium_user
    def avg_unique_tracks_per_premium_user(self,days: int = 30) -> float:
        premium_users = [u for u in self._users.values() if isinstance(u, PremiumUser)]

        if not premium_users:
            return 0.0

        time_window = datetime.now() - timedelta(days=days)
        total_unique_tracks = 0
        for user in premium_users:
            unique_tracks = {
                session.track.track_id
                for session in user.sessions
                if session.timestamp >= time_window
            }
            total_unique_tracks += len(unique_tracks)
        return total_unique_tracks / len(premium_users)
#q3 track_with_most_distinct_listeners
    def track_with_most_distinct_listeners(self) -> Track | None:
        if not self._sessions:
            return None
        listener_map = {}

        for session in self._sessions:
            t_id = session.track.track_id
            u_id = session.user.user_id

            if t_id not in listener_map:
                listener_map[t_id] = set()

            listener_map[t_id].add(u_id)

        most_popular_id = max(listener_map, key=lambda tid: len(listener_map[tid]))

        return self._catalogue.get(most_popular_id)
#q4 avg_session_duration_by_user_type
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        times = {}
        for session in self._sessions:
            user_type_name = type(session.user).__name__
            if  user_type_name not in times:
                times[user_type_name] = [0.0, 0]
            times[user_type_name][0] += session.duration_listened_seconds
            times[user_type_name][1] += 1
        results = []
        for type_name, data in times.items():
                avg_seconds = data[0] / data[1]
                results.append((type_name, avg_seconds))
        results.sort(key=lambda item: item[1], reverse=True)
        return results

#q5 total_listening_time_underage_sub_users_minutes
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total_minutes = 0.0

        for session in self._sessions:
            if isinstance(session.user, FamilyMember) and session.user.age < age_threshold:
                total_minutes += session.duration_listened_seconds / 60.0

        return total_minutes

#q6 top_artists_by_listening_time
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        count = 0
        artist_times = {}
        for session in self._sessions:
            if isinstance(session.track, Song):
                artist = session.track.artist
                duration = session.duration_listened_minutes()
                artist_times[artist] = artist_times.get(artist, 0.0) + duration

        sorted_artists = sorted(artist_times.items(), key=lambda x: x[1], reverse=True)

        results = []
        for entry in sorted_artists:
            if count < n:
                results.append(entry)
                count += 1
            else:
                break
        return results
#q7 user_top_genre
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None :
        user = self._users.get(user_id)
        if not user or not user.sessions:
            return None

        total_time = user.total_listening_minutes()
        if total_time == 0:
            return None

        genre_times = {}
        for session in user.sessions:
            g = session.track.genre
            genre_times[g] = genre_times.get(g, 0.0) + session.duration_listened_minutes()

        top_genre, max_time = max(genre_times.items(), key=lambda item: item[1])

        percentage = (max_time / total_time) * 100
        return top_genre, percentage
#q8 collaborative_playlists_with_many_artists
    def collaborative_playlists_with_many_artists(self,threshold: int = 3) -> list[CollaborativePlaylist]:
        results = []
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                unique_artists = set()
                for track in playlist.tracks:
                    if isinstance(track, Song):
                        unique_artists.add(track.artist)

                if len(unique_artists) > threshold:
                    results.append(playlist)
        return results
#q9 avg_tracks_per_playlist_type
    def avg_tracks_per_playlist_type(self) -> dict[str, float] :
        p_total, p_num = 0, 0
        cp_total, cp_num = 0, 0
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                cp_total += len(playlist.tracks)
                cp_num += 1
            else:
                p_total += len(playlist.tracks)
                p_num += 1
        return {
            "Playlist": p_total / p_num if p_num > 0 else 0.0,
            "CollaborativePlaylist": cp_total / cp_num if cp_num > 0 else 0.0
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






