"""
OmniStream Pro - Extension Localhost Bridge Server
Listens on 127.0.0.1:28795 for incoming video stream capture jobs from browser extensions.
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from typing import Optional

BRIDGE_PORT = 28795

class BridgeHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress standard logging to avoid terminal clutter
        pass

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            response = {
                "status": "ok",
                "app": "OmniStream Pro",
                "version": "1.0.0",
                "bridge": "active"
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self._send_cors_headers()
            self.end_headers()

    def do_POST(self):
        if self.path == "/add":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                post_body = self.rfile.read(content_len).decode("utf-8")
                data = json.loads(post_body)

                # Pass job to OmniStream App main queue
                app = getattr(self.server, "app_instance", None)
                if app and hasattr(app, "log_queue"):
                    app.log_queue.put(("bridge_job", data))

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self._send_cors_headers()
                self.end_headers()
                response = {"success": True, "message": "Stream queued successfully in OmniStream Pro"}
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self._send_cors_headers()
                self.end_headers()
                response = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self._send_cors_headers()
            self.end_headers()


class BridgeServer:
    def __init__(self, app_instance, port: int = BRIDGE_PORT):
        self.app_instance = app_instance
        self.port = port
        self.httpd: Optional[HTTPServer] = None
        self.thread: Optional[threading.Thread] = None
        self.is_running = False

    def start(self):
        try:
            self.httpd = HTTPServer(("127.0.0.1", self.port), BridgeHandler)
            self.httpd.app_instance = self.app_instance
            self.is_running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            return True
        except OSError:
            # Port already in use or permission denied
            self.is_running = False
            return False

    def _run(self):
        try:
            if self.httpd:
                self.httpd.serve_forever()
        except Exception:
            pass

    def stop(self):
        self.is_running = False
        if self.httpd:
            try:
                self.httpd.shutdown()
                self.httpd.server_close()
            except Exception:
                pass
