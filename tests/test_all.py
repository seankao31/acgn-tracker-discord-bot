import pytest
from src.acgn_data import AcgnData
from src.acgn_tracker_database import AcgnTrackerDatabase
from src.progress_data import ProgressData


@pytest.fixture
def data():
    acgn_data = [
        {
            'title': 'aaa',
            'final_episode': 13
        },
        {
            'title': 'bbbb',
            'final_episode': 50
        },
        {
            'title': 'ccccc',
            'final_episode': 6
        },
    ]
    progress_data = [
        {
            'user': 1,
            'title': 'aaa',
            'episode': 4
        },
        {
            'user': 1,
            'title': 'bbbb',
            'episode': 26
        },
        {
            'user': 2,
            'title': 'aaa',
            'episode': 7
        },
        {
            'user': 3,
            'title': 'ccccc',
            'episode': 2
        },
    ]
    return acgn_data, progress_data


@pytest.fixture
def initial_db(data):
    acgn_data, progress_data = data
    acgns = []
    progresses = []

    for acgn in acgn_data:
        acgns.append(AcgnData(acgn['title'], acgn['final_episode']))
    for progress in progress_data:
        progresses.append(ProgressData(
            progress['user'], progress['title'], progress['episode']))

    return AcgnTrackerDatabase(acgns, progresses)
