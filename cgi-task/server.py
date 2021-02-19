from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = ('localhost', 5002)

httpd = HTTPServer(HOST, CGIHTTPRequestHandler)
httpd.serve_forever()
