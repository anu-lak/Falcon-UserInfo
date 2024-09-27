import falcon
from waitress import serve
from user_info.user_resource import UserResource



app = falcon.App()
app.add_route('/user', UserResource())
app.add_route('/user/{email}', UserResource())

if __name__ == '__main__':
    print("Server is starting on http://127.0.0.1:8080")
    serve(app, host='localhost', port=8080)
