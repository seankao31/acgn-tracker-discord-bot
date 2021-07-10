import pytest
import random
from src.acgn_data import AcgnData
from src.acgn_tracker_model import AcgnTrackerModel
from src.exceptions import AcgnNotFound
from src.progress_data import ProgressData


@pytest.fixture
def data():
    user_data = [
        {
            'discord_id': 222,
            'discord_username': 'abc#3'
        },
        {
            'discord_id': 333,
            'discord_username': 'def#5'
        },
        {
            'discord_id': 444,
            'discord_username': 'ghi#8'
        }
    ]
    acgn_data = [
        {
            'title': 'aaa',
            'final_episode': '13'
        },
        {
            'title': 'bbbb',
            'final_episode': '50'
        },
        {
            'title': 'ccccc',
            'final_episode': '6'
        },
    ]
    progress_data = [
        {
            'user_id': 0,
            'acgn_id': 0,
            'episode': '4'
        },
        {
            'user_id': 0,
            'acgn_id': 1,
            'episode': '26'
        },
        {
            'user_id': 1,
            'acgn_id': 0,
            'episode': '7'
        },
        {
            'user_id': 2,
            'acgn_id': 2,
            'episode': '2'
        },
    ]
    return {'user': user_data, 'acgn': acgn_data, 'progress': progress_data}


@pytest.fixture
def random_user(data):
    return random.choice(data['user'])


@pytest.fixture
def random_acgn(data):
    return random.choice(data['acgn'])


@pytest.fixture
def random_progress(data):
    return random.choice(data['progress'])
