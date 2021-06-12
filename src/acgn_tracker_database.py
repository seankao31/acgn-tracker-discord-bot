from .acgn_data import AcgnData
from .progress_data import ProgressData


class AcgnTrackerDatabase:
    """Database of acgns and progresses.

    Attributes:
        acgns: A list of AcgnData of tracked acgns.
        progresses: A list of ProgressData of tracked progresses.
    """
    def __init__(self, acgns=None, progresses=None):
        """Inits the database.

        Args:
            acgns: Optional; A list of AcgnData.
            progresses: Optional; A list of ProgressData.
        """
        if acgns is None:
            acgns = []
        if progresses is None:
            progresses = []
        self.acgns = acgns
        self.progresses = progresses

    def acgn_update(self, title: str, final_episode):
        """Adds or updates an acgn in the database.

        Updates final_episode of an acgn entry matching the given title.
        If there's no matching entry, create a new one and add to database.

        Args:
            title: A string.
            final_episode: Number of final episode. Usually it's an integer.
        """
        acgn_matched = self.acgn_find(title)
        if acgn_matched:
            the_acgn = acgn_matched[0]
            the_acgn.final_episode = final_episode
        else:
            new_acgn = AcgnData(title, final_episode)
            self.acgns.append(new_acgn)

    def acgn_find(self, title: str):
        """Returns list of AcgnData that match the given title.

        Args:
            title: A string.
        """
        if not self.acgns:
            return []
        # if db setup correctly then it should only have one element
        return [acgn for acgn in self.acgns if acgn.title == title]

    def progress_update(self, user, title: str, episode):
        """Adds or updates a progress in the database.

        Updates episode of a progress entry matching the given user and title.
        If there's no matching entry, create a new one and add to database.

        Args:
            user: An identifier indicating the user.
            title: A string.
            episode: Number of the episode. Usually it's an integer.
        """
        acgn_matched = self.acgn_find(title)
        if not acgn_matched:
            # no such title
            # TODO: should raise exception
            return

        progress_matched = self.progress_find(user, title)
        if not progress_matched:
            new_progress = ProgressData(user, title, episode)
            self.progresses.append(new_progress)
        else:
            the_progress = progress_matched[0]
            the_progress.episode = episode

    def progress_find(self, user, title: str):
        """Returns list of ProgressData that match the given user and title.

        Args:
            user: An identifier indicating the user.
            title: A string.
        """
        if not self.progresses:
            return []
        # if db setup correctly then it should only have one element
        return [progress for progress in self.progresses
                if progress.user == user and progress.title == title]
