# CitationClaw SPA Workspace Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign CitationClaw's existing SPA into a unified academic workspace UI that references `example.html`, while preserving current backend APIs and critical front-end behavior.

**Architecture:** Keep the current FastAPI + Jinja + vanilla JS SPA structure, but break the UI into shared workspace partials and a single visual system. Use shared shell components and per-workspace partials so `/`, `/config`, `/task`, and `/results` all render the same design language and preserve existing JavaScript hooks. The user explicitly requested working only in the repository root, so implement this plan in the root workspace rather than a separate git worktree.

**Tech Stack:** FastAPI, Jinja2 templates, vanilla JavaScript, Bootstrap utilities/icons, shared CSS in `citationclaw/static/css/style.css`, pytest + FastAPI `TestClient`

---

## File Map

### Create

- `citationclaw/templates/_workspace_page_head.html`
  - Shared page-head partial for workspace title, kicker, description, and action area.
- `citationclaw/templates/_home_workspace.html`
  - Home SPA workspace markup.
- `citationclaw/templates/_config_workspace.html`
  - Config SPA workspace markup reused by `/config` and the SPA config panel.
- `citationclaw/templates/_task_workspace.html`
  - Task SPA workspace markup reused by `/task` and the SPA task panel.
- `test/test_ui_templates.py`
  - Shared UI smoke tests for shell and workspace hooks.
- `docs/superpowers/plans/2026-04-23-spa-workspace-ui-redesign.md`
  - This implementation plan.

### Modify

- `citationclaw/templates/base.html`
  - Shared nav shell and panel container wrappers.
- `citationclaw/templates/index.html`
  - Compose the SPA out of workspace partials instead of inline monolithic sections.
- `citationclaw/templates/config.html`
  - Reuse the shared config workspace partial for standalone route parity.
- `citationclaw/templates/task.html`
  - Reuse the shared task workspace partial for standalone route parity.
- `citationclaw/templates/results.html`
  - Reuse the shared results workspace partial for standalone route parity.
- `citationclaw/templates/_results_workspace.html`
  - Align the results workspace with the same shared shell and rail system.
- `citationclaw/static/css/style.css`
  - Add shared design tokens and all workspace layout styles.
- `citationclaw/static/js/main.js`
  - Adapt SPA routing and DOM interactions to the new workspace structure without changing backend APIs.
- `test/test_results_ui.py`
  - Keep results-specific smoke coverage aligned with the redesigned results workspace.

## Task 1: Build Shared Workspace Shell

**Files:**
- Create: `test/test_ui_templates.py`
- Create: `citationclaw/templates/_workspace_page_head.html`
- Modify: `citationclaw/templates/base.html`
- Modify: `citationclaw/static/css/style.css`

- [ ] **Step 1: Write the failing shell smoke test**

```python
import os
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from citationclaw.app.main import app


client = TestClient(app)


def test_all_routes_render_inside_workspace_shell():
    for route in ["/", "/config", "/task", "/results"]:
        response = client.get(route)
        assert response.status_code == 200
        html = response.text
        assert 'class="cc-app"' in html
        assert 'class="agent-page-content cc-shell"' in html
        assert 'data-spa-panel="home"' in html
        assert 'data-spa-panel="config"' in html
        assert 'data-spa-panel="task"' in html
        assert 'data-spa-panel="results"' in html
```

- [ ] **Step 2: Run the shell smoke test to verify it fails**

Run: `pytest test/test_ui_templates.py::test_all_routes_render_inside_workspace_shell -v`

Expected: FAIL because the current shell still lacks the full four-workspace nav and shared wrapper markers.

- [ ] **Step 3: Implement the shared workspace shell**

Add the shared page-head partial:

```html
<div class="cc-page-head">
  <div>
    <p class="cc-page-kicker">{{ kicker }}</p>
    <h1 class="cc-page-title">{{ title|safe }}</h1>
    {% if description %}
    <p class="cc-page-description">{{ description }}</p>
    {% endif %}
  </div>
  {% if actions %}
  <div class="cc-page-actions">
    {{ actions|safe }}
  </div>
  {% endif %}
</div>
```

Update the shared shell in `citationclaw/templates/base.html`:

