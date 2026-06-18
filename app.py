"""Interactive Streamlit visualizer + Claude copilot for a DLP demo-data session.

Data-driven: point it at a session folder (the `<company>_demo_data/` dir) via
DLP_SESSION_DIR and it renders the demo story, the leaks-in-context view, the
diversity/coverage picture, and a filterable planted index. An optional
sidebar copilot (Bedrock/Anthropic) can navigate the app (Tier 1) and adjust the
synthetic data/config (Tier 2). With no credentials the copilot hides itself and
the app stays fully usable offline.

Launch:
    DLP_SESSION_DIR=/path/to/<company>_demo_data \
      uv run --with streamlit --with pandas --with plotly --with boto3 \
      streamlit run scripts/app.py
"""
from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

import view_contract as vc  # shared, non-proprietary UI contract (VIEWS + state keys)

def _discover_sessions() -> list[Path]:
    """Return the candidate session folder(s), in priority order:
    1. DLP_SESSION_DIR (single, explicit — unchanged local behavior);
    2. every `sessions/<name>/` subdir with a PLANTED_INDEX.csv (multi → picker);
    3. a bundled `./session/` or the app dir itself; else any subdir with an index."""
    env = os.environ.get("DLP_SESSION_DIR")
    if env:
        return [Path(env).expanduser().resolve()]
    here = Path(__file__).resolve().parent
    base = here / "sessions"
    if base.is_dir():
        subs = sorted(p.resolve() for p in base.iterdir()
                      if p.is_dir() and (p / "PLANTED_INDEX.csv").exists())
        if subs:
            return subs
    if (here / "session" / "PLANTED_INDEX.csv").exists():
        return [(here / "session").resolve()]
    if (here / "PLANTED_INDEX.csv").exists():
        return [here]
    subs = sorted(p.resolve() for p in here.iterdir()
                  if p.is_dir() and (p / "PLANTED_INDEX.csv").exists())
    return subs or [Path(".").resolve()]


def _session_label(p: Path) -> str:
    try:
        return json.loads((p / "session.json").read_text()).get("company", p.name)
    except Exception:
        return p.name


# Copilot is OFF by default — opt in with DLP_COPILOT=1 (needs Bedrock/Anthropic
# creds). Hosted/public deploys leave it off: the app stays a read-only viewer.
COPILOT_ENABLED = os.environ.get("DLP_COPILOT", "").strip().lower() in ("1", "true", "yes", "on")

_SESSIONS = _discover_sessions()

st.set_page_config(page_title="DLP demo data", layout="wide")

CHAL_LABEL = {"straightforward": "🎯 straightforward", "fp_near_miss": "🟡 FP near-miss",
              "fn_evasive": "🫥 FN evasive"}
CHAL_COLOR = {"straightforward": "#e8590c", "fp_near_miss": "#f5c518", "fn_evasive": "#1c7ed6"}
CAT_COLOR = {"secret": "#e03131", "confidential": "#9c36b5", "PII": "#1971c2", "financial": "#2f9e44"}
VIEW_ICON = {"Demo overview": "📖 Demo overview", "Coverage & diversity": "🌈 Coverage & diversity",
             "Findings": "🔍 Findings", "Research & decisions": "🔬 Research & decisions"}
DET_BADGE = {"detected": "✅ detected", "missed": "❌ missed", "false_positive": "🟥 fired (FP)",
             "correctly_quiet": "🟢 quiet", "not_integrated": "⬜ not integrated", "scan_error": "⚠️ error"}
CONF_COLOR = {"high": "#2f9e44", "medium": "#f08c00", "low": "#e8590c"}
STATUS_COLOR = {"confirmed": "#2f9e44", "proposed": "#f08c00", "rejected": "#868e96"}


def md_safe(s) -> str:
    return str(s).replace("$", "\\$")           # avoid Streamlit `$...$` LaTeX math


def html_safe(s) -> str:
    return html.escape(str(s)).replace("$", "&#36;")


