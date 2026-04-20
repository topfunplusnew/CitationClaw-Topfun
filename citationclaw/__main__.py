"""
CitationClaw — 论文被引画像分析🦞

Usage:
    citationclaw          # start web server at http://0.0.0.0:8000
    citationclaw --port 8080
    citationclaw --no-browser
"""

import argparse
import threading
import time
import webbrowser
import sys


def build_parser():
    parser = argparse.ArgumentParser(
        prog="citationclaw",
        description="CitationClaw — 论文被引画像分析🦞",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    return parser


def browser_url_for_host(host: str, port: int) -> str:
    browser_host = "127.0.0.1" if host == "0.0.0.0" else host
    return f"http://{browser_host}:{port}"


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        import uvicorn
        from citationclaw.app.main import app
    except ImportError as e:
        print("=" * 60)
        print("错误: 缺少依赖包!")
        print(f"详细信息: {e}")
        print("\n请先安装依赖:")
        print("  pip install citationclaw")
        print("=" * 60)
        sys.exit(1)

    print(f"\n  CitationClaw 🦞  →  http://{args.host}:{args.port}\n")

    if not args.no_browser:
        def _open_browser():
            time.sleep(1.5)
            try:
                webbrowser.open(browser_url_for_host(args.host, args.port))
            except Exception:
                pass
        threading.Thread(target=_open_browser, daemon=True).start()

    try:
        uvicorn.run(app, host=args.host, port=args.port, log_level="warning")
    except KeyboardInterrupt:
        print("\nCitationClaw stopped.")


if __name__ == "__main__":
    main()
