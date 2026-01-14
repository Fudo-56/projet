from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests

TRAITEMENT_URL = "http://traitement:6000"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = json.loads(self.rfile.read(length))

        # Relais vers traitement
        r = requests.post(TRAITEMENT_URL, json=data, timeout=5)

        self.send_response(r.status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(r.content)


server = HTTPServer(("0.0.0.0", 5000), Handler)
print("🌐 Server listening on port 5000")
server.serve_forever()

