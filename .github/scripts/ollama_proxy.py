#!/usr/bin/env python3
"""Small bearer-token gate in front of Ollama's OpenAI-compatible API."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_KEY = os.environ.get("OLLAMA_API_KEY", "")
UPSTREAM = "http://127.0.0.1:11434"

if len(API_KEY) < 32:
    raise SystemExit("OLLAMA_API_KEY must be set to a random value of at least 32 characters.")

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def respond(self, status, body, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def authorized(self):
        supplied = self.headers.get("Authorization", "")
        # Constant-time comparison avoids leaking key-prefix information.
        import hmac
        expected = "Bearer " + API_KEY
        return hmac.compare_digest(supplied.encode(), expected.encode())

    def forward(self):
        if not self.authorized():
            self.respond(401, b'{"error":{"message":"Unauthorized","type":"authentication_error"}}')
            return
        if self.path not in ("/v1/models", "/v1/chat/completions"):
            self.respond(404, b'{"error":{"message":"Endpoint not supported"}}')
            return
        data = None
        if self.command == "POST":
            length = int(self.headers.get("Content-Length", "0"))
            if length > 2 * 1024 * 1024:
                self.respond(413, b'{"error":{"message":"Request too large"}}')
                return
            data = self.rfile.read(length)
        req = Request(
            UPSTREAM + self.path,
            data=data,
            headers={"Content-Type": self.headers.get("Content-Type", "application/json")},
            method=self.command,
        )
        try:
            with urlopen(req, timeout=300) as response:
                self.respond(response.status, response.read(), response.headers.get("Content-Type", "application/json"))
        except HTTPError as exc:
            self.respond(exc.code, exc.read())
        except (URLError, TimeoutError) as exc:
            self.respond(502, json.dumps({"error":{"message":"Ollama upstream unavailable","detail":str(exc)}}).encode())

    def do_GET(self):
        self.forward()

    def do_POST(self):
        self.forward()

    def log_message(self, fmt, *args):
        # Never log request headers or bearer tokens.
        print("proxy:", fmt % args, flush=True)

ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
