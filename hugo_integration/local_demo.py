"""Loopback-only browser interface for Hugo's local security demonstration."""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from hugo_integration.hugo_watchdog import HugoWatchdog

PAGE = """<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><title>Hugo Security Watchdog</title>
<style>body{max-width:760px;margin:40px auto;font:16px system-ui;background:#0c1622;color:#e8f1ff}textarea,button{font:inherit}textarea{width:100%;min-height:110px}button{margin-top:12px;padding:10px 16px}.card{white-space:pre-wrap;background:#14263b;padding:16px;border-radius:8px}</style>
</head><body><h1>Hugo: Security Watchdog</h1><p>Local-only controlled demonstration. No external tools or data access.</p>
<textarea id=\"message\" placeholder=\"Enter a safe local demonstration prompt\"></textarea><br><button id=\"send\">Send to Hugo</button>
<h2>Security decision</h2><div id=\"result\" class=\"card\">Awaiting a local prompt.</div>
<script>document.getElementById('send').onclick=async()=>{const message=document.getElementById('message').value;const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})});document.getElementById('result').textContent=JSON.stringify(await r.json(),null,2)};</script>
</body></html>"""


def build_server(mode: str = "hardened", port: int = 8088) -> ThreadingHTTPServer:
    watchdog = HugoWatchdog(
        mode=mode,
        log_path=Path("hugo_integration/logs/hugo-decisions.jsonl"),
    )

    class LocalHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path != "/":
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            self._send_json_or_html(PAGE.encode("utf-8"), "text/html; charset=utf-8")

        def do_POST(self) -> None:
            if self.path != "/api/chat":
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 5000:
                    raise ValueError("invalid request size")
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                result = watchdog.handle_message(payload.get("message", ""))
                self._send_json_or_html(json.dumps(result).encode("utf-8"), "application/json")
            except (ValueError, json.JSONDecodeError) as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))

        def _send_json_or_html(self, body: bytes, content_type: str) -> None:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format: str, *_args: object) -> None:
            return

    return ThreadingHTTPServer(("127.0.0.1", port), LocalHandler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Hugo's local-only Security Watchdog demo.")
    parser.add_argument("--mode", choices=("baseline", "hardened"), default="hardened")
    parser.add_argument("--port", type=int, default=8088)
    args = parser.parse_args()
    server = build_server(mode=args.mode, port=args.port)
    print(f"Hugo local demo: http://127.0.0.1:{server.server_port} ({args.mode} mode)")
    print("Loopback-only. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nHugo local demo stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
