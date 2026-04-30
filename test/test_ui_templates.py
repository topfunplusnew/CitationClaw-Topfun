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


def test_workspace_nav_omits_same_page_section_links():
    html = client.get("/").text

    assert 'href="/#scholar-import-card"' not in html
    assert 'href="/#service-tier-card"' not in html
    assert ">Imports<" not in html
    assert ">Service Levels<" not in html


def test_workspace_uses_site_logo_asset():
    html = client.get("/").text

    assert Path("citationclaw/static/assets/logo.jpg").is_file()
    assert 'href="/static/assets/logo.jpg"' in html
    assert 'src="/static/assets/logo.jpg"' in html
    assert 'src="/static/citationclaw_icon.png"' not in html


def test_workspace_pages_use_spark_brand_name():
    for route in ["/", "/config", "/task", "/results", "/notice"]:
        html = client.get(route).text

        assert "Spark" in html
        assert "CitationClaw" not in html


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
        'id="idx-enable-year-traverse"',
        'class="cc-rail-actions"',
        'class="cc-rail-actions-primary"',
        'class="cc-rail-actions-secondary"',
        'id="idx-progress-section"',
        'id="idx-log-section"',
        'id="idx-results-section"',
    ]:
        assert token in html

    assert "cc-preview-card" not in html
    assert "Citation Lineage Map Preview" not in html
    assert "System Notice" not in html
    assert "启动前提示" not in html
    assert "导入 Google Scholar 前，请先填写" not in html


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
        ".cc-home-detail-grid",
        ".cc-config-grid",
        ".cc-config-card",
        ".cc-task-grid",
        ".cc-terminal-card",
        ".cc-rail-card",
        ".cc-app #scholar-import-card",
        ".cc-app #scholar-import-card .cc-mini-panel-head",
        ".cc-rail-actions",
        ".cc-rail-actions-primary",
        ".cc-rail-actions-secondary",
        "object-fit: cover;",
    ]:
        assert token in css

    assert ".cc-home-detail-grid {\n  grid-template-columns: 1fr;" in css
    assert ".cc-preview-card" not in css


def test_config_saves_immediately_and_home_autosaves():
    js = Path("citationclaw/static/js/main.js").read_text(encoding="utf-8")
    html = client.get("/").text

    assert "cc-toast-container" in html
    assert "function showOperationToast" in js
    assert "showOperationToast('success'" in js
    assert "showOperationToast('error'" in js
    assert "async function saveMergedConfig" in js
    assert "await saveConfigNow();" in js
    assert "const indexConfigInputs" in js
    assert "idx-enable-year-traverse" in js
    html_count = client.get("/").text.count('id="enable-year-traverse"')
    assert html_count == 1
    assert "idx-save-config-btn" in js
    assert "input', autoSaveIndexConfig" in js
    assert "change', autoSaveIndexConfig" in js