def highlight(text: str, values: list[str]) -> str:
    enc = lambda t: html.escape(t).replace("$", "&#36;")
    esc = enc(text)
    spans = []
    for v in values:
        if not v:
            continue
        v = str(v).split("…")[0].replace("\\n", "\n")
        for piece in [p for p in v.split("\n") if len(p.strip()) >= 4]:
            spans.append(enc(piece))
    for s in sorted(set(spans), key=len, reverse=True):
        esc = esc.replace(s, f"\x00{s}\x01")
    return esc.replace("\x00", "<mark style='background:#ffe066;padding:0 2px'>").replace("\x01", "</mark>")


PRE_STYLE = ("white-space:pre-wrap;font-size:12px;background:#0e1117;color:#e6e6e6;"
             "padding:12px;border-radius:6px;overflow-x:auto")


def item_card(r) -> str:
    badge = CHAL_LABEL.get(r["detection_challenge"], r["detection_challenge"])
    return (f"<div style='border-left:4px solid {CAT_COLOR.get(r['category'],'#888')};"
            f"padding:4px 10px;margin-bottom:8px'>"
            f"<b>{html_safe(r['category'])} / {html_safe(r['data_type'])}</b> &nbsp;"
            f"<span style='font-size:12px'>{badge}</span><br>"
            f"<code style='font-size:11px'>{html_safe(str(r['value'])[:60])}</code><br>"
            f"<span style='font-size:12px;color:#aaa'>@ {html_safe(r['location'])}</span><br>"
            f"<span style='font-size:13px'>{html_safe(r['why_it_lands'])}</span></div>")


def carrier_pre(file, values) -> str | None:
    fpath = CARRIERS / str(file)
    if not fpath.exists():
        return None
    return f"<pre style='{PRE_STYLE}'>{highlight(fpath.read_text(encoding='utf-8', errors='replace'), values)}</pre>"


@st.cache_data
def load(session_dir_str: str):
    session_dir = Path(session_dir_str)
    idx = session_dir / "PLANTED_INDEX.csv"
    if not idx.exists():
        return None, {}, ""
    df = pd.read_csv(idx).fillna("")
    sess = {}
    sp = session_dir / "session.json"
    if sp.exists():
        try:
            sess = json.loads(sp.read_text())
        except json.JSONDecodeError:
            sess = {}
    story = ""
    mp = session_dir / "PLANTED_INDEX.md"
    if mp.exists():
        m = re.search(r"##\s*The demo story\s*(.+?)(?:\n##\s|\Z)", mp.read_text(), re.S)
        if m:
            story = m.group(1).strip()
    if not story:
        story = sess.get("profile_summary", "")
    return df, sess, story


# ---- choose the session (sidebar picker when more than one is bundled) ------
if len(_SESSIONS) > 1:
    names = [p.name for p in _SESSIONS]
    if "session_pick" not in st.session_state:
        qp = st.query_params.get("session")
        st.session_state["session_pick"] = names.index(qp) if qp in names else 0
    idx_pick = st.sidebar.selectbox(
        "Demo session", range(len(_SESSIONS)), key="session_pick",
        format_func=lambda i: _session_label(_SESSIONS[i]))
    SESSION_DIR = _SESSIONS[idx_pick]
    st.query_params["session"] = SESSION_DIR.name   # shareable deep link
else:
    SESSION_DIR = _SESSIONS[0]
IDX = SESSION_DIR / "PLANTED_INDEX.csv"
CARRIERS = SESSION_DIR / "carriers"

df, sess, story = load(str(SESSION_DIR))
if df is None:
    st.title("DLP demo data")
    st.error(f"No PLANTED_INDEX.csv under {SESSION_DIR}. Set DLP_SESSION_DIR or add a `sessions/<name>/` folder.")
    st.stop()

company = sess.get("company", SESSION_DIR.name)
sid = sess.get("session_id", "")
cfg = sess.get("config", {})