```html
<body class="cc-app">
  <nav class="agent-navbar cc-navbar">
    <div class="agent-navbar-inner cc-navbar-inner">
      <a href="/" class="agent-brand cc-brand-lockup">
        <div class="agent-brand-icon">
          <img src="/static/citationclaw_icon.png" width="28" height="28" alt="CitationClaw" style="display:block">
        </div>
        <div>
          <div class="agent-brand-name">CitationClaw</div>
          <div class="agent-brand-sub">Turning Every Citation into Explainable Impact</div>
        </div>
      </a>
      <div class="agent-nav-links cc-nav-links">
        <a href="/" class="agent-nav-link cc-nav-link{% if request.url.path == '/' %} active{% endif %}" data-spa-panel="home">
          <i class="bi bi-house-fill"></i> 首页
        </a>
        <a href="/?panel=config" class="agent-nav-link cc-nav-link" data-spa-panel="config">
          <i class="bi bi-sliders"></i> 配置
        </a>
        <a href="/?panel=task" class="agent-nav-link cc-nav-link{% if request.url.path == '/task' %} active{% endif %}" data-spa-panel="task">
          <i class="bi bi-terminal-fill"></i> 任务
        </a>
        <a href="/?panel=results" class="agent-nav-link cc-nav-link{% if request.url.path == '/results' %} active{% endif %}" data-spa-panel="results">
          <i class="bi bi-folder2-open"></i> 结果
        </a>
      </div>
    </div>
  </nav>

  <div class="agent-page-content cc-shell">
    {% block content %}{% endblock %}
  </div>
</body>
```

Add shell styles in `citationclaw/static/css/style.css`:

```css
.cc-shell {
  max-width: 1440px;
  margin: 0 auto;
  width: 100%;
  padding: 32px 24px 56px;
}

.cc-page-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 24px;
}

.cc-page-kicker {
  margin: 0 0 6px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--accent);
}

.cc-page-title {
  margin: 0;
  font-size: clamp(2rem, 2.6vw, 2.7rem);
  line-height: 1.1;
  letter-spacing: -0.04em;
}
```

- [ ] **Step 4: Run the shell smoke test to verify it passes**

Run: `pytest test/test_ui_templates.py::test_all_routes_render_inside_workspace_shell -v`

Expected: PASS

- [ ] **Step 5: Commit the shared shell**

```bash
git add test/test_ui_templates.py citationclaw/templates/_workspace_page_head.html citationclaw/templates/base.html citationclaw/static/css/style.css
git commit -m "feat: add shared SPA workspace shell"
```

## Task 2: Redesign the Home Workspace

**Files:**
- Create: `citationclaw/templates/_home_workspace.html`
- Modify: `citationclaw/templates/index.html`
- Modify: `citationclaw/static/css/style.css`
- Modify: `test/test_ui_templates.py`

- [ ] **Step 1: Add a failing home-workspace smoke test**

Append this test to `test/test_ui_templates.py`:

```python
def test_home_workspace_keeps_launch_controls_and_workspace_sections():
    html = client.get("/").text

    for token in [
        "cc-home-workspace",
        "cc-home-grid",
        "cc-launch-stack",
        "cc-home-rail",
        'id="paper-input"',
        'id="idx-run-btn"',
        'id="scholar-url-input"',
        'data-spa-panel="config"',
        'data-spa-panel="results"',
    ]:
        assert token in html
```

- [ ] **Step 2: Run the home-workspace smoke test to verify it fails**

Run: `pytest test/test_ui_templates.py::test_home_workspace_keeps_launch_controls_and_workspace_sections -v`

Expected: FAIL because the current home panel is still an inline monolith and lacks the new workspace wrappers.

- [ ] **Step 3: Implement the home workspace partial and include it from the SPA**

Create `citationclaw/templates/_home_workspace.html`:

```html
<div id="spa-panel-home" class="spa-panel spa-panel-active cc-home-workspace">
  {% set kicker = "Academic Workspace" %}
  {% set title = "论文被引<span>画像分析</span>" %}
  {% set description = "输入论文题目，组织分析层级，并从统一的启动台发起任务。" %}
  {% set actions %}
    <a href="#" class="btn btn-outline-primary btn-sm" data-spa-panel="config">
      <i class="bi bi-sliders"></i> 打开配置
    </a>
  {% endset %}
  {% include "_workspace_page_head.html" %}

  <div class="cc-home-grid">
    <section class="cc-launch-stack">
      <div class="agent-card cc-card cc-workspace-panel">
        <div class="agent-card-label"><i class="bi bi-person-badge-fill"></i>&nbsp; 从 Google Scholar 主页导入论文</div>
        <input id="scholar-url-input" type="text" class="form-control" placeholder="https://scholar.google.com/citations?user=...">
      </div>

      <div class="agent-card cc-card cc-workspace-panel">
        <div class="agent-card-label"><i class="bi bi-file-text"></i>&nbsp; 目标论文题目</div>
        <div id="paper-list"></div>
        <input id="paper-input" type="text" autocomplete="off" placeholder="输入论文题目，按回车添加…">
      </div>

      <div class="agent-card cc-card cc-workspace-panel">
        <div class="agent-card-label"><i class="bi bi-layers"></i>&nbsp; 服务层级</div>
        <select id="idx-service-tier" class="form-select form-select-sm"></select>
        <button id="idx-run-btn" class="btn-agent-primary"><i class="bi bi-play-fill"></i> 开始分析</button>
      </div>
    </section>

    <aside class="cc-home-rail">
      <div class="cc-rail-card">
        <h3>运行摘要</h3>
        <div id="global-progress" class="spa-global-progress"></div>
      </div>
      <div class="cc-rail-card">
        <h3>快捷入口</h3>
        <a href="#" data-spa-panel="results">查看结果</a>
      </div>
    </aside>
  </div>
</div>
```

Replace the old inline home section in `citationclaw/templates/index.html` with:

```html
{% include "_home_workspace.html" %}
```

Add the home layout styles:

```css
.cc-home-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(280px, 0.9fr);
  gap: 24px;
}

.cc-launch-stack,
.cc-home-rail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cc-workspace-panel,
.cc-rail-card {
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  padding: 20px;
}
```

- [ ] **Step 4: Run the home-workspace smoke test to verify it passes**

Run: `pytest test/test_ui_templates.py::test_home_workspace_keeps_launch_controls_and_workspace_sections -v`

Expected: PASS

- [ ] **Step 5: Commit the home workspace redesign**

```bash
git add citationclaw/templates/_home_workspace.html citationclaw/templates/index.html citationclaw/static/css/style.css test/test_ui_templates.py
git commit -m "feat: redesign home workspace"
```

## Task 3: Redesign the Config Workspace

**Files:**
- Create: `citationclaw/templates/_config_workspace.html`
- Modify: `citationclaw/templates/index.html`
- Modify: `citationclaw/templates/config.html`
- Modify: `citationclaw/static/css/style.css`
- Modify: `test/test_ui_templates.py`

- [ ] **Step 1: Add a failing config-workspace smoke test**

Append this test to `test/test_ui_templates.py`:

```python
def test_config_workspace_keeps_form_and_testing_hooks():
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
```

- [ ] **Step 2: Run the config-workspace smoke test to verify it fails**

Run: `pytest test/test_ui_templates.py::test_config_workspace_keeps_form_and_testing_hooks -v`

Expected: FAIL because `/config` still renders the old single-form layout.

- [ ] **Step 3: Implement the config workspace partial and reuse it in both routes**

Create `citationclaw/templates/_config_workspace.html`:

