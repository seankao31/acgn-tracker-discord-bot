from pymongo import MongoClient

from .acgn_data import AcgnData
from .exceptions import AcgnNotFound
from .progress_data import ProgressData


class AcgnTrackerDatabase:
    """Database of acgns and progresses.

    Attributes:
        acgns: A list of AcgnData of tracked acgns.
        progresses: A list of ProgressData of tracked progresses.
    """
    def __init__(self, db=None, acgns=None, progresses=None):
        """Inits the database.

        Args:
            mongoclient: Optional; A MongoClient.
            acgns: Optional; A list of AcgnData.
            progresses: Optional; A list of ProgressData.
        """
        if db is None:
            db = MongoClient().acgn_tracker
        self.db = db
        self.db.acgns.drop()
        if acgns is not None:
            self.db.acgns.insert_many([acgn.__dict__ for acgn in acgns])
        self.db.progresses.drop()
        if progresses is not None:
            self.db.progresses.insert_many([progress.__dict__
                                            for progress in progresses])

    def acgn_count(self):
        """Returns number of acgns in the database."""
        return self.db.acgns.count_documents({})

    def acgn_list(self):
        """Returns all acgns in the database."""
        return [AcgnData(title=acgn['title'],
                         final_episode=acgn['final_episode'])
                for acgn in self.db.acgns.find({})]

    def acgn_update(self, title: str, final_episode):
        """Adds or updates an acgn in the database.

        Updates final_episode of an acgn entry matching the given title.
        If there's no matching entry, create a new one and add to database.

        Args:
            title: A string.
            final_episode: Number of final episode. Usually it's an integer.
        """
        self.db.acgns.update_one({'title': title},
                                 {'$set': {'final_episode': final_episode}},
                                 upsert=True)

    def acgn_find(self, title: str):
        """Returns list of AcgnData that match the given title.

        Args:
            title: A string.
        """
        # if db setup correctly then it should only have one element
        acgns = self.db.acgns.find({'title': title})
        acgns = [AcgnData(title=acgn['title'],
                          final_episode=acgn['final_episode'])
                 for acgn in acgns]
        return acgns

    def progress_count(self):
        """Returns number of progresses in the database."""
        return self.db.progresses.count_documents({})

    def progress_list(self):
        """Returns all progresses in the database."""
        return [ProgressData(user=progress['user'],
                             title=progress['title'],
                             episode=progress['episode'])
                for progress in self.db.progresses.find({})]

    def progress_update(self, user, title: str, episode):
        """Adds or updates a progress in the database.

        Updates episode of a progress entry matching the given user and title.
        If there's no matching entry, create a new one and add to database.

        Args:
            user: An identifier indicating the user.
            title: A string.
            episode: Number of the episode. Usually it's an integer.

        Raises:
            AcgnNotFound: Title doesn't exist in the database.
        """
        acgn_matched = self.acgn_find(title)
        if not acgn_matched:
            raise AcgnNotFound

        self.db.progresses.update_one({'user': user, 'title': title},
                                      {'$set': {'episode': episode}},
                                      upsert=True)

    def progress_find(self, user, title: str):
        """Returns list of ProgressData that match the given user and title.

        Args:
            user: An identifier indicating the user.
            title: A string.
        """
        # if db setup correctly then it should only have one element
        progresses = self.db.progresses.find({'user': user, 'title': title})
        progresses = [ProgressData(user=progress['user'],
                                   title=progress['title'],
                                   episode=progress['episode'])
                      for progress in progresses]
        return progresses
