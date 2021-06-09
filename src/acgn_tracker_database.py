from .acgn_data import AcgnData
from .progress_data import ProgressData


class AcgnTrackerDatabase:
    def __init__(self, acgns=[], progresses=[]):
        self.acgns = acgns
        self.progresses = progresses

    def acgn_find(self, title: str):
        if not self.acgns:
            return []
        return [acgn for acgn in self.acgns if acgn.title == title]
