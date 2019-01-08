from sys import version as python_version
import cgi
import threading

if python_version.startswith('3'):
    from urllib.parse import parse_qs
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from urlparse import parse_qs
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_GET(self):
        self._set_headers()
        print(self.path)
        print(parse_qs(self.path[2:]))
        #self.wfile.write("<html><body><h1>Get Request Received!</h1></body></html>")
    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        #print(form)
        #print(len(form))
        for field in form.list:
            print(field.name+" : "+field.value)
        #print(form.getvalue("result"))
        #print(form.getvalue("field"))
        #self.wfile.write("<html><body><h1>POST Request Received!</h1></body></html>")

class http_server:
    def __init__(self, server_class=HTTPServer, handler_class=GP, port=8088):
        server_address = ('', port)
        self.httpd = server_class(server_address, handler_class)
        print('Server running at localhost:8088...')
        self.pending_requests = 0
        self.completed_requests = 0
    def run(self):
        while self.pending_requests != 0:
            self.httpd.handle_request()
            self.pending_requests -= 1
            self.completed_requests += 1
    def run_forever(self):
        self.httpd.serve_forever()
    def threaded_server(self):
        t = threading.Thread(target=self.httpd.serve_forever)
        t.deamon = False
        t.start()
    def stop(self):
        self.httpd.shutdown()
    def increase_pending_requests_by_one(self):
        self.pending_requests += 1
        if self.pending_requests == 1:
            t = threading.Thread(target=self.run)
            t.start()
    def get_pending_requests(self):
        return self.pending_requests
    def has_pending_requests(self):
        return self.pending_requests != 0
    def get_completed_requests(self):
        return self.completed_requests

if __name__ == "__main__":
    server = http_server()
    server.increase_pending_requests_by_one()
    #server.threaded_server()
    server.stop()
