import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from citationclaw.app.main import app


client = TestClient(app)


def test_workspace_shell_renders_shared_nav_and_actions():
    for route in ["/", "/config", "/task", "/results"]:
        response = client.get(route)
        assert response.status_code == 200
        html = response.text

        for token in [
            'class="cc-app"',
            'class="agent-page-content cc-shell"',
            'data-spa-panel="home"',
            'cc-navbar-search',
            'cc-navbar-cta',
        ]:
            assert token in html


def test_home_workspace_keeps_dashboard_hooks():
    html = client.get("/").text

    for token in [
        "cc-home-workspace",
        "cc-home-grid",
        "cc-home-main",
        "cc-home-rail",
        "cc-summary-stats",
        'id="paper-input"',
        'id="scholar-url-input"',
        'id="idx-run-btn"',
        'id="idx-progress-section"',
        'id="idx-log-section"',
        'id="idx-results-section"',
    ]:
        assert token in html


def test_config_workspace_keeps_form_hooks():
    html = client.get("/config").text

    for token in [
        "cc-config-workspace",
        "cc-config-grid",
        "cc-config-main",
        "cc-config-rail",
        'id="config-form"',
        'id="scraper-api-keys"',
        'id="openai-api-key"',
        'id="test-api-btn"',
        'id="existing-files-alert"',
    ]:
        assert token in html


def test_task_workspace_keeps_control_hooks():
    html = client.get("/task").text

    for token in [
        "cc-task-workspace",
        "cc-task-grid",
        "cc-task-main",
        "cc-task-rail",
        'id="log-container"',
        'id="progress-bar"',
        'id="ws-status"',
        'id="continue-btn"',
        'id="cancel-btn"',
    ]:
        assert token in html


def test_workspace_styles_cover_shared_shell_and_workspace_primitives():
    css = Path("citationclaw/static/css/style.css").read_text(encoding="utf-8")

    for token in [
        ".cc-navbar-tools",
        ".cc-navbar-search",
        ".cc-shell",
        ".cc-page-head",
        ".cc-summary-card",
        ".cc-home-grid",
        ".cc-home-card",
        ".cc-config-grid",
        ".cc-config-card",
        ".cc-task-grid",
        ".cc-terminal-card",
        ".cc-rail-card",
    ]:
        assert token in css
