import falcon
import json
from user_info.main.database import db
from user_info.main.model import User


class UserResource:
    def __init__(self):
        self.collection = db['users']

    def on_get(self,req,resp,email):
        try:

            if '@' not in email:
                raise ValueError("Invalid email address")

            # Retrieve user info based on email
            user_info = self.collection.find_one({'email': email}, {'_id': 0})
            if user_info:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(user_info)
            else:
                resp.status = falcon.HTTP_404  # Not Found
                resp.body = json.dumps({'error': 'User not found'})

        except ValueError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = json.dumps({'error': str(e)})

    def on_post(self, req, resp):
        try:
            data  = req.media
            required_keys = ['name', 'age', 'email']

            if not all(key in data for key in required_keys):
                raise ValueError("All fields (name, age, email) are required")
            if not isinstance(data['age'], int):
                raise ValueError("Age must be an integer")
            if data['age']<0:
                raise ValueError("Age cannot be below 0")
            if '@' not in data['email']:
                raise ValueError("Invalid email address")
            if self.collection.find_one({'email': data.get('email')}):
                raise ValueError("Email already exists")


            user = User.from_dict(data)
            self.collection.insert_one(user.to_dict())
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'message': 'User info added successfully'})

            # Writing to json file
            try:
                with open("users.json", "r") as f:
                    users = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                users = []

            users.append({'name': data.get('name'), 'email': data.get('email'), 'age': data.get('age')})
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)


        except KeyError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = json.dumps({'error': str(e)})
        except ValueError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = json.dumps({'error': str(e)})
        except Exception as e:
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
            resp.body = json.dumps({'error': 'Internal Server Error'})