# ---- session state (these keys are the copilot↔UI contract) ----------------
ss = st.session_state
ss.setdefault(vc.K_VIEW, vc.VIEWS[0])
ss.setdefault(vc.K_CARRIER, sorted(df["file"].unique())[0])
for k in (vc.K_FCAT, vc.K_FCHAL, vc.K_FSURF, vc.K_FPER):
    ss.setdefault(k, [])
ss.setdefault(vc.K_FOCUS, None)

# ---- mount the copilot FIRST (off by default): its dispatch sets nav state ---
if COPILOT_ENABLED:
    import copilot  # internal-only; intentionally NOT shipped in the public read-only build
    copilot.render_copilot(SESSION_DIR, df, cfg)

# ---- sanitize copilot/user-set view against current options -----------------
if ss[vc.K_VIEW] not in vc.VIEWS:
    ss[vc.K_VIEW] = vc.VIEWS[0]


# --------------------------------------------------------------------------- #
# Views
# --------------------------------------------------------------------------- #
def render_overview():
    c = st.columns(6)
    c[0].metric("Carriers", df["file"].nunique())
    c[1].metric("Planted items", len(df))
    c[2].metric("Distinct values", df["value"].nunique())
    c[3].metric("Categories", df["category"].nunique())
    c[4].metric("Surfaces", df["surface"].nunique())
    c[5].metric("Personas", df["persona"].nunique())
    if story:
        st.markdown("### The demo story")
        st.markdown(md_safe(story))
    st.markdown("### Precision vs. recall framing")
    cc = df["detection_challenge"].value_counts()
    p = st.columns(3)
    p[0].metric("🎯 True positives to catch", int(cc.get("straightforward", 0)))
    p[1].metric("🟡 Must NOT alert (precision)", int(cc.get("fp_near_miss", 0)))
    p[2].metric("🫥 Evasive (recall)", int(cc.get("fn_evasive", 0)))


def render_coverage():
    total, distinct = len(df), df["value"].nunique()
    d = st.columns(3)
    d[0].metric("Total plants", total)
    d[1].metric("Distinct values", distinct)
    d[2].metric("Duplicate values", total - distinct)
    st.markdown("### Category × surface coverage")
    fig = px.imshow(pd.crosstab(df["category"], df["surface"]), text_auto=True,
                    aspect="auto", color_continuous_scale="Blues")
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, width="stretch")
    st.markdown("### Context spread per data type")
    st.caption("Distinct surfaces / files / challenges per data type. Single-surface rows are diversity gaps.")
    g = df.groupby("data_type").agg(
        plants=("value", "size"), distinct_values=("value", "nunique"),
        files=("file", "nunique"), surfaces=("surface", "nunique"),
        challenges=("detection_challenge", "nunique"),
    ).sort_values(["surfaces", "plants"], ascending=False)
    g["context_gap"] = g["surfaces"].eq(1).map({True: "⚠️ single-surface", False: ""})
    st.dataframe(g, width="stretch")
    cols = st.columns(2)
    with cols[0]:
        st.markdown("### Challenge mix by category")
        cc = df.groupby(["category", "detection_challenge"]).size().reset_index(name="n")
        fig = px.bar(cc, x="category", y="n", color="detection_challenge", color_discrete_map=CHAL_COLOR)
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0), legend_title="")
        st.plotly_chart(fig, width="stretch")
    with cols[1]:
        st.markdown("### Who leaks what (personas)")
        pc = df["persona"].value_counts().reset_index(); pc.columns = ["persona", "n"]
        fig = px.bar(pc, x="n", y="persona", orientation="h")
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, width="stretch")
    st.markdown("### Surfaces")
    sc = df["surface"].value_counts().reset_index(); sc.columns = ["surface", "n"]
    fig = px.bar(sc, x="surface", y="n"); fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, width="stretch")


