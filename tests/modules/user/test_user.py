import pytest
import json
from pymongo import MongoClient
from src.kashflow.app import *


@pytest.fixture(scope='module')
def app(request):
    """Fixture to initialize flask app"""
    app = create_app()

    with app.app_context():
        # init_db()
        yield app


@pytest.fixture
def client(request, app):
    """Fixture to initialize flask-restplus test client"""
    c = app.test_client()

    def teardown():
        pass # os.unlink(app.config['DATABASE'])

    request.addfinalizer(teardown)
    return c


@pytest.fixture(scope='module')
def data(request, app):
    """Fixture to initialize MongoDB test database"""
    cl = MongoClient('127.0.0.1:27017')
    db = cl[app.config['DATABASE']]
    _data = {}
    _data['user'] = {
        "first_name": "Amy",
        "last_name": "Jones",
        "email": "amy.jones.1877256@gmail.com",
        "gender": "female",
        "dob": "1994-07-31T00:00:00.000Z"
    }
    id = db.users.insert_one(_data['user']).inserted_id
    _data['user']['id'] = str(id)
    yield _data
    result = db.users.delete_many({})


class TestUsersApi():
    """Tests for users API at /api/users
    These are infrastructure tests and require a running MongoDB instance
    """

    def test_get(self, client, data):
        res = client.get('/api/users')
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_get_by_id(self, client, data):
        uri = '/api/users/' + data['user']['id']
        res = client.get(uri)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_get_by_bad_id(self, client, data):
        uri = '/api/users/' + '356fb7a2c0571b6d6cc2368e'
        res = client.get(uri)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 404

    def test_get_by_email(self, client, data):
        res = client.get('/api/users?email=timjenks@gmail.com')
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_post(self, client, data):
        user = {
            "first_name": "Tom",
            "last_name": "Jones",
            "email": "tim.jones.1877256@gmail.com",
            "gender": "male",
            "dob": "1984-07-31T00:38:21.702Z"
        }
        user_json = json.dumps(user)
        headers = {'Content-Type': 'application/json'}
        res = client.post('/api/users', data=user_json, headers=headers, follow_redirects=True)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_post_duplicate(self, client, data):
        user = {
            "first_name": "Amy",
            "last_name": "Jones",
            "email": "amy.jones.1877256@gmail.com",
            "gender": "female",
            "dob": "1994-07-31T00:00:00.000Z"
        }
        user_json = json.dumps(user)
        headers = {'Content-Type': 'application/json'}
        res = client.post('/api/users', data=user_json, headers=headers, follow_redirects=True)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 409

    def test_update_by_id(self, client, data):
        user = {
            "id": data['user']['id'],
            "first_name": "Amy",
            "last_name": "Archer",
            "email": "amy.jones.1877256@gmail.com",
            "gender": "female",
            "dob": "1994-07-31T00:00:00.000Z"
        }
        user_json = json.dumps(user)
        headers = {'Content-Type': 'application/json'}
        res = client.put('/api/users', data=user_json, headers=headers, follow_redirects=True)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_update_by_bad_id(self, client, data):
        user = {
            "id": '356fb7a2c0571b6d6cc2368e',
            "first_name": "Amy",
            "last_name": "Archer",
            "email": "amy.jones.1877256@gmail.com",
            "gender": "female",
            "dob": "1994-07-31T00:00:00.000Z"
        }
        user_json = json.dumps(user)
        headers = {'Content-Type': 'application/json'}
        res = client.put('/api/users', data=user_json, headers=headers, follow_redirects=True)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 404

    def test_delete_by_id(self, client, data):
        uri = '/api/users/' + data['user']['id']
        res = client.delete(uri)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_delete_by_bad_id(self, client, data):
        uri = '/api/users/' + '356fb7a2c0571b6d6cc2368e'
        res = client.delete(uri)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 404