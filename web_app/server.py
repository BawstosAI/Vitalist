#!/usr/bin/env python3
"""
Simple HTTP server to run the Vitalist web app.
Run this script from the web_app directory.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow loading JSON files
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

def main():
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    Handler = MyHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}/index.html"
            print(f"\n{'='*60}")
            print(f"🚀 Vitalist Web App Server")
            print(f"{'='*60}")
            print(f"\nServer running at: {url}")
            print(f"\nPress Ctrl+C to stop the server\n")
            print(f"{'='*60}\n")
            
            # Try to open browser automatically
            try:
                webbrowser.open(url)
            except:
                pass
            
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 98 or e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use.")
            print(f"   Try a different port: python server.py {PORT + 1}")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            sys.exit(1)
    main()
