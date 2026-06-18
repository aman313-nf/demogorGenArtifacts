"""Shared UI contract for the DLP demo viewer + copilot.

Just view names and Streamlit session-state keys — no logic, no IP. The viewer
(app.py) depends on this; the copilot (copilot.py) reuses it so navigation
targets stay in sync. Safe to ship in a public read-only build.
"""
VIEWS = ["Demo overview", "Leaks in context", "Coverage & diversity", "Planted index",
         "Research & decisions", "Detector results"]

K_VIEW, K_CARRIER = "view", "leak_carrier"
K_FCAT, K_FCHAL, K_FSURF, K_FPER = "f_cat", "f_chal", "f_surf", "f_per"
K_FOCUS = "focus_value"
