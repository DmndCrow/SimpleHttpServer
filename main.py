import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv('HTTP_PORT', '3000'))


class HandleRoute:
    def __init__(self):
        self.routes = {
            '/': self.root(),
            '/hello': self.hello()
        }

    def root(self):
        return 'Root Directory'

    def hello(self):
        return 'Hello World'


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # How long was the message?
        length = int(self.headers.get('Content-length', 0))

        # Read the correct amount of data from the request.
        data = json.loads(self.rfile.read(length).decode())

        # Send the "message" field back as the response.
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        response = {
            'response': data
        }

        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        routes = HandleRoute().routes

        if self.path in routes:
            response = {
                'response': routes[self.path]
            }
        else:
            response = {
                'response': 'oops'
            }

        self.wfile.write(json.dumps(response).encode())


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', PORT), Handler)

    try:
        print('Server is running at port', PORT)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
