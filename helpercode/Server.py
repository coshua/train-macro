from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from TrainTicketMacro import process
port = 1010

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request = urlparse(self.path)
        params = parse_qs(request.query)
        print(params, len(params))
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        if len(params) > 0:
            process()

# httpd = HTTPServer(('0.0.0.0', port), RequestHandler)
# httpd.serve_forever()