def render_research():
    rp = SESSION_DIR / "research.json"
    if not rp.exists():
        st.info("No `research.json` for this session. The skill records its company research "
                "(findings + sources) and the design decisions (choice → rationale → what it drove) here, "
                "so the *reasoning* behind the demo is inspectable — not just the output.")
        return
    try:
        R = json.loads(rp.read_text())
    except json.JSONDecodeError:
        st.error("research.json is not valid JSON")
        return
    findings = R.get("findings", [])
    hypotheses = R.get("hypotheses", [])
    decisions = R.get("decisions", [])
    oq = R.get("open_questions", [])
    st.caption(f"How this demo was designed for **{R.get('company', company)}**"
               + (f" · researched {R['researched_at']}" if R.get("researched_at") else ""))
    m = st.columns(4)
    m[0].metric("Research findings", len(findings))
    m[1].metric("Risk hypotheses", len(hypotheses))
    m[2].metric("Design decisions", len(decisions))
    m[3].metric("Open questions", len(oq))

    if R.get("narrative"):
        st.markdown("### Demo thesis")
        st.markdown(md_safe(R["narrative"]))

    if hypotheses:
        st.markdown("### Prospect-specific risk hypotheses")
        st.caption("Non-obvious use cases derived from what's distinctive about this prospect — "
                   "the discovery questions to confirm with them.")
        for h in hypotheses:
            stt = h.get("status", "proposed")
            tag = (f"<span style='font-size:11px;color:#fff;background:{STATUS_COLOR.get(stt,'#868e96')};"
                   f"padding:1px 6px;border-radius:8px'>{html_safe(stt)}</span>")
            st.markdown(f"<div style='border-left:3px solid #e8590c;padding:3px 10px;margin-bottom:8px'>"
                        f"{tag} <b>{html_safe(h.get('hypothesis',''))}</b><br>"
                        f"<span style='font-size:12px;color:#aaa'>basis: {html_safe(h.get('basis',''))}</span></div>",
                        unsafe_allow_html=True)

    if findings:
        st.markdown("### What we learned about the prospect")
        for f in findings:
            conf = f.get("confidence", "")
            tag = (f"<span style='font-size:11px;color:#fff;background:{CONF_COLOR.get(conf,'#868e96')};"
                   f"padding:1px 6px;border-radius:8px'>{html_safe(conf)}</span>") if conf else ""
            src = str(f.get("source", ""))
            src_html = (f"  ·  <a href='{html.escape(src)}' target='_blank'>source</a>"
                        if src.startswith("http") else (f"  ·  {html_safe(src)}" if src else ""))
            st.markdown(f"<div style='border-left:3px solid #4263eb;padding:3px 10px;margin-bottom:8px'>"
                        f"<b>{html_safe(f.get('topic','—'))}</b> {tag}<br>"
                        f"<span style='font-size:13px'>{html_safe(f.get('finding',''))}</span>"
                        f"<span style='font-size:12px;color:#aaa'>{src_html}</span></div>",
                        unsafe_allow_html=True)

    if decisions:
        st.markdown("### Why these choices (research → design)")
        for d in decisions:
            st.markdown(f"<div style='border-left:3px solid #9c36b5;padding:3px 10px;margin-bottom:8px'>"
                        f"<b>{html_safe(d.get('area','—'))}:</b> {html_safe(d.get('choice',''))}<br>"
                        f"<span style='font-size:13px'>{html_safe(d.get('rationale',''))}</span><br>"
                        f"<span style='font-size:12px;color:#aaa'>→ drove: {html_safe(d.get('drove',''))}</span></div>",
                        unsafe_allow_html=True)

    if oq:
        st.markdown("### Open questions / caveats")
        for q in oq:
            st.markdown(f"- {md_safe(q)}")


def _dp_overlap(finding: str, value: str) -> bool:
    f = str(finding).strip().lower()
    v = str(value).split("…")[0].replace("\\n", "\n").strip().strip("'\"").lower()
    return bool(f and v and (f in v or v in f))


