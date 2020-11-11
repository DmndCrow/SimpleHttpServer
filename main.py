import os
import http.server
import socketserver
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv('HTTP_PORT', '3000'))
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
