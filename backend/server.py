from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import threading

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("index.html", "rb") as file:
                self.wfile.write(file.read())

        elif self.path.startswith("/welcome"):
            params = parse_qs(urlparse(self.path).query)
            username = params.get("username", [""])[0]
            if username == "":
                username = 'visitante'
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("welcome.html", "rb") as file:
                content = file.read().decode("utf-8").replace("{{ username }}", username)
                self.wfile.write(content.encode())

        elif self.path == "/shutdown":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Servidor encerrado.")
            threading.Thread(target=self.server.shutdown).start()

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("not_found.html", "rb") as file:
                self.wfile.write(file.read())
    def do_POST(self):
        if self.path == "/submit":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            params = parse_qs(post_data)
            username = params.get("username", [""])[0]
            self.send_response(302)
            self.send_header("Location", f"/welcome?username={username}")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("not_found.html", "rb") as file:
                self.wfile.write(file.read())
def run():
    port = 8000
    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Servidor rodando na porta {port}. Use Ctrl+C para encerrar.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Servidor encerrado.")

if __name__ == "__main__":
    run()


