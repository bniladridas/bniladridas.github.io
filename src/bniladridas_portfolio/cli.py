import argparse
import http.server
import os
import pathlib
import socketserver
import sys
import webbrowser
from importlib import resources

def get_static_dir() -> pathlib.Path:
    # Single source: when running from checkout, serve directly from Site root
    try:
        checkout_root = pathlib.Path(__file__).resolve().parents[2]
        if (checkout_root / "index.html").is_file():
            return checkout_root
    except Exception:
        pass
    # When installed, static lives inside the package (populated via force-include)
    try:
        pkg_files = resources.files("bniladridas_portfolio")  # type: ignore
        p = pkg_files / "static"
        if p.is_dir():
            return pathlib.Path(str(p))
    except Exception:
        pass
    return pathlib.Path(__file__).parent / "static"

def serve(host: str, port: int, open_browser: bool):
    static = get_static_dir()
    if not static.is_dir():
        print(f"Static dir not found: {static}", file=sys.stderr)
        sys.exit(1)
    os.chdir(static)
    handler = http.server.SimpleHTTPRequestHandler
    # allow reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((host, port), handler) as httpd:
        url = f"http://{host}:{port}/"
        print(f"Serving portfolio at {url}  (static: {static})")
        print("Press Ctrl+C to stop.")
        if open_browser:
            try:
                webbrowser.open(url)
            except Exception:
                pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")

def main():
    p = argparse.ArgumentParser(prog="portfolio", description="Portfolio server for bniladridas")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("serve", help="Serve the portfolio locally")
    s.add_argument("--host", default="127.0.0.1", help="Host (default 127.0.0.1)")
    s.add_argument("--port", type=int, default=8000, help="Port (default 8000)")
    s.add_argument("--open", action="store_true", help="Open browser")
    s.add_argument("--no-open", dest="open", action="store_false", help="Do not open browser")
    s.set_defaults(open=False)
    args = p.parse_args()
    if args.cmd == "serve":
        serve(args.host, args.port, args.open)

if __name__ == "__main__":
    main()
