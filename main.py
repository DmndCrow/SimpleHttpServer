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
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        routes = HandleRoute().routes

        if self.path in routes:
            data = {
                'response': routes[self.path]
            }
        else:
            data = {
                'response': 'oops'
            }

        self.wfile.write(json.dumps(data).encode())


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', PORT), Handler)

    try:
        print('Server is running at port', PORT)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
