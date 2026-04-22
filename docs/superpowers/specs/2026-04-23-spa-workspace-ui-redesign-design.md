# CitationClaw SPA Workspace UI Redesign

- Date: 2026-04-23
- Scope: Web UI redesign for the existing SPA experience
- Reference: `example.html`
- Decision: Use a unified SPA workspace design, keep existing backend APIs and core behaviors

## Goal

Redesign the current web UI so the app feels like a coherent academic workspace instead of several loosely connected Bootstrap pages and panels. The redesign should clearly reference the visual language of `example.html`, while adapting it to the actual CitationClaw workflow.

The redesign must keep the current SPA model, existing backend routes, and existing core interactions. It may reorganize layout, information architecture, templates, styling, and front-end structure where necessary.

## Non-Goals

- Rewriting the backend API
- Changing the core business workflow
- Introducing a new frontend framework
- Using this redesign as a pretext for unrelated refactors

## Product Direction

The target UI is an academic workspace:

- Light background with disciplined spacing and high information clarity
- Hard-edged cards and restrained motion
- Blue as the primary accent color
- A clear distinction between primary work surfaces and secondary information rails
- SPA navigation that feels like full pages rather than hidden sections inside one long screen

This should feel inspired by `example.html`, not copied one-to-one.

## Information Architecture

The app remains a SPA with four primary workspaces:

1. `home`
   - Purpose: launchpad and overview
   - Primary responsibilities: paper input, Scholar import, service tier selection, run action
   - Secondary responsibilities: recent activity, run summary, shortcuts, reminders

2. `config`
   - Purpose: system settings workspace
   - Primary responsibilities: API configuration, models, prompts, filtering and verification settings, output and runtime parameters
   - Secondary responsibilities: saved-state feedback, test tools, configuration guidance, existing-file reminders

3. `task`
   - Purpose: execution monitoring workspace
   - Primary responsibilities: live logs, progress, phase status, task control
   - Secondary responsibilities: import history, continue flow, execution summaries

4. `results`
   - Purpose: results browsing workspace
   - Primary responsibilities: browse result folders, inspect files, open reports, download outputs
   - Secondary responsibilities: recent result activity, quick stats, file-type guide

The homepage no longer acts as the place where every detail lives. It becomes the launchpad. The other panels become complete workspace views inside the SPA shell.

## Shared Shell

The redesign introduces a shared workspace shell used by all four panels.

### Shared shell responsibilities

- Consistent top navigation
- Consistent page head pattern
- Consistent workspace panel and rail card system
- Consistent loading, empty, and error-state treatment
- Consistent typography, spacing, border, and button rules

### Shared navigation

The top bar remains global and persistent across the SPA. It should expose:

- Brand lockup
- Primary navigation for `home`, `config`, `task`, and `results`
- A clear active state for the current workspace
- Optional global progress or status summary entry point

## Shared Design System

### Visual language

- Light canvas
- Structured whitespace
- Sharp card boundaries
- Strong title hierarchy
- Minimal but intentional hover feedback
- No decorative gradients beyond subtle background atmosphere
- No over-animated or playful UI treatment

### Shared component families

- Page head
- Workspace panel
- Rail card
- Status chip
- Primary action button
- Secondary action button
- Metric card
- List card
- Terminal card
- Empty-state block
- Loading block
- Error-state block

### Interaction rules

- Hover effects are restrained: border emphasis, slight text shift, mild elevation
- Active states are signaled by border and color, not giant colored blocks
- Empty states always include the next action
- Error states always include recovery actions when possible

## Workspace Layouts

## Home Workspace

### Purpose

Serve as the launchpad for new analysis runs and as a summary of current system activity.

### Layout

Two-column workspace:

- Left main column:
  - hero / page head
  - paper input stack
  - Scholar import card
  - service tier card
  - primary run controls
- Right rail:
  - recent task summary
  - global progress summary
  - key reminders
  - shortcut actions to config and results

### Behavioral decision

The homepage should no longer carry the entire advanced configuration form. Instead:

- Keep only the minimum launch-critical information on the home workspace
- Show whether required configuration is complete
- Route detailed editing to the config workspace

## Config Workspace

### Purpose

Provide a dedicated, comprehensible settings workspace.

### Layout

Two-column workspace:

- Left main column:
  - API configuration section
  - model configuration section
  - prompt configuration section
  - scholar filter / author verification section
  - output and runtime section
- Right rail:
  - saved configuration summary
  - API test panel
  - existing-results reminder
  - configuration guidance links

### Structural rule

The configuration page should use multiple independently titled section cards, not one long undifferentiated form.

## Task Workspace

### Purpose

Act as an execution console.

### Layout

Two-column workspace:

- Left main column:
  - live terminal/log panel
  - progress and current phase context
- Right rail:
  - task controls
  - phase cards
  - import-history controls
  - continue / cancel / result navigation

### Visual rule

The log area should feel like the dominant operational surface. Supporting controls should look subordinate but accessible.

## Results Workspace

### Purpose

Provide a browsing workflow for folders and result files.

### Layout

Two-column workspace:

- Left main column:
  - results page head
  - folder grid or file grid depending on context
- Right rail:
  - quick stats
  - recent activity
  - file-type guide

### Navigation rule

Results flow remains:

1. See result batches / folders
2. Open a folder
3. Browse files
4. Download files or open HTML reports

The redesign changes presentation, not the functional flow.

## Data Flow and State Handling

### Data flow

- Keep the existing SPA router model
- Keep the existing backend APIs
- Let each workspace load its own data independently
- Keep detailed execution content inside `task`
- Allow high-level run status to surface globally

### Required visible states per workspace

Each workspace must support:

- default state
- loading state
- empty state
- error state

### State behavior requirements

- Loading states should share visual language and structure
- Empty states must explain what to do next
- Error states must identify the failed area and provide recovery paths

## Compatibility Rules

The redesign may change template structure, wrappers, and layout composition, but it must preserve current behavior.

### Must preserve

- Paper input and restoration
- Scholar import workflow
- Config load and save
- Task start, cancel, continue, and import history
- Results browsing, download, and report viewing

### Frontend compatibility strategy

- Preserve current critical DOM hooks where JavaScript depends on them
- Add wrappers freely where needed
- Prefer adapting current `main.js` before considering large-scale rewrite
- Only reorganize JS where existing structure materially blocks the redesign

## Testing Strategy

### UI smoke coverage

Add or update smoke tests so they verify:

- Shared shell exists
- Home workspace keeps run-critical controls
- Config workspace keeps form-critical controls
- Task workspace keeps log/progress-critical containers
- Results workspace keeps folder/file browsing containers

### Scope of tests

- Structural and hook-presence validation only
- No fragile pixel-based testing
- No visual snapshot system required for this redesign

## Implementation Order

1. Build the shared workspace shell and design tokens
2. Redesign `home`
3. Redesign `config`
4. Redesign `task`
5. Redesign `results`
6. Unify polish across all workspaces
7. Run smoke verification

## Acceptance Criteria

The redesign is successful when:

- All four workspaces share one coherent visual system
- The app visibly references the style and discipline of `example.html`
- The SPA feels like a set of intentional workspaces, not a stack of patched panels
- Existing backend APIs and core flows still work
- Critical front-end hooks required by current JS remain intact
- Loading, empty, and error states are consistent across workspaces

## Open Constraint Decisions Already Resolved

- Redesign scope: all primary web workspaces
- Reference fidelity: use `example.html` as reference, not a literal copy
- Navigation model: keep SPA
- Freedom to change layout: yes, as long as existing core interactions and APIs remain intact