def _run_detector_ui(nf, tfile, tvalue, tdtype):
    """Manual-run controls + live scan for one resolved data point."""
    default_det = nf.detector_for(tdtype)
    # reset the detector choice to the row's default whenever the target changes
    tgt = f"{tfile}|{tdtype}|{str(tvalue)[:40]}"
    if st.session_state.get("_det_tgt") != tgt:
        st.session_state["_det_tgt"] = tgt
        st.session_state["det_choice"] = [default_det] if default_det else []
    det_values = [d["value"] for d in nf.DETECTORS]
    st.multiselect("Detector(s) to run", det_values, format_func=nf.label_for, key="det_choice")
    conf = st.selectbox("Min confidence", nf.MIN_CONFIDENCE, key="det_conf")
    st.caption(f"Most-relevant detector for `{tdtype}`: "
               f"**{nf.label_for(default_det) if default_det else 'none — not integrated'}**. "
               "Scans the carrier text in context (context affects detection).")
    chosen = st.session_state.get("det_choice", [])
    if st.button("▶ Run scan", key="det_run"):
        if not chosen:
            st.warning("Pick at least one detector.")
            return
        carrier = CARRIERS / tfile
        text = carrier.read_text(encoding="utf-8", errors="replace") if carrier.exists() else str(tvalue)
        try:
            finds = nf.scan(text, chosen, conf)
        except nf.ScanError as e:
            st.error(f"scan failed (network?): {e}")
            return
        caught = sorted({f["detector_name"] for f in finds if _dp_overlap(f["finding"], tvalue)})
        if caught:
            st.success(f"This data point **was caught** by: {', '.join(caught)}")
        else:
            st.info("This data point was **not caught** by the selected detector(s) "
                    "(evasive value, wrong detector, or correctly ignored near-miss).")
        if finds:
            st.dataframe(pd.DataFrame([{
                "detector": f["detector_name"], "finding": str(f["finding"])[:60],
                "confidence": f["confidence"], "start": f["start_index"], "end": f["end_index"],
            } for f in finds]), width="stretch", hide_index=True)
        else:
            st.caption("No findings returned for the selected detector(s) on this carrier.")


