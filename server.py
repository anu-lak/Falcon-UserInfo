import falcon
from waitress import serve

# Define a resource that handles HTTP GET requests
class HelloWorldResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # Set the HTTP status code to 200 OK
        resp.text = "Hello hiiii, Falcon World!"  # Set the response body text

# Create a Falcon app instance
app = falcon.App()

# Add a route that maps the URL path "/hello" to the HelloWorldResource
app.add_route('/hello', HelloWorldResource())

# Set up the Waitress server to serve the Falcon app
if __name__ == '__main__':
    print("Server is starting on http://127.0.0.1:8000")
    serve(app, host='localhost', port=8080)

# from wsgiref import simple_server
 # httpd = simple_server.make_server('localhost', 8000, app)
    # print("Serving on http://localhost:8000/user")
    # httpd.serve_forever()