```html
<div{% if embedded %} id="spa-panel-config" class="spa-panel" style="display:none"{% else %} class="cc-config-workspace"{% endif %}>
  {% set kicker = "System Settings" %}
  {% set title = "配置工作区 / Config Workspace" %}
  {% set description = "集中管理 API、模型、Prompt、筛选策略和运行参数。" %}
  {% include "_workspace_page_head.html" %}

  <div class="cc-config-grid">
    <section class="cc-config-main">
      <form id="config-form" class="cc-form-shell">
        <section class="cc-form-section">
          <h3 class="cc-form-section-title">API 配置</h3>
          <textarea id="scraper-api-keys" class="form-control font-monospace" rows="3"></textarea>
          <input id="openai-api-key" type="text" class="form-control font-monospace" placeholder="your-api-key">
        </section>

        <section class="cc-form-section">
          <h3 class="cc-form-section-title">Prompt 配置</h3>
          <textarea id="author-search-prompt1" class="form-control font-monospace" rows="3"></textarea>
          <textarea id="author-search-prompt2" class="form-control font-monospace" rows="4"></textarea>
        </section>
      </form>
    </section>

    <aside class="cc-config-rail">
      <div id="existing-files-alert" class="cc-rail-card" style="display:none;"></div>
      <div class="cc-rail-card">
        <h3>API 测试</h3>
        <button type="button" id="test-api-btn" class="btn btn-outline-primary">测试 API 连接和 Web Search</button>
      </div>
    </aside>
  </div>
</div>
```

Reuse the partial in `citationclaw/templates/index.html` and `citationclaw/templates/config.html`:

```html
{% set embedded = True %}
{% include "_config_workspace.html" %}
```

```html
{% set embedded = False %}
{% include "_config_workspace.html" %}
```

Add config layout styles:

```css
.cc-config-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.8fr) minmax(290px, 0.9fr);
  gap: 24px;
}

.cc-config-main,
.cc-config-rail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cc-form-shell {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: transparent;
  border: 0;
  box-shadow: none;
}

.cc-form-section {
  padding: 20px;
  border: 1px solid #edf2f7;
  background: #fff;
}

.cc-form-section-title {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 700;
}
```

- [ ] **Step 4: Run the config-workspace smoke test to verify it passes**

Run: `pytest test/test_ui_templates.py::test_config_workspace_keeps_form_and_testing_hooks -v`

Expected: PASS

- [ ] **Step 5: Commit the config workspace redesign**

```bash
git add citationclaw/templates/_config_workspace.html citationclaw/templates/index.html citationclaw/templates/config.html citationclaw/static/css/style.css test/test_ui_templates.py
git commit -m "feat: redesign config workspace"
```

## Task 4: Redesign the Task Workspace

**Files:**
- Create: `citationclaw/templates/_task_workspace.html`
- Modify: `citationclaw/templates/index.html`
- Modify: `citationclaw/templates/task.html`
- Modify: `citationclaw/static/css/style.css`
- Modify: `test/test_ui_templates.py`

- [ ] **Step 1: Add a failing task-workspace smoke test**

Append this test to `test/test_ui_templates.py`:

```python
def test_task_workspace_keeps_terminal_and_control_hooks():
    html = client.get("/task").text

    for token in [
        "cc-task-workspace",
        "cc-task-grid",
        "cc-terminal-card",
        "cc-task-rail",
        'id="log-container"',
        'id="progress-bar"',
        'id="ws-status"',
        'id="continue-btn"',
        'id="cancel-btn"',
    ]:
        assert token in html
```

- [ ] **Step 2: Run the task-workspace smoke test to verify it fails**

Run: `pytest test/test_ui_templates.py::test_task_workspace_keeps_terminal_and_control_hooks -v`

Expected: FAIL because `/task` still renders the old Bootstrap card layout.

- [ ] **Step 3: Implement the task workspace partial and standalone route reuse**

Create `citationclaw/templates/_task_workspace.html`:

```html
<div{% if embedded %} id="spa-panel-task" class="spa-panel" style="display:none"{% else %} class="cc-task-workspace"{% endif %}>
  {% set kicker = "Execution Console" %}
  {% set title = "任务监控 / Task Monitor" %}
  {% set description = "在统一控制台中查看日志、阶段进度与执行控制。" %}
  {% include "_workspace_page_head.html" %}

  <div class="cc-task-grid">
    <section class="cc-terminal-card">
      <div class="cc-terminal-head">
        <h3>任务日志</h3>
        <span id="ws-status" class="cc-status-chip">连接中...</span>
      </div>
      <div id="log-container" class="log-terminal"></div>
      <div class="cc-terminal-foot">
        <button id="clear-logs-btn" class="btn btn-sm btn-outline-secondary">清空日志</button>
        <button id="auto-scroll-btn" class="btn btn-sm btn-outline-primary active">自动滚动</button>
      </div>
    </section>

    <aside class="cc-task-rail">
      <div class="cc-rail-card">
        <h3>任务进度</h3>
        <div id="progress-bar" class="progress-bar bg-success" style="width:0%">0%</div>
      </div>
      <div class="cc-rail-card">
        <h3>任务控制</h3>
        <button id="continue-btn" class="btn btn-success btn-lg" style="display:none;">继续执行阶段2/3</button>
        <button id="cancel-btn" class="btn btn-danger" style="display:none;">取消任务</button>
      </div>
    </aside>
  </div>
</div>
```

