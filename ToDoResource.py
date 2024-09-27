import falcon
import json

class TodoResource:
	def __init__(self):
		self.todos = []
	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		resp.body = json.dumps({'todos': self.todos})
	def on_post(self, req, resp):
		data = req.media
		todo = data.get('todo')
		if todo is not None:
			self.todos.append(todo)
			resp.status = falcon.HTTP_201
			resp.body = json.dumps({'message': 'Todo added successfully'})
		else:
			resp.status = falcon.HTTP_BAD_REQUEST
			resp.body = json.dumps({'error': 'Invalid request'})

app = falcon.App()
app.add_route('/todos', TodoResource())

if __name__ == '__main__':
	from wsgiref import simple_server

	httpd = simple_server.make_server('localhost', 8000, app)
	httpd.serve_forever()
