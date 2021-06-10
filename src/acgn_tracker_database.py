from .acgn_data import AcgnData
from .progress_data import ProgressData


class AcgnTrackerDatabase:
    def __init__(self, acgns=[], progresses=[]):
        self.acgns = acgns
        self.progresses = progresses

    def acgn_update(self, title: str, final_episode):
        acgn_matched = self.acgn_find(title)
        if acgn_matched:
            the_acgn = acgn_matched[0]
            the_acgn.final_episode = final_episode
        else:
            new_acgn = AcgnData(title, final_episode)
            self.acgns.append(new_acgn)

    def acgn_find(self, title: str):
        if not self.acgns:
            return []
        # if db setup correctly then it should only have one element
        return [acgn for acgn in self.acgns if acgn.title == title]

    def progress_update(self, user, title: str, episode):
        acgn_matched = self.acgn_find(title)
        if acgn_matched == []:
            # no such title
            return

        # TODO: might check whether episode exceeds final_episode
        # watch out non-integer episodes, can't expect int or even number?

        progress_matched = self.progress_find(user, title)
        if progress_matched == []:
            new_progress = ProgressData(user, title, episode)
            self.progresses.append(new_progress)
        else:
            the_progress = progress_matched[0]
            the_progress.episode = episode

    def progress_find(self, user, title: str):
        if not self.progresses:
            return []
        # if db setup correctly then it should only have one element
        return [progress for progress in self.progresses
                if progress.user is user and progress.title is title]
