# DLP demo — Streamlit viewer (multi-session)

Read-only viewer for synthetic DLP demo-data sessions. No model, no credentials,
no network — just `streamlit + pandas + plotly`. The in-app Claude copilot is
**disabled** here (it only mounts when `DLP_COPILOT=1` is set with
Bedrock/Anthropic creds, which this deploy never sets).

All data under `sessions/` is **entirely synthetic** — fabricated values with
realistic *shape* (format-valid keys/SSNs/contacts), never real people or live
credentials.

## How it works
- The app loads every `sessions/<name>/` folder that contains a `PLANTED_INDEX.csv`.
- **One session →** it just shows it. **Multiple →** a **"Demo session" picker**
  appears in the sidebar; a `?session=<name>` URL opens one directly (shareable link).
- Add a prospect later by dropping a new `sessions/<name>/` folder in and pushing —
  no code changes.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repo (**private recommended** — see note).
2. share.streamlit.io → **New app** → pick repo + branch, **main file = `app.py`**.
3. (Recommended) **Settings → Sharing**: restrict viewers to an email allowlist.
4. No secrets needed (copilot off). Deploy → one URL serves all bundled sessions.

## ⚠️ Note on the synthetic data
`sessions/*/carriers/` contains format-valid **secret-shaped** strings
(AWS-key-like, DB URLs) and **PII-shaped** strings (SSNs, emails, phones). They are
fake, but GitHub **secret scanning / push protection** may flag the repo, and the
app *looks* like it exposes credentials/PII. Keep the repo **private** and the app
**viewer-restricted**. To avoid scanner noise, replace secret-shaped values with
obviously-fake placeholders before pushing (trades a little detector-realism for
quiet hosting).

## Layout
```
app.py                 # the read-only viewer
view_contract.py       # shared UI constants (view names + state keys)
requirements.txt · .streamlit/config.toml
sessions/
  apollo-io/           # a demo session: PLANTED_INDEX.csv, carriers/, research.json, session.json, ...
  <next-prospect>/     # add more here; the picker lists them automatically
```
