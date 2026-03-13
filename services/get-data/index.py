from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Path:", self.path)  # In thông tin từ trình duyệt
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Data received!")

server = HTTPServer(('localhost', 9080), RequestHandler)
print("Server running on http://localhost:9080")
server.serve_forever()
