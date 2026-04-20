"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from datetime import date
from abc import ABC
from typing import List,Set,TYPE_CHECKING
if TYPE_CHECKING:
    from .sessions import ListeningSession



"""https://www.geeksforgeeks.org/python/abstract-classes-in-python/"""
class User(ABC):
    """Base class for platform users."""
    def __init__(self,user_id: str,name: str,age: int):
        """
                Initialize a user.

                Args:
                    user_id: identifier(unique).
                    name: the name of the user.
                    age: the age of the user.
                """
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions : List["ListeningSession"] = []


    def add_session(self,session:"ListeningSession")->None:
            """Add a listening session."""
            self.sessions.append(session)


    def total_listening_seconds(self)->int:
            """Calculate the total listening time in seconds."""
            return sum(session.duration_listened_seconds for session in self.sessions)


    def total_listening_minutes(self)->float:
            """ Calculate the total listening time in minutes."""
            return self.total_listening_seconds() / 60.0


    def unique_tracks_listened(self)->Set[str]:
            """Get unique track IDs listened by the user."""
            return {session.track.track_id for session in self.sessions}

class FreeUser(User):
    """User with very limited features"""
    MAX_SKIPS_PER_HOUR=6

class PremiumUser (User):
    """User with a  subscription that needs to be paid for."""
    def __init__(self, user_id: str, name: str, age: int,subscription_start:date):
        """Initializing a premium user."""
        super().__init__(user_id,name,age)
        self.subscription_start= subscription_start

class FamilyAccountUser(User):
    def __init__(self, user_id: str, name: str, age: int):
        """Initializing a family account user."""
        super().__init__(user_id, name, age)
        self.sub_users : List ["FamilyMember"] = []


    def add_sub_user(self,sub_user:"FamilyMember")->None:
        """ add a sub-user to the family account."""
        if sub_user not in self.sub_users:
            self.sub_users.append(sub_user)





    def all_members(self)-> List["User"]:
        """return all the members in  family account."""
        return [self] + self.sub_users

class FamilyMember(User):
    def __init__(self, user_id: str, name: str, age: int,parent:FamilyAccountUser):
        """Initialize a family member."""
        super().__init__(user_id, name, age)
        self.parent = parent











