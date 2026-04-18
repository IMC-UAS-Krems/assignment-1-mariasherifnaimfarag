"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import (
    AlbumTrack,
    SingleRelease,
    InterviewEpisode,
    NarrativeEpisode,
    AudiobookTrack,
)
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


# ---------------------------------------------------------------------------
# Helper - timestamps relative to the real current time so that the
# "last 30 days" window in Q2 always contains RECENT sessions.
# ---------------------------------------------------------------------------
FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)   # well within 30-day window
OLD    = FIXED_NOW - timedelta(days=60)   # outside 30-day window


@pytest.fixture
def platform() -> StreamingPlatform:
    """Return a fully populated StreamingPlatform instance."""
    platform = StreamingPlatform("TestStream")

    # ------------------------------------------------------------------
    # Artists
    # ------------------------------------------------------------------
    pixels  = Artist("a1", "Pixels",    genre="pop")
    taylorswift = Artist("a2", "TaylorSwift", genre="pop")
    shakira = Artist("a3", "Shakira", genre="pop")
    billie = Artist("a4", "Billie", genre="pop")
    ariana = Artist("a5", "Ariana Grande", genre="pop")
    drake = Artist("a6", "Drake", genre="hip-hop")
    edsheeran = Artist("a7", "Ed Sheeran", genre="pop")
    dua = Artist("a8", "Dua Lipa", genre="pop")
    weeknd = Artist("a9", "The Weeknd", genre="r&b")
    coldplay = Artist("a10", "Coldplay", genre="alternative")
    for artist in (taylorswift,shakira, billie,ariana,drake,edsheeran,dua,weeknd,coldplay):
         platform.add_artist(artist)


    # ------------------------------------------------------------------
    # Albums & AlbumTracks
    # ------------------------------------------------------------------
    dd = Album("alb1", "Digital Dreams", artist=pixels, release_year=2022)
    t1 = AlbumTrack("t1", "Pixel Rain",      180, "pop",  pixels, track_number=1)
    t2 = AlbumTrack("t2", "Grid Horizon",    210, "pop",  pixels, track_number=2)
    t3 = AlbumTrack("t3", "Vector Fields",   195, "pop",  pixels, track_number=3)

    for track in (t1, t2, t3):
        dd.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(dd)

    d2=Album("alb2", "golden hits", artist=taylorswift, release_year=2022)
    t4=AlbumTrack("t1_3", "Blank space", 180, "pop", taylorswift, track_number=1)
    t5=AlbumTrack("t2_4", "cruel summer", 380, "pop", taylorswift, track_number=2)
    t6=AlbumTrack("t3_5","shake it off",450,"pop",taylorswift, track_number=3)
    for track in (t4, t5, t6):
        d2.add_track(track)
        platform.add_track(track)
        taylorswift.add_track(track)
    platform.add_album(d2)

    d3 = Album("alb3", "Dark Hours", artist=billie, release_year=2023)

    b1 = AlbumTrack("t4", "Midnight Silence", 200, "pop", billie, track_number=1)
    b2 = AlbumTrack("t5", "Broken Lights", 240, "pop", billie, track_number=2)
    b3 = AlbumTrack("t6", "Ocean Fear", 210, "pop", billie, track_number=3)

    for track in (b1, b2, b3):
        d3.add_track(track)
        platform.add_track(track)
        billie.add_track(track)

    platform.add_album(d3)




    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    alice = FreeUser("u1", "Alice",   age=30)
    bob   = PremiumUser("u2", "Bob",   age=25, subscription_start=date(2023, 1, 1))
    lily = PremiumUser("u3", "Lily", age=30, subscription_start=date(2023, 1, 1))
    father = FamilyAccountUser("u4", "Father", age=50)
    daughter = FamilyMember("u5", "daughter", age=15,parent=father)
    tom = FreeUser("u6", "Tom", age=22)

    emma = PremiumUser("u7", "Emma", age=28, subscription_start=date(2022, 5, 10))






    for user in (alice, bob,father, daughter,lily,tom,emma):
        platform.add_user(user)



    # ------------------------------------------------------------------
    # Listening sessions
    # ------------------------------------------------------------------
    s1 = ListeningSession("s1", alice, t1, RECENT, 180)
    s2 = ListeningSession("s2", bob, t2, RECENT, 200)
    s3 = ListeningSession("s3", father, t2, RECENT, 150)
    s4 = ListeningSession("s4", daughter, t3, OLD, 100)
    s5 = ListeningSession("s5", lily, t1, RECENT, 300)
    s6 = ListeningSession("s6", tom, t3, RECENT, 210)
    s7=ListeningSession("s7", emma, t1, RECENT, 180)
    for s in (s1, s2, s3, s4, s5, s6, s7):
        platform.record_session(s)



    # ------------------------------------------------------------------
    # playlists
    # ------------------------------------------------------------------
    p1 = Playlist("p1", "Alice Favorites", alice)
    p1.add_track(t1)
    p1.add_track(t2)

    # Collaborative playlist
    p2 = CollaborativePlaylist("p2", "Shared Mix", bob)

    # Add contributors
    p2.add_contributor(alice)
    p2.add_contributor(father)

    # Add tracks
    p2.add_track(t2)
    p2.add_track(t3)

    platform.add_playlist(p1)
    platform.add_playlist(p2)

    # ------------------------------------------------------------------
    # single release
    # ------------------------------------------------------------------

    sr1 = SingleRelease("sng1", "bad guy", 210, "pop", billie,date(2016,2,20))
    sr2 = SingleRelease("sng2", "Ocean Eyes Acoustic", 190, "pop", billie,date(2018,5,18))


    platform.add_track(sr1)
    platform.add_track(sr2)


    billie.add_track(sr1)
    billie.add_track(sr2)



    return platform




@pytest.fixture
def fixed_now() -> datetime:
    """Expose the shared FIXED_NOW constant to tests."""
    return FIXED_NOW


@pytest.fixture
def recent_ts() -> datetime:
    return RECENT


@pytest.fixture
def old_ts() -> datetime:
    return OLD
