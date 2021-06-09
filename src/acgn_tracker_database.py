from .acgn_data import AcgnData
from .progress_data import ProgressData


class AcgnTrackerDatabase:
    def __init__(self, acgns=[], progresses=[]):
        self.acgns = acgns
        self.progresses = progresses