Reuse the partial in `citationclaw/templates/index.html` and `citationclaw/templates/task.html`:

```html
{% set embedded = True %}
{% include "_task_workspace.html" %}
```

```html
{% set embedded = False %}
{% include "_task_workspace.html" %}
```

Add task layout styles:

```css
.cc-task-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.75fr) minmax(300px, 0.9fr);
  gap: 24px;
}

.cc-terminal-card {
  border: 1px solid var(--cc-border);
  background: var(--cc-surface);
  box-shadow: var(--cc-shadow-md);
}

.cc-task-rail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
```

- [ ] **Step 4: Run the task-workspace smoke test to verify it passes**

Run: `pytest test/test_ui_templates.py::test_task_workspace_keeps_terminal_and_control_hooks -v`

Expected: PASS

- [ ] **Step 5: Commit the task workspace redesign**

```bash
git add citationclaw/templates/_task_workspace.html citationclaw/templates/index.html citationclaw/templates/task.html citationclaw/static/css/style.css test/test_ui_templates.py
git commit -m "feat: redesign task workspace"
```

## Task 5: Rebuild the Results Workspace as a Shared Browsing Surface

**Files:**
- Modify: `citationclaw/templates/_results_workspace.html`
- Modify: `citationclaw/templates/index.html`
- Modify: `citationclaw/templates/results.html`
- Modify: `citationclaw/static/css/style.css`
- Modify: `test/test_results_ui.py`

- [ ] **Step 1: Add a failing results smoke test that enforces the shared workspace shape**

Update `test/test_results_ui.py` to assert the final shared results structure:

```python
def test_results_workspace_markup_is_shared_between_home_panel_and_standalone_page():
    home = client.get("/?panel=results").text
    results = client.get("/results").text

    for html in (home, results):
        for token in [
            "cc-results-workspace",
            "cc-results-layout",
            "cc-results-main",
            "cc-results-rail",
            'id="results-folder-list"',
            'id="results-table"',
            'id="results-panel-title"',
            'id="results-quick-stats"',
            'id="results-recent-list"',
        ]:
            assert token in html
```

- [ ] **Step 2: Run the results smoke test to verify it fails**

Run: `pytest test/test_results_ui.py::test_results_workspace_markup_is_shared_between_home_panel_and_standalone_page -v`

Expected: FAIL if the results markup still differs between embedded and standalone modes.

- [ ] **Step 3: Finalize the shared results workspace partial**

Keep the results partial as the canonical shared browsing surface:

```html
<div class="cc-results-workspace" data-results-mode="{{ 'embedded' if results_embedded else 'standalone' }}">
  {% set kicker = "Academic Workspace" %}
  {% set title = "结果文件夹 <span>/ Results Folder</span>" %}
  {% set description = "按分析批次浏览导出结果，支持快速预览 HTML 报告、下载结构化文件，并查看最近更新。" %}
  {% include "_workspace_page_head.html" %}

  <div class="cc-results-layout">
    <section class="cc-results-main">
      <div class="cc-results-panel">
        <div class="cc-results-panel-head">
          <div class="cc-results-panel-heading">
            <div class="cc-results-panel-icon"><i class="bi bi-folder2-open"></i></div>
            <div>
              <p class="cc-results-panel-label">Current Analysis Set</p>
              <h2 id="results-panel-title" class="cc-results-panel-title">结果文件夹</h2>
            </div>
          </div>
        </div>
        <div id="results-folder-view">
          <div id="results-folder-list" class="cc-results-grid cc-results-folder-grid"></div>
        </div>
        <div id="results-file-view" style="display:none;">
          <div id="results-table" class="cc-results-grid cc-results-file-grid"></div>
        </div>
      </div>
    </section>

    <aside class="cc-results-rail">
      <div id="results-quick-stats" class="cc-results-stats"></div>
      <div class="cc-results-rail-card">
        <h3>Recent Activity</h3>
        <div id="results-recent-list" class="cc-results-recent-list"></div>
      </div>
    </aside>
  </div>
</div>
```

