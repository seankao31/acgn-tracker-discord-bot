import pytest
import random
from src.acgn_data import AcgnData
from src.acgn_tracker_database import AcgnTrackerDatabase
from src.exceptions import AcgnNotFound
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
def random_acgn(data):
    acgn_data, _ = data
    return random.choice(acgn_data)


@pytest.fixture
def random_progress(data):
    _, progress_data = data
    return random.choice(progress_data)


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


def test_acgn_find_not_in_db(initial_db):
    fake_acgn_title = 'xxx'
    empty_db = AcgnTrackerDatabase()
    assert empty_db.acgn_find(fake_acgn_title) == []
    assert initial_db.acgn_find(fake_acgn_title) == []


@pytest.mark.repeat(5)
def test_acgn_find_in_db(random_acgn, initial_db):
    acgn_matched = initial_db.acgn_find(random_acgn['title'])
    assert len(acgn_matched) == 1
    acgn = acgn_matched[0]
    assert acgn.title == random_acgn['title']
    assert acgn.final_episode == random_acgn['final_episode']


@pytest.mark.repeat(5)
def test_acgn_update_add_new_in_empty(random_acgn):
    title = random_acgn['title']
    final_episode = random_acgn['final_episode']
    db = AcgnTrackerDatabase()
    db.acgn_update(title, final_episode)
    assert len(db.acgns) == 1
    the_acgn = db.acgns[0]
    assert the_acgn.title == title
    assert the_acgn.final_episode == final_episode


def test_acgn_update_add_new_in_nonempty(initial_db):
    db = initial_db
    initial_len = len(db.acgns)
    new_title = 'xxx'
    new_final_episode = 100

    db.acgn_update(new_title, new_final_episode)
    assert len(db.acgns) == initial_len + 1
    the_acgn = db.acgns[-1]
    assert the_acgn.title == new_title
    assert the_acgn.final_episode == new_final_episode


@pytest.mark.repeat(5)
def test_acgn_update_existed(random_acgn, initial_db):
    db = initial_db
    initial_len = len(db.acgns)
    title = random_acgn['title']
    new_final_episode = random_acgn['final_episode'] + 10

    db.acgn_update(title, new_final_episode)
    assert len(db.acgns) == initial_len
    acgn_matched = db.acgn_find(title)
    the_acgn = acgn_matched[0]
    assert the_acgn.title == title
    assert the_acgn.final_episode == new_final_episode


@pytest.mark.repeat(5)
def test_progress_find_not_in_db(random_progress, initial_db):
    user_true = random_progress['user']
    title_true = random_progress['title']
    user_false = 1000
    title_false = 'xxx'
    empty_db = AcgnTrackerDatabase()
    assert empty_db.progress_find(user_false, title_false) == []

    assert initial_db.progress_find(user_false, title_false) == []
    assert initial_db.progress_find(user_true, title_false) == []
    assert initial_db.progress_find(user_false, title_true) == []


@pytest.mark.repeat(5)
def test_progress_find_in_db(random_progress, initial_db):
    user = random_progress['user']
    title = random_progress['title']
    episode = random_progress['episode']
    progress_matched = initial_db.progress_find(user, title)
    assert len(progress_matched) == 1
    progress = progress_matched[0]
    assert progress.user == user
    assert progress.title == title
    assert progress.episode == episode


@pytest.mark.repeat(5)
def test_progress_update_add_new_in_empty_fail(random_progress):
    user = random_progress['user']
    title = random_progress['title']
    episode = random_progress['episode']
    db = AcgnTrackerDatabase()

    with pytest.raises(AcgnNotFound):
        db.progress_update(user, title, episode)
        assert db.progresses == []


@pytest.mark.repeat(5)
def test_progress_update_add_new_in_nonempty(random_acgn, initial_db):
    db = initial_db
    initial_len = len(db.progresses)
    new_user = 777
    title = random_acgn['title']
    episode = 1

    # add new progress whose title already exist in acgn database
    db.progress_update(new_user, title, episode)
    assert len(db.progresses) == initial_len + 1
    the_progress = db.progresses[-1]
    assert the_progress.user == new_user
    assert the_progress.title == title
    assert the_progress.episode == episode

    # add new progress with a new title. should fail
    with pytest.raises(AcgnNotFound):
        title_fake = 'xxx'
        db.progress_update(new_user, title_fake, episode)
        assert len(db.progresses) == initial_len + 1
        for progress in db.progresses:
            assert progress.title != title_fake


@pytest.mark.repeat(5)
def test_progress_update_existed(random_progress, initial_db):
    db = initial_db
    initial_len = len(db.progresses)
    user = random_progress['user']
    title = random_progress['title']
    new_episode = random_progress['episode'] + 1

    db.progress_update(user, title, new_episode)
    assert len(db.progresses) == initial_len
    progress_matched = db.progress_find(user, title)
    the_progress = progress_matched[0]
    assert the_progress.user == user
    assert the_progress.title == title
    assert the_progress.episode == new_episode
