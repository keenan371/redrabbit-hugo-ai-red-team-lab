"""Loopback-only control center showing only generated local scan data."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from redrabbit_agent.runner import run_safe_demo

ROOT = Path(__file__).parent


def latest_reports() -> list[dict]:
    reports = []
    for item in sorted((ROOT / "results").glob("*.json"), reverse=True):
        reports.append(json.loads(item.read_text(encoding="utf-8")))
    return reports


def page() -> bytes:
    reports = latest_reports()
    latest = reports[0] if reports else None
    data = json.dumps(latest or {"status": "No local scan has run yet."})
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>RedRabbit vs Hugo</title><style>body{{background:#08111d;color:#e5f3ff;font:16px system-ui;max-width:960px;margin:30px auto}}button{{padding:10px 14px;margin:4px;background:#0f7195;color:white;border:0;border-radius:6px}}pre,.card{{background:#102235;padding:16px;border-radius:8px;white-space:pre-wrap}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}small{{color:#a9bfd1}}</style></head><body><h1>RedRabbit vs. Hugo</h1><p>Local-only controlled AI-security demonstration. No external targets, tools, credentials, or cloud data.</p><div><button onclick="run('baseline')">Start Baseline Demo</button><button onclick="run('hardened')">Start Safe Demo (Hardened)</button></div><div class="grid"><section class="card"><h2>Hugo · Security Watchdog</h2><p>Mode: <span id="mode">{latest['mode'] if latest else 'idle'}</span></p><p>Latest decision: <span id="decision">{latest['results'][-1]['actual_behavior'] if latest else 'none'}</span></p></section><section class="card"><h2>RedRabbit · AI Red Team</h2><p>Fixed catalog: 4 benign simulations</p><p>Progress: <span id="progress">{latest['summary']['total'] if latest else 0}</span>/4</p></section></div><h2>Executive summary</h2><pre id="summary">{data}</pre><h2>Live event timeline</h2><pre id="timeline">Run a local demo to generate real JSONL events.</pre><script>async function run(mode){{let r=await fetch('/api/run',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{mode}})}});let d=await r.json();document.getElementById('summary').textContent=JSON.stringify(d,null,2);document.getElementById('mode').textContent=d.mode;document.getElementById('decision').textContent=d.results[d.results.length-1].actual_behavior;document.getElementById('progress').textContent=d.summary.total;let e=await fetch('/api/events/'+d.scan_id);document.getElementById('timeline').textContent=await e.text();}}</script></body></html>'''.encode()


def build_server(port: int = 8090) -> ThreadingHTTPServer:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self._send(page(), 'text/html; charset=utf-8')
            elif self.path.startswith('/api/events/'):
                scan_id = self.path.rsplit('/', 1)[-1]
                path = ROOT / 'events' / f'{scan_id}.jsonl'
                if path.is_file(): self._send(path.read_bytes(), 'application/jsonl')
                else: self.send_error(HTTPStatus.NOT_FOUND)
            else: self.send_error(HTTPStatus.NOT_FOUND)
        def do_POST(self):
            if self.path != '/api/run': self.send_error(HTTPStatus.NOT_FOUND); return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                payload = json.loads(self.rfile.read(length))
                report = run_safe_demo(str(payload.get('mode')), ROOT)
                self._send(json.dumps(report).encode(), 'application/json')
            except (ValueError, json.JSONDecodeError) as error: self.send_error(HTTPStatus.BAD_REQUEST, str(error))
        def _send(self, body, mime):
            self.send_response(HTTPStatus.OK); self.send_header('Content-Type', mime); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
        def log_message(self, _format, *_args): return
    return ThreadingHTTPServer(('127.0.0.1', port), Handler)

if __name__ == '__main__':
    server = build_server(); print('Control Center: http://127.0.0.1:8090'); server.serve_forever()
