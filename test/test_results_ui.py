import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from citationclaw.app.main import app


client = TestClient(app)


def test_results_workspace_markup_is_shared_between_home_and_results():
    home = client.get("/").text
    results = client.get("/results").text

    for html in (home, results):
        for token in [
            "cc-results-workspace",
            "cc-results-layout",
            "cc-results-grid",
            'id="results-folder-list"',
            'id="results-table"',
            'id="results-panel-title"',
            'id="results-quick-stats"',
            'id="results-recent-list"',
        ]:
            assert token in html


def test_results_workspace_styles_exist_in_root_stylesheet():
    css = Path("citationclaw/static/css/style.css").read_text(encoding="utf-8")
    for token in [
        ".cc-results-workspace {",
        ".cc-results-layout {",
        ".cc-results-panel {",
        ".cc-results-grid {",
        ".cc-folder-card {",
        ".cc-file-card {",
        ".cc-results-rail {",
    ]:
        assert token in css
