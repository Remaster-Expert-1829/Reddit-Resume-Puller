import http.server
import socketserver
import subprocess
import json

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/refresh':
            try:
                # Run main.py which pulls the latest data
                result = subprocess.run(['python', 'main.py'], capture_output=True, text=True)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                if result.returncode == 0:
                    response = {'status': 'success', 'message': 'Data refreshed successfully!'}
                else:
                    response = {'status': 'error', 'message': 'Script failed.', 'error': result.stderr}
                    
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'status': 'error', 'message': str(e)}
                self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "File not found")

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print("This server can handle the /api/refresh POST request.")
        print("Press Ctrl+C to stop.")
        httpd.serve_forever()