def render_findings():
    """One workspace: every planted item with its detector status, filters, and a
    row-select detail (carrier in context + talking point + detector result + run)."""
    try:
        import nf_playground as nf
    except Exception:
        nf = None
    rp = SESSION_DIR / "detector_results.json"
    R = json.loads(rp.read_text()) if rp.exists() else None
    det = {}
    if R:
        for it in R["items"]:
            det[(it["file"], it["location"], str(it["value"]))] = it

    def item_of(r):
        return det.get((r["file"], r["location"], str(r["value"])))

    def status_of(r):
        it = item_of(r)
        return it["status"] if it else None

    # ---- report-card summary (if scanned) ----
    if R:
        s = R["summary"]
        c = st.columns(6)
        c[0].metric("✅ Detected", s["detected"])
        c[1].metric("❌ Missed", s["missed"], help="planted true positives the relevant detector missed (recall gap)")
        c[2].metric("🟥 Fired on FP", s["false_positive"], help="near-misses the detector wrongly flagged (precision miss)")
        c[3].metric("🟢 Quiet on FP", s["correctly_quiet"], help="near-misses correctly ignored")
        c[4].metric("⬜ Not integrated", s["not_integrated"])
        rec, prec = s.get("recall_pct"), s.get("precision_quiet_pct")
        c[5].metric("Recall", f"{rec}%" if rec is not None else "—",
                    help=f"precision on near-misses: {prec}%" if prec is not None else None)
    else:
        st.info("No detector report card yet — run `scripts/scan.py --dir <session>` to add detector "
                "status. Planted items still show below; you can also run a detector manually on any row.")

    # ---- filters: status · category · challenge · carrier file ----
    for key, col in [(vc.K_FCAT, "category"), (vc.K_FCHAL, "detection_challenge")]:
        opts = sorted(df[col].unique())
        ss[key] = [v for v in ss.get(key, []) if v in opts]
    statuses = sorted({status_of(r) or "not scanned" for _, r in df.iterrows()})
    fc = st.columns(4)
    fstatus = fc[0].selectbox("Status", ["(all)"] + statuses, key="find_status")
    fc[1].multiselect("Category", sorted(df["category"].unique()), key=vc.K_FCAT)
    fc[2].multiselect("Challenge", sorted(df["detection_challenge"].unique()), key=vc.K_FCHAL)
    ffile = fc[3].selectbox("Carrier file", ["(all)"] + sorted(df["file"].unique()), key="find_file")

    frows = []
    for _, r in df.iterrows():
        if fstatus != "(all)" and (status_of(r) or "not scanned") != fstatus:
            continue
        if ss[vc.K_FCAT] and r["category"] not in ss[vc.K_FCAT]:
            continue
        if ss[vc.K_FCHAL] and r["detection_challenge"] not in ss[vc.K_FCHAL]:
            continue
        if ffile != "(all)" and r["file"] != ffile:
            continue
        frows.append(r)

    table = pd.DataFrame([{
        "status": DET_BADGE.get(status_of(r), status_of(r)) if status_of(r) else "—",
        "file": r["file"], "category": r["category"], "data_type": r["data_type"],
        "value": str(r["value"])[:40], "challenge": r["detection_challenge"],
        "detector": (item_of(r) or {}).get("detector") or "—",
        "conf": (item_of(r) or {}).get("confidence") or "",
    } for r in frows])
    st.caption(f"{len(frows)} of {len(df)} planted items — click a row to inspect it in context.")
    event = st.dataframe(table, width="stretch", hide_index=True,
                         on_select="rerun", selection_mode="single-row", key="findings_table")
    rows = event.selection.rows if event and event.selection else []
    if not rows:
        st.caption("👆 select a row to see the carrier in context, the talking point, the detector "
                   "result, and to run a detector manually.")
        return

    r = frows[rows[0]]
    st.divider()
    st.markdown(f"### {r['data_type']} in `{r['file']}`  ·  _{r['surface']}_")
    left, right = st.columns([3, 2])
    with left:
        st.markdown("**Carrier in context** — all planted values highlighted")
        pre = carrier_pre(r["file"], df[df["file"] == r["file"]]["value"].tolist())
        if pre:
            st.markdown(pre, unsafe_allow_html=True)
        else:
            st.info(f"(carrier file {r['file']} not found)")
    with right:
        st.markdown(item_card(r), unsafe_allow_html=True)
        it = item_of(r)
        if it:
            line = f"**Detector:** {DET_BADGE.get(it['status'], it['status'])}"
            if it.get("detector"):
                line += f" · `{it['detector']}`"
            if it.get("confidence"):
                line += f" · {it['confidence']}"
            st.markdown(line)
        st.markdown("**Run a detector**")
        if nf is None:
            st.warning("Detector integration not bundled in this build.")
        else:
            _run_detector_ui(nf, r["file"], r["value"], r["data_type"])


# ---- header + copilot-drivable view nav ------------------------------------
st.title(f"🛡️  {company} — DLP demo data")
meta = f"session `{sid}`" if sid else SESSION_DIR.name
if cfg.get("emphasis"):
    meta += f"  ·  emphasis: **{str(cfg['emphasis']).replace('_',' ')}**"
if cfg.get("scale"):
    meta += f"  ·  scale: **{str(cfg['scale']).replace('_',' ')}**"
st.caption(meta)

st.radio("View", vc.VIEWS, key=vc.K_VIEW, horizontal=True,
         format_func=VIEW_ICON.get, label_visibility="collapsed")
st.divider()

RENDERERS = {"Demo overview": render_overview, "Coverage & diversity": render_coverage,
             "Findings": render_findings, "Research & decisions": render_research}
_ = RENDERERS.get(ss[vc.K_VIEW], render_overview)()
