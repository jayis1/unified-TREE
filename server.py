#!/usr/bin/env python3
"""unified TREE registry API and zero-dependency dashboard server."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class TreeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB), **kwargs)

    def send_json(self, value, status=200):
        payload = json.dumps(value, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            devices = load_json("devices.json")["devices"]
            self.send_json({
                "status": "ready",
                "service": "unified TREE",
                "time": datetime.now(timezone.utc).isoformat(),
                "node_types": len(devices),
            })
        elif path == "/api/nodes":
            self.send_json(load_json("devices.json"))
        elif path == "/api/topology":
            self.send_json(load_json("platform.json"))
        elif path == "/api/summary":
            devices = load_json("devices.json")["devices"]
            self.send_json({
                "nodes": len(devices),
                "domains": dict(sorted(Counter(d["domain"] for d in devices).items())),
                "roles": dict(sorted(Counter(r for d in devices for r in d["roles"]).items())),
            })
        elif path.startswith("/api/"):
            self.send_json({"error": "not found"}, 404)
        else:
            super().do_GET()

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)
    server = ThreadingHTTPServer((args.host, args.port), TreeHandler)
    print(f"unified TREE dashboard: http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping unified TREE.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
