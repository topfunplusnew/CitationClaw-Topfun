"""Unit tests for CLI defaults."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from citationclaw.__main__ import browser_url_for_host, build_parser


def test_default_host_is_public_bind_address():
    args = build_parser().parse_args([])
    assert args.host == "0.0.0.0"


def test_host_flag_still_allows_override():
    args = build_parser().parse_args(["--host", "127.0.0.1"])
    assert args.host == "127.0.0.1"


def test_public_bind_opens_browser_on_loopback():
    assert browser_url_for_host("0.0.0.0", 8000) == "http://127.0.0.1:8000"