Reuse it from both `citationclaw/templates/index.html` and `citationclaw/templates/results.html`:

```html
{% set results_embedded = True %}
{% include "_results_workspace.html" %}
```

```html
{% set results_embedded = False %}
{% include "_results_workspace.html" %}
```

Add the shared results browsing styles:

```css
.cc-results-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.85fr) minmax(290px, 0.95fr);
  gap: 24px;
}

.cc-results-main,
.cc-results-rail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cc-results-grid {
  display: grid;
  gap: 16px;
}

.cc-results-folder-grid,
.cc-results-file-grid {
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}
```

- [ ] **Step 4: Run the results smoke test to verify it passes**

Run: `pytest test/test_results_ui.py::test_results_workspace_markup_is_shared_between_home_panel_and_standalone_page -v`

Expected: PASS

- [ ] **Step 5: Commit the shared results workspace**

```bash
git add citationclaw/templates/_results_workspace.html citationclaw/templates/index.html citationclaw/templates/results.html citationclaw/static/css/style.css test/test_results_ui.py
git commit -m "feat: unify results workspace surface"
```

## Task 6: Adapt SPA JavaScript to the New Workspace Structure

**Files:**
- Modify: `citationclaw/static/js/main.js`
- Modify: `test/test_ui_templates.py`
- Modify: `test/test_results_ui.py`

- [ ] **Step 1: Add a failing test that locks the SPA hook inventory**

Append this test to `test/test_ui_templates.py`:

```python
def test_spa_panels_preserve_critical_dom_hooks():
    html = client.get("/").text

    for token in [
        'id="spa-panel-home"',
        'id="spa-panel-config"',
        'id="spa-panel-task"',
        'id="spa-panel-results"',
        'id="global-progress"',
        'id="results-back-btn"',
        'id="loading-indicator"',
        'id="empty-state"',
    ]:
        assert token in html
```

- [ ] **Step 2: Run the SPA hook smoke test to verify it fails**

Run: `pytest test/test_ui_templates.py::test_spa_panels_preserve_critical_dom_hooks -v`

Expected: FAIL if the redesigned panel composition dropped any current JavaScript hook.

- [ ] **Step 3: Adapt `main.js` to the new structure without changing API contracts**

Refactor SPA initialization to tolerate standalone pages and partial-based panels:

```javascript
function initResultsPanel() {
    document.querySelectorAll('[data-results-refresh]').forEach(button => {
        button.addEventListener('click', () => {
            loadResults();
        });
    });

    if (window.location.pathname === '/results') {
        loadResults();
    }
}

var SpaRouter = (function () {
    let _currentPanel = 'home';

    function init() {
        if (!document.querySelector('.spa-panel')) {
            return;
        }

        document.addEventListener('click', function (e) {
            var link = e.target.closest('[data-spa-panel]');
            if (!link) return;
            e.preventDefault();
            switchTo(link.dataset.spaPanel);
        });
    }

    return { init: init, switchTo: switchTo, current: function () { return _currentPanel; } };
})();
```

Keep results DOM hook helpers resilient:

```javascript
function _resultsSetLoading(show) {
    const loading = document.getElementById('loading-indicator');
    if (loading) loading.style.display = show ? 'grid' : 'none';
}

function _resultsShowView(view) {
    const emptyState = document.getElementById('empty-state');
    const folderView = document.getElementById('results-folder-view');
    const fileView = document.getElementById('results-file-view');
    const backBtn = document.getElementById('results-back-btn');

    if (emptyState) emptyState.style.display = view === 'empty' ? 'grid' : 'none';
    if (folderView) folderView.style.display = view === 'folders' ? 'block' : 'none';
    if (fileView) fileView.style.display = view === 'files' ? 'block' : 'none';
    if (backBtn) backBtn.style.display = view === 'files' ? 'inline-flex' : 'none';
}
```

