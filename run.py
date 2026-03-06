"""
Flask wrapper to serve Streamlit app with static file support for PWA.
This enables proper serving of manifest.json and service worker files.
"""
import os
import sys
import subprocess
import threading
import time
from flask import Flask, send_from_directory
import requests

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Routes for static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/service-worker.js')
def serve_service_worker():
    response = send_from_directory('static', 'service-worker.js')
    response.headers['Content-Type'] = 'application/javascript'
    return response

# Proxy everything else to Streamlit
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_streamlit(path):
    try:
        # Forward request to Streamlit running on localhost:8501
        url = f'http://localhost:8501/{path}'
        headers = {k: v for k, v in dict(request.headers).items() if k.lower() not in ['host', 'connection']}
        
        if request.method == 'GET':
            resp = requests.get(url, headers=headers, params=request.args)
        elif request.method == 'POST':
            resp = requests.post(url, headers=headers, json=request.json, data=request.data)
        else:
            resp = requests.request(request.method, url, headers=headers)
        
        return resp.content, resp.status_code, dict(resp.headers)
    except Exception as e:
        return f"Error: {str(e)}", 500

def run_streamlit():
    """Run Streamlit in a separate thread"""
    time.sleep(2)  # Give Flask time to start
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port=8501",
        "--server.address=localhost",
        "--logger.level=error",
        "--client.showErrorDetails=false"
    ])

if __name__ == '__main__':
    # Start Streamlit in background
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    streamlit_thread.start()
    
    # Start Flask
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
