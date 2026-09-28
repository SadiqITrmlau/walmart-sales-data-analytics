import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

# Change working directory to current file directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and disable caching during local development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def run_server():
    global PORT
    for attempt in range(10):
        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                url = f"http://localhost:{PORT}"
                print("=" * 60)
                print(f"  Walmart BI Dashboard - Created by Sadiq Khan")
                print(f"  Server is running at: {url}")
                print(f"  Press Ctrl+C in this terminal to stop the server")
                print("=" * 60)
                webbrowser.open(url)
                httpd.serve_forever()
                break
        except OSError as e:
            if "Address already in use" in str(e) or e.errno == 10048:
                PORT += 1
            else:
                raise e

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nServer stopped successfully.")
