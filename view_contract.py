"""Shared UI contract for the DLP demo viewer + copilot.

Just view names and Streamlit session-state keys — no logic, no IP. The viewer
(app.py) depends on this; the copilot (copilot.py) reuses it so navigation
targets stay in sync. Safe to ship in a public read-only build.
"""
# View name → display label (with icon). VIEWS is derived from this, so the tab
# list and its labels are a SINGLE source of truth and can never drift out of
# sync (which would make a radio format_func return None and crash the app).
VIEW_ICON = {
    "Demo overview": "📖 Demo overview",
    "Coverage & diversity": "🌈 Coverage & diversity",
    "Findings": "🔍 Findings",
    "Research & decisions": "🔬 Research & decisions",
}
VIEWS = list(VIEW_ICON)

K_VIEW, K_CARRIER = "view", "leak_carrier"
K_FCAT, K_FCHAL, K_FSURF, K_FPER = "f_cat", "f_chal", "f_surf", "f_per"
K_FOCUS = "focus_value"
