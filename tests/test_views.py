import pytest
from json import loads

from vikingapp import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    # TODO: Add the database init
    # with app.app_context():
    #     app.init_db()
    
    yield client

def test_index(client):
    rv = client.get('/')
    assert b'Hello World!' in rv.data

def test_greet_person(client):
    rv = client.get('/name/Tom')
    assert b'Hello Tom!' in rv.data

def test_post_greet_person_returns_405(client):
    rv = client.post('/name/Tom')
    assert '405' in rv.status

def test_sum_stuff_returns_sum(client):
    rv = client.get('/sum?x=2&y=3')
    data = loads(rv.data)
    assert data['sum'] == 5

def test_sum_stuff_post_returns_405(client):
    rv = client.post('/sum?x=3&y=4')
    assert '405' in rv.status
