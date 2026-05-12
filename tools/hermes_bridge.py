#!/usr/bin/env python3
"""
Hermes → Echo Bridge
Receives POST from Hermes → forwards to KiloClaw hooks endpoint → injects into Echo session
"""
import http.server, json, urllib.request, os

HOOKS_URL = "http://localhost:3001/hooks/hermes"
HOOKS_TOKEN = "bce208a9eedb58cd673cff1538bf8b778d3b8bd71058a7ed02249dcbf65bc57b"
BRIDGE_SECRET = open("/root/.secrets/ecdash_token").read().strip()

class BridgeHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[bridge] {self.address_string()} {fmt % args}")

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "echo-hermes-bridge"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != "/message":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        auth = self.headers.get("Authorization", "")
        if auth != f"Bearer {BRIDGE_SECRET}":
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error":"unauthorized"}')
            return

        try:
            data = json.loads(body)
            message = data.get("message", "")
            source = data.get("source", "hermes")
            if not message:
                raise ValueError("No message")
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        payload = json.dumps({"message": f"[From {source}]: {message}"}).encode()
        req = urllib.request.Request(
            HOOKS_URL, data=payload,
            headers={"Authorization": f"Bearer {HOOKS_TOKEN}", "Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                result = json.load(r)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "delivered", "runId": result.get("runId")}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

if __name__ == "__main__":
    PORT = 9876
    server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), BridgeHandler)
    print(f"[bridge] Echo-Hermes bridge on :{PORT}")
    server.serve_forever()