- [ ] **Step 4: Run syntax and hook verification**

Run:

```bash
pytest test/test_ui_templates.py::test_spa_panels_preserve_critical_dom_hooks -v
node --check citationclaw/static/js/main.js
```

Expected:

- pytest: PASS
- node: exit code 0 with no output

- [ ] **Step 5: Commit the JavaScript adaptation**

```bash
git add citationclaw/static/js/main.js test/test_ui_templates.py test/test_results_ui.py
git commit -m "feat: adapt SPA hooks for redesigned workspaces"
```

## Task 7: Final Regression Pass and Visual Unification

**Files:**
- Modify: `citationclaw/static/css/style.css`
- Modify: `citationclaw/templates/index.html`
- Modify: `citationclaw/templates/config.html`
- Modify: `citationclaw/templates/task.html`
- Modify: `citationclaw/templates/results.html`
- Modify: `test/test_ui_templates.py`
- Modify: `test/test_results_ui.py`

- [ ] **Step 1: Add a failing stylesheet smoke test for the shared visual system**

Append this test to `test/test_ui_templates.py`:

```python
from pathlib import Path


def test_stylesheet_contains_shared_workspace_tokens():
    css = Path("citationclaw/static/css/style.css").read_text(encoding="utf-8")

    for token in [
        ".cc-page-actions {",
        ".cc-page-description {",
        ".cc-config-rail {",
        ".cc-status-chip {",
        "@media (max-width: 820px) {",
        "@media (max-width: 640px) {",
    ]:
        assert token in css
```

- [ ] **Step 2: Run the stylesheet smoke test to verify it fails**

Run: `pytest test/test_ui_templates.py::test_stylesheet_contains_shared_workspace_tokens -v`

Expected: FAIL until the shared stylesheet is fully unified around the workspace design system.

- [ ] **Step 3: Finish visual unification and responsive cleanup**

Complete the final CSS pass so all four workspaces use the same system:

```css
@media (max-width: 1100px) {
  .cc-home-grid,
  .cc-config-grid,
  .cc-task-grid,
  .cc-results-layout {
    grid-template-columns: 1fr;
  }
}

.cc-page-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.cc-page-description {
  max-width: 760px;
  margin: 12px 0 0;
  color: var(--muted);
  line-height: 1.75;
}

.cc-config-rail {
  min-width: 0;
}

.cc-rail-card {
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  padding: 20px;
}

.cc-status-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

@media (max-width: 820px) {
  .cc-page-head {
    flex-direction: column;
    align-items: stretch;
  }
}

@media (max-width: 640px) {
  .cc-home-grid,
  .cc-config-grid,
  .cc-task-grid,
  .cc-results-layout {
    gap: 16px;
  }
}
```

Keep standalone routes aligned with SPA partials:

```html
{% set embedded = False %}
{% include "_config_workspace.html" %}
```

```html
{% set embedded = False %}
{% include "_task_workspace.html" %}
```

```html
{% set results_embedded = False %}
{% include "_results_workspace.html" %}
```

- [ ] **Step 4: Run the full verification suite**

Run:

```bash
pytest test/test_ui_templates.py test/test_results_ui.py -v
node --check citationclaw/static/js/main.js
docker compose up -d --build
curl -s http://localhost:8000/results | rg -n "cc-results-workspace|cc-results-layout|results-quick-stats"
curl -s http://localhost:8000/ | rg -n "cc-home-workspace|spa-panel-config|spa-panel-task|spa-panel-results"
```

Expected:

- pytest: all UI smoke tests PASS
- node: exit code 0 with no output
- docker compose: container starts without naming conflicts
- first curl: prints lines containing `cc-results-workspace`, `cc-results-layout`, and `results-quick-stats`
- second curl: prints lines containing `cc-home-workspace`, `spa-panel-config`, `spa-panel-task`, and `spa-panel-results`

- [ ] **Step 5: Commit the final unification**

```bash
git add citationclaw/static/css/style.css citationclaw/templates/index.html citationclaw/templates/config.html citationclaw/templates/task.html citationclaw/templates/results.html test/test_ui_templates.py test/test_results_ui.py
git commit -m "feat: finish SPA workspace redesign"
```
