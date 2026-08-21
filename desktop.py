#!/usr/bin/env python3
"""Launch unified TREE like a desktop application."""

import socket
import threading
import webbrowser

import server


def available_port(start=8080, attempts=20):
    for port in range(start, start + attempts):
        with socket.socket() as candidate:
            try:
                candidate.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError("No local dashboard port is available")


def main():
    port = available_port()
    url = f"http://127.0.0.1:{port}"
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    return server.main(["--host", "127.0.0.1", "--port", str(port)])


if __name__ == "__main__":
    raise SystemExit(main())
