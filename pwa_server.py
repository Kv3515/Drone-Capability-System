#!/usr/bin/env python3
"""
Reverse proxy server that handles both Streamlit app and static files.
Routes /static/* to local files, proxies everything else to Streamlit.
"""
import os
import sys
import subprocess
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen
import json
import mimetypes

class DualServerHandler(BaseHTTPRequestHandler):
    """Handle both static files and proxy to Streamlit"""
    
    def do_GET(self):
        # Handle static files directly
        if self.path.startswith('/static/'):
            self.serve_static_file(self.path[8:])
        elif self.path == '/manifest.json':
            self.serve_static_file('manifest.json')
        elif self.path == '/service-worker.js':
            self.serve_static_file('service-worker.js')
        else:
            # Proxy to Streamlit
            self.proxy_to_streamlit()
    
    def serve_static_file(self, filepath):
        """Serve a static file from the static directory"""
        file_path = os.path.join('static', filepath)
        
        if not os.path.exists(file_path):
            self.send_error(404, f'File not found: {filepath}')
            return
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            if filepath.endswith('.json'):
                mime_type = 'application/json'
            elif filepath.endswith('.js'):
                mime_type = 'application/javascript'
            else:
                mime_type = 'application/octet-stream'
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', len(content))
            self.send_header('Cache-Control', 'public, max-age=3600')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, str(e))
    
    def proxy_to_streamlit(self):
        """Proxy request to Streamlit running on port 8501"""
        try:
            streamlit_url = f'http://localhost:8501{self.path}'
            
            # Create request to Streamlit
            req = urlopen(streamlit_url, timeout=10)
            content = req.read()
            
            self.send_response(req.status)
            for header, value in req.headers.items():
                if header.lower() not in ['content-encoding', 'transfer-encoding']:
                    self.send_header(header, value)
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(502, f'Bad Gateway: {str(e)}')
    
    def log_message(self, format, *args):
        # Minimal logging
        if '/static/' not in self.path:
            print(f'[{self.client_address[0]}] {format % args}')

def start_streamlit():
    """Start Streamlit in a background thread"""
    time.sleep(2)  # Wait for server to be ready
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--server.port=8501',
        '--server.address=localhost',
        '--logger.level=error',
        '--client.showErrorDetails=false'
    ])

def run_server(port=10000):
    """Run the dual-purpose server"""
    # Start Streamlit in background
    streamlit_thread = threading.Thread(target=start_streamlit, daemon=True)
    streamlit_thread.start()
    
    server = HTTPServer(('0.0.0.0', port), DualServerHandler)
    print(f'PWA Server with Streamlit proxy running on port {port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down...')
        server.shutdown()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    run_server(port)

