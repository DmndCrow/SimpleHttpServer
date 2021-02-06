import os
import json
import secrets
import string
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from urllib.parse import parse_qs
from jinja2 import Template

load_dotenv()

PORT = int(os.getenv('HTTP_PORT', '3000'))

long_urls = {}
short_urls = {}

redirect = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        window.onload = function () {
            window.location.href = '%s'
        }
    </script>
</head>
<body>

</body>
</html>
"""


class HandleRoute:
    def __init__(self):
        self.routes = {
            '/': self.root(),
            '/url': self.urlShortener(),
            '/not-found': self.notFound()
        }

    def root(self):
        f = open('./templates/index.html', 'r', encoding='utf-8')
        return f.read()

    def urlShortener(self):
        f = open('./templates/shortener.html', 'r', encoding='utf-8')
        return f.read()

    def redirect(self, url):
        return redirect % url

    def notFound(self):
        f = open('./templates/not-found.html', 'r', encoding='utf-8')
        return f.read()


class Handler(BaseHTTPRequestHandler):
    def generateShortUrl(self):
        length = 6
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        return password

    def do_POST(self):
        # How long was the message?
        length = int(self.headers.get('Content-length', 0))

        # Read the correct amount of data from the request.
        data = self.rfile.read(length).decode()
        form = parse_qs(data)

        long = form['long_url'][0]

        if long in long_urls:
            short = long_urls[long]
        else:
            short = self.generateShortUrl()
            while short in short_urls:
                short = self.generateShortUrl()
            short_urls[short] = long
            long_urls[long] = short

        # Send the "message" field back as the response.
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        response = {
            'Short url is': f'http://localhost:{PORT}/' + short
        }

        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        routes = HandleRoute().routes

        if self.path in routes:
            self.wfile.write(routes[self.path].encode())
        elif self.path[1:] in short_urls:
            res = HandleRoute().redirect(short_urls[self.path[1:]])
            self.wfile.write(res.encode())
        else:
            self.wfile.write(routes['/not-found'].encode())


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', PORT), Handler)

    try:
        print('Server is running at port', PORT)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
