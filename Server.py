from http.server import BaseHTTPRequestHandler

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Error response if URL path contains the word error
            if("error" in self.path):
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>My Service</title></head>", "utf-8"))
                self.wfile.write(bytes("<p>Request Path: %s</p>" % self.path, "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes("<h1>Error Page!</h1>", "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>My Service</title></head>", "utf-8"))
                self.wfile.write(bytes("<p>Request Path: %s</p>" % self.path, "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes("<h1>This is an example web server.</p>", "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))
        except:
            print("SERVER ERROR!!!!")