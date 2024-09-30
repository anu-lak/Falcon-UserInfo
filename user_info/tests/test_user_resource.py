import json
import falcon
import pytest
import mongomock
from falcon import testing
from unittest.mock import patch
from user_info.main.user_resource import UserResource


@pytest.fixture
def client():

    app = falcon.App()
    user_resource = UserResource()
    app.add_route('/users', user_resource)
    app.add_route('/users/{email}', user_resource)


    return testing.TestClient(app)


# # Test for the POST request
@patch('user_info.database.db')  # Mocking the MongoDB collection_in
def test_on_post_success(mock_db,client):

    # Mock MongoDB insert_one operation
    mock_db['users'].insert_one.return_value = None

    user_data = {
        'name': 'Anu2 M',
        'email': 'anu@example.com',
        'age': 30
    }

    response = client.simulate_post('/users', json=user_data)
    
    assert response.status == '201 Created'
    assert json.loads(response.content) == {'message': 'User info added successfully'}

########################
@patch('user_info.database.MongoClient', new=mongomock.MongoClient)
def test_on_post_success(client):
   
    user_data = {
        'name': 'Anuuuuu M',
        'email': 'anu@example.com',
        'age': 30
    }

    response = client.simulate_post('/users', json=user_data)

    assert response.status == '201 Created'
    assert json.loads(response.content) == {'message': 'User info added successfully'}



@patch('user_info.database.db')
def test_on_post_missing_fields(mock_db, client):

    
    user_data = {
        'name': 'Anu M',
        'email': 'anu@example.com',
    }

    response = client.simulate_post('/users', json=user_data)

    assert response.status == '400 Bad Request'
    assert json.loads(response.content) == {'error': 'All fields (name, age, email) are required'}


@patch('user_info.database.db')
def test_on_post_invalid_email(mock_db, client):

    user_data = {
        'name': 'Anu M',
        'email': 'anuexample.com',
        'age': 30
    }

    response = client.simulate_post('/users', json=user_data)

    assert response.status == '400 Bad Request'
    assert json.loads(response.content) == {'error': 'Invalid email address'}

@patch('user_info.database.db')
def test_on_post_invalid_age(mock_db, client):

    user_data = {
        'name': 'Anu M',
        'email': 'anue@xample.com',
        'age': "gh"
    }

    response = client.simulate_post('/users', json=user_data)

    assert response.status == '400 Bad Request'
    assert json.loads(response.content) == {'error': 'Age must be an integer'}


# Test for the GET request
@patch('user_info.database.db')
def test_on_get_success(mock_db, client):
    # Mock MongoDB find_one operation
    mock_db['users'].find_one.return_value = {
        'name': 'Anu M',
        'email': 'anu@example.com',
        'age': 30
    }

    response = client.simulate_get('/users/anu@example.com')

    assert response.status == '200 OK'
    assert json.loads(response.content) == {
        'name': 'Anu M',
        'email': 'anu@example.com',
        'age': 30
    }


@patch('user_info.database.db')
def test_on_get_user_not_found(mock_db, client):
    # Mock MongoDB find_one operation to return None (user not found)
    mock_db['users'].find_one.return_value = None

    response = client.simulate_get('/users/nonexistent@example.com')

    assert response.status == '404 Not Found'
    assert json.loads(response.content) == {'error': 'User not found'}

