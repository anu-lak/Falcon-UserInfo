import json
import falcon
import pytest
import mongomock
from falcon import testing
from unittest.mock import patch
from user_info.main.user_resource import UserResource
from user_info.tests.mock_collection import MockCollection


@pytest.fixture
def mock_collection():
    return MockCollection()


@pytest.fixture
def client(mock_collection):

    app = falcon.App()
    user_resource = UserResource(mock_collection)
    app.add_route('/users', user_resource)
    app.add_route('/users/{email}', user_resource)
    return testing.TestClient(app)


# POST tests
@patch('user_info.main.database.db')
def test_on_post_success(mock_db, client):
    user_data = {
        'name': 'Anu M',
        'age': 30,
        'email': 'anu@example.com'
    }
    response = client.simulate_post('/users', json=user_data)
    assert response.status == '201 Created'
    assert json.loads(response.content) == {'message': 'User info added successfully'}


@patch('user_info.main.database.db')
def test_on_post_missing_fields(mock_db, client):

    
    user_data = {
        'name': 'Anu M',
        'email': 'anu@example.com',
    }

    response = client.simulate_post('/users', json=user_data)

    assert response.status == '400 Bad Request'
    assert json.loads(response.content) == {'error': 'All fields (name, age, email) are required'}


@patch('user_info.main.database.db')
def test_on_post_invalid_email(mock_db, client):

    user_data = {
        'name': 'Anu M',
        'email': 'anuexample.com',
        'age': 30
    }

    response = client.simulate_post('/users', json=user_data)

    assert response.status == '400 Bad Request'
    assert json.loads(response.content) == {'error': 'Invalid email address'}

@patch('user_info.main.database.db')
def test_on_post_invalid_age(mock_db, client):

    user_data = {
        'name': 'Anu M',
        'email': 'anue@xample.com',
        'age': "gh"
    }

    response = client.simulate_post('/users', json=user_data)

    assert response.status == '400 Bad Request'
    assert json.loads(response.content) == {'error': 'Age must be an integer'}

@patch('user_info.main.database.db')
def test_on_post_negative_age_(mock_db, client):

    user_data = {
        'name': 'Anu M',
        'email': 'anue@xample.com',
        'age': -34
    }

    response = client.simulate_post('/users', json=user_data)

    assert response.status == '400 Bad Request'
    assert json.loads(response.content) == {'error': 'Age cannot be below 0'}

@patch('user_info.main.database.db')
def test_on_post_existing_email(mock_db, client):
    existing_user = {
        'name': 'Existing User',
        'email': 'anu@example.com',
        'age': 25
    }

    # Inserting the pre-existing user into the mock database
    client.app._router._roots[0].resource.collection.insert_one(existing_user)

    # Trying to insert a new user with the same email
    new_user_data = {
        'name': 'Anu M',
        'email': 'anu@example.com',
        'age': 30
    }

    response = client.simulate_post('/users', json=new_user_data)
    assert response.status == '400 Bad Request'
    assert json.loads(response.content) == {'error': 'Email already exists'}



# GET tests
@patch('user_info.main.database.db')
def test_on_get_success(mock_db, client):
    # Create a mock MongoDB connection
    with mongomock.patch(servers=['localhost:27017']):
        # Mock MongoDB find_one operation
        mock_db['users'].find_one.return_value = {
            'name': 'Anu M',
            'email': 'anu@example.com',
            'age': 30
        }

        # Insert the user data into the mock collection
        client.app._router._roots[0].resource.collection.insert_one({
            'name': 'Anu M',
            'email': 'anu@example.com',
            'age': 30
        })

        response = client.simulate_get('/users/anu@example.com')

        assert response.status == '200 OK'
        assert json.loads(response.content) == {
            'name': 'Anu M',
            'email': 'anu@example.com',
            'age': 30
        }


@patch('user_info.main.database.db')
def test_on_get_user_not_found(mock_db, client):
    # Mock MongoDB find_one operation to return None (user not found)
    mock_db['users'].find_one.return_value = None

    response = client.simulate_get('/users/nonexistent@example.com')

    assert response.status == '404 Not Found'
    assert json.loads(response.content) == {'error': 'User not found'}


@patch('user_info.main.database.db')
def test_on_get_invalid_email(mock_db, client):
    response = client.simulate_get('/users/invalid-email')

    assert response.status == '400 Bad Request'
    assert json.loads(response.content) == {'error': 'Invalid email address'}