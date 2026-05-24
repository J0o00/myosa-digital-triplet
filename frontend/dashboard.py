
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time, os, base64, json
from ui_styles import GLOBAL_CSS, status_card, metric_card, three_js_model_html, diagnostics_assistant_html, SVG_ACTIVITY, SVG_HEART, SVG_SYNC, SVG_SHIELD, SVG_DATABASE

# ── Page Config ──
st.set_page_config(page_title="Digital Triplet Command Center", page_icon="✦", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── UnicornStudio Background Loader ──
import streamlit.components.v1 as components

components.html("""
<script>
    const parentDoc = window.parent.document;
    
    // Create the background div if it doesn't exist
    if (!parentDoc.getElementById("unicorn-bg")) {
        const bgDiv = parentDoc.createElement("div");
        bgDiv.id = "unicorn-bg";
        bgDiv.setAttribute("data-us-project", "VHdphegF30v2j1bserOH");
        bgDiv.className = "absolute w-full h-full left-0 top-0 -z-10";
        bgDiv.style.position = "fixed";
        bgDiv.style.width = "100vw";
        bgDiv.style.height = "100vh";
        bgDiv.style.left = "0";
        bgDiv.style.top = "0";
        bgDiv.style.zIndex = "-10";
        parentDoc.body.appendChild(bgDiv);
        
        // Load the UnicornStudio script
        const script = parentDoc.createElement("script");
        script.src = "https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.31/dist/unicornStudio.umd.js";
        script.onload = function() {
            if (window.parent.UnicornStudio) {
                window.parent.UnicornStudio.init();
            }
        };
        parentDoc.head.appendChild(script);
    }
</script>
""", height=0, width=0)

# ── Paths ──
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "sensor_data.csv")
MODEL_FILE = os.path.join(os.path.dirname(__file__), "..", "MOTOR", "dc motor 3d model.glb")

# ── Helpers ──
@st.cache_data
def get_model_b64(fp):
    try:
        with open(fp, "rb") as f: return base64.b64encode(f.read()).decode()
    except (FileNotFoundError, IOError, OSError):
        return ""

@st.cache_data(ttl=1)
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            if len(df) > 0: return df
        except (pd.errors.EmptyDataError, pd.errors.ParserError, IOError):
            pass
    return pd.DataFrame()

def pct_dev(a, e):
    return round(abs(a - e) / e * 100, 1) if e != 0 else 0.0

def dev_cls(p):
    if p <= 10: return "dev-ok"
    if p <= 25: return "dev-warn"
    return "dev-crit"

def styled_fig(fig, h=280):
    fig.update_layout(height=h, margin=dict(l=8,r=8,t=32,b=8), paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=10, family="-apple-system"),
        legend=dict(orientation="h", y=1.12, font=dict(size=9, color="#94a3b8")))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255, 255, 255, 0.04)", title="", zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255, 255, 255, 0.04)", title="", zeroline=False)
    return fig

# ── Sidebar ──
with st.sidebar:
    st.markdown("""<div style="text-align:center; padding:20px 0 10px;">
        <div style="font-family:-apple-system, sans-serif; font-size:1.15rem; font-weight:600; color:#ffffff;
        letter-spacing:-0.01em;">Digital Triplet</div>
        <div style="font-family:-apple-system, sans-serif; font-size:0.7rem; color:#94a3b8; letter-spacing:0.05em;
        margin-top:2px; font-weight: 500;">COMMAND CENTER v3.0</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255, 255, 255, 0.08); margin:10px 0;'>", unsafe_allow_html=True)
    nav = st.radio("NAV", ["Dashboard", "Live Stream", "Digital Twin", "AI Diagnostics", "Alerts Center", "Summary Reports", "System Settings"], label_visibility="collapsed")
    st.markdown("<hr style='border-color:rgba(255, 255, 255, 0.08); margin:10px 0;'>", unsafe_allow_html=True)
    st.markdown("""<div style="text-align:center; padding:10px;">
        <div style="font-family:-apple-system, sans-serif; font-size:0.72rem; color:#94a3b8; font-weight: 500; letter-spacing: 0.01em;">
        SYSTEM MONITORING<br><span style="color:#ffffff; font-weight:600;">● ACTIVE</span></div>
    </div>""", unsafe_allow_html=True)

# ── Load Data ──
df = load_data()
if df.empty:
    st.warning("⏳ Awaiting telemetry stream. Start the generator.")
    time.sleep(1); st.rerun()

latest = df.iloc[-1]
status = str(latest.get("status", "normal"))
health = float(latest.get("health_score", 0))
twin_st = str(latest.get("twin_status", "N/A"))
dev_score = float(latest.get("deviation_score", 0))
prev = df.iloc[-2] if len(df) > 1 else latest
plot_df = df.tail(60)

# Fetch new hardware fields safely
voltage = float(latest.get("voltage", 0))
power = float(latest.get("power", 0))
pressure = float(latest.get("pressure", 0))
edge_vib = float(latest.get("edge_vibration", 0))
color_cmd = str(latest.get("color_cmd", "MONITORING"))

# Color command helpers
CMD_STYLES = {
    "GREEN_RUN":  ("🟢", "cmd-green",   "RUN"),
    "RED_STOP":   ("🔴", "cmd-red",     "STOP"),
    "BLUE_MAINT": ("🔵", "cmd-blue",    "MAINT"),
    "MONITORING": ("⚪", "cmd-monitor", "MONITOR"),
}

# Status helpers
s_color = {"normal":"#ffffff","warning":"#fbbf24","critical":"#f87171"}.get(status,"#ffffff")
s_val = {"normal":"val-green","warning":"val-yellow","critical":"val-red"}.get(status,"val-cyan")
s_label = {"normal":"NOMINAL","warning":"WARNING","critical":"CRITICAL"}.get(status,"UNKNOWN")
risk = "LOW" if health >= 80 else ("MEDIUM" if health >= 50 else "HIGH")
risk_cls = "val-green" if health >= 80 else ("val-yellow" if health >= 50 else "val-red")
uptime_h = len(df)

# ── Nav Routing ──
if nav == "Dashboard":
    # ── Header ──
    st.markdown(f"""<div style="display:flex; justify-content:space-between; align-items:center; padding:0 0 8px;">
        <div><span style="font-family:-apple-system, sans-serif; font-size:1.45rem; font-weight:600; color:#ffffff; letter-spacing:-0.015em;">Electric Motor Digital Triplet</span>
        <br><span style="font-family:-apple-system, sans-serif; font-size:0.78rem; color:#94a3b8; font-weight: 400;">
        Real-time Telemetry · Anomaly Detection · System Gatekeeper · Digital Twin Sync</span></div>
        <div style="text-align:right; font-family:-apple-system, sans-serif; font-size:0.72rem; color:#94a3b8; font-weight: 500;">
        LAST UPDATE<br><span style="color:#ffffff; font-family:-apple-system, sans-serif; font-size:0.8rem; font-weight:600;">{latest['timestamp']}</span></div>
    </div>""", unsafe_allow_html=True)
    
    # ── Critical Banner ──
    if status == "critical":
        st.markdown(f'<div style="background:rgba(248,113,113,0.1); border:1px solid rgba(248,113,113,0.3); border-radius:8px; padding:10px 18px; font-family:-apple-system, sans-serif; font-size:0.8rem; font-weight:600; color:#f87171; text-align:center; letter-spacing:0.01em; animation:pulse-red 2s infinite; margin-bottom:12px;">✖ CRITICAL FAULT — SAFE MODE RECOMMENDED</div>', unsafe_allow_html=True)
    elif status == "warning":
        st.markdown(f'<div style="background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.25); border-radius:8px; padding:10px 18px; font-family:-apple-system, sans-serif; font-size:0.8rem; font-weight:600; color:#fbbf24; text-align:center; letter-spacing:0.01em; margin-bottom:12px;">◆ ANOMALY DETECTED — MONITOR CLOSELY</div>', unsafe_allow_html=True)

    # ── Row 1: Status Cards ──
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.markdown(status_card(SVG_ACTIVITY, "Motor Status", s_label, s_val), unsafe_allow_html=True)
    with c2: st.markdown(status_card(SVG_HEART, "Health Score", f"{health:.0f}%", "val-green" if health>=80 else ("val-yellow" if health>=50 else "val-red")), unsafe_allow_html=True)
    with c3:
        sync_stroke = {"Aligned": "#ffffff", "Diverging": "#fbbf24", "Desynced": "#f87171"}.get(twin_st, "#ffffff")
        sync_svg = SVG_SYNC.format(style=f"stroke: {sync_stroke}; filter: drop-shadow(0 0 4px {sync_stroke}44);")
        st.markdown(status_card(sync_svg, "Twin Sync", twin_st, "val-green" if twin_st=="Aligned" else ("val-yellow" if twin_st=="Diverging" else "val-red")), unsafe_allow_html=True)

    with c4: st.markdown(status_card(SVG_SHIELD, "Predicted Risk", risk, risk_cls), unsafe_allow_html=True)
    with c5:
        cmd_icon, cmd_cls, cmd_short = CMD_STYLES.get(color_cmd, ("⚪", "cmd-monitor", "???"))
        st.markdown(status_card(cmd_icon, "MYOSA Cmd", cmd_short, "val-green" if color_cmd=="GREEN_RUN" else ("val-red" if color_cmd=="RED_STOP" else "val-cyan")), unsafe_allow_html=True)
    with c6: st.markdown(status_card(SVG_DATABASE, "Data Points", str(uptime_h), "val-cyan"), unsafe_allow_html=True)
    
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── Main Tabs ──
    st_overview, st_telemetry, st_ai, st_sync = st.tabs([
        "Overview", 
        "Telemetry", 
        "Gatekeeper", 
        "Synchronization"
    ])

    with st_overview:
        col_3d, col_ai = st.columns([1.6, 1])
        with col_3d:
            st.markdown('<div class="section-hdr">Digital Twin Visualization</div>', unsafe_allow_html=True)
            import math
            clean_telemetry = {k: ("None" if isinstance(v, float) and math.isnan(v) else v) for k, v in dict(latest).items()}
            telemetry_json = json.dumps(clean_telemetry).replace("'", "&#39;")
            st.markdown(f'<div id="live-telemetry-data" style="display:none;">{telemetry_json}</div>', unsafe_allow_html=True)
            st.iframe(three_js_model_html("app/static/dc_motor.glb", s_color), height=500)
            st.markdown(f'<div style="text-align:center;margin-top:6px"><span class="pill pill-{status}">{s_label}</span></div>', unsafe_allow_html=True)
            
        with col_ai:
            st.markdown('<div class="section-hdr">Predictive Summary</div>', unsafe_allow_html=True)
            conf = max(65, min(99, int(health * 0.9 + 10)))
            etf = "72+ hrs" if health >= 80 else ("24-48 hrs" if health >= 50 else "< 12 hrs")
            fault_type = str(latest.get("fault_type", "none"))
            deg_src = fault_type.replace("_"," ").title() if fault_type != "none" else "None Detected"
            deg_rate = f"{dev_score:.1f}%"
            
            badge_cls = {"normal":"badge-normal","warning":"badge-warning","critical":"badge-critical"}.get(status,"badge-normal")
            badge_txt = {"normal":"SYSTEMS NOMINAL","warning":"PREDICTED DEGRADATION","critical":"CRITICAL FAILURE"}.get(status,"UNKNOWN")
            st.markdown(f'<div class="ai-box" style="text-align:center"><span class="ai-badge {badge_cls}">{badge_txt}</span></div>', unsafe_allow_html=True)
            
            st.markdown(f"""<div class="ai-box">
                <table style="width:100%; font-family:-apple-system, sans-serif; font-size:0.85rem; color:#94a3b8;">
                <tr><td style="padding:5px 0; color:#94a3b8; font-weight:400;">Diagnostic Confidence</td><td style="text-align:right; color:#ffffff; font-family:'JetBrains Mono'; font-weight:600;">{conf}%</td></tr>
                <tr><td style="padding:5px 0; color:#94a3b8; font-weight:400;">Est. Time to Failure</td><td style="text-align:right; color:#ffffff; font-family:'JetBrains Mono'; font-weight:600;">{etf}</td></tr>
                <tr><td style="padding:5px 0; color:#94a3b8; font-weight:400;">Degradation Source</td><td style="text-align:right; color:#fbbf24; font-family:'JetBrains Mono'; font-weight:600;">{deg_src}</td></tr>
                <tr><td style="padding:5px 0; color:#94a3b8; font-weight:400;">Degradation Rate</td><td style="text-align:right; color:#fbbf24; font-family:'JetBrains Mono'; font-weight:600;">{deg_rate}</td></tr>
                </table>
            </div>""", unsafe_allow_html=True)
            
            if fault_type != "none":
                sev = str(latest.get("fault_severity","Unknown"))
                fc = "#f87171" if sev == "Severe" else "#fbbf24"
                st.markdown(f"""<div class="ai-box" style="border-left:3px solid {fc};">
                    <b style="color:{fc}; font-size:0.85rem; font-family:-apple-system;">◆ ACTIVE FAULT DETECTED</b><br>
                    <span style="color:#94a3b8; font-size:0.82rem; font-family:-apple-system;">Type: <b style="color:#f9fafc">{deg_src}</b> · Severity: <b style="color:{fc}">{sev}</b></span>
                </div>""", unsafe_allow_html=True)

            ai_action = latest.get("ai_action", "None")
            if pd.notna(ai_action) and str(ai_action) not in ("nan","None",""):
                st.markdown(f"""<div class="ai-box" style="border-left:3px solid #ffffff;">
                    <b style="color:#ffffff; font-size:0.85rem; font-family:-apple-system;">✦ SYSTEM AUTONOMOUS MITIGATION</b><br>
                    <span style="color:#94a3b8; font-size:0.82rem; font-family:-apple-system;">{ai_action}</span>
                </div>""", unsafe_allow_html=True)

    with st_telemetry:
        st.markdown('<div class="section-hdr">Live Metrics</div>', unsafe_allow_html=True)
        mc1,mc2,mc3,mc4 = st.columns(4)
        telem1 = [
            (mc1, "RPM", latest['rpm'], prev['rpm'], "", "#ffffff", False),
            (mc2, "Temperature", latest['temperature'], prev['temperature'], "°C", "#ffffff", True),
            (mc3, "Vibration", latest['vibration'], prev['vibration'], "mm/s", "#ffffff", True),
            (mc4, "Current", latest['current'], prev['current'], "A", "#ffffff", True),
        ]
        for col, lbl, val, pval, unit, clr, inv in telem1:
            with col:
                st.markdown(metric_card(lbl, f"{val:.1f}", val - pval, unit, clr, inv), unsafe_allow_html=True)
                
        mc5,mc6,mc7,mc8 = st.columns(4)
        telem2 = [
            (mc5, "Voltage", voltage, float(prev.get('voltage', voltage)), "V", "#ffffff", False),
            (mc6, "Power", power, float(prev.get('power', power)), "W", "#ffffff", True),
            (mc7, "Pressure", pressure, float(prev.get('pressure', pressure)), "hPa", "#ffffff", False),
            (mc8, "Health Score", health, float(prev.get('health_score', health)), "%", "#ffffff", False),
        ]
        for col, lbl, val, pval, unit, clr, inv in telem2:
            with col:
                st.markdown(metric_card(lbl, f"{val:.1f}", val - pval, unit, clr, inv), unsafe_allow_html=True)
                
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-hdr">Telemetry High-Resolution Trends</div>', unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        def hex_to_rgba(h, alpha=0.05):
            h = h.lstrip('#')
            return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{alpha})"
        
        def trend_chart(df, ac, ec, title, clr):
            f = go.Figure()
            if ec in df.columns:
                f.add_trace(go.Scatter(x=df["timestamp"], y=df[ec], name="Baseline", line=dict(color=clr, width=1.5, dash="dot"), opacity=0.4))
            f.add_trace(go.Scatter(x=df["timestamp"], y=df[ac], name="Actual", line=dict(color=clr, width=2),
                fill='tozeroy', fillcolor=hex_to_rgba(clr, 0.05)))
            f.update_layout(title=dict(text=title, font=dict(size=12, color='#ffffff', family='-apple-system', weight='bold')))
            return styled_fig(f, 240)
            
        with t1:
            st.plotly_chart(trend_chart(plot_df,"rpm","expected_rpm","RPM","#ffffff"), key="trend_rpm", use_container_width=True)
            st.plotly_chart(trend_chart(plot_df,"vibration","expected_vibration","Vibration","#fbbf24"), key="trend_vib", use_container_width=True)
        with t2:
            st.plotly_chart(trend_chart(plot_df,"temperature","expected_temperature","Temperature","#ffffff"), key="trend_temp", use_container_width=True)
            st.plotly_chart(trend_chart(plot_df,"current","expected_current","Current","#94a3b8"), key="trend_curr", use_container_width=True)
        with t3:
            if "voltage" in plot_df.columns:
                st.plotly_chart(trend_chart(plot_df,"voltage","expected_voltage","Voltage","#ffffff"), key="trend_volt", use_container_width=True)
            if "power" in plot_df.columns:
                st.plotly_chart(trend_chart(plot_df,"power","expected_power","Power","#94a3b8"), key="trend_power", use_container_width=True)

    with st_ai:
        st.markdown('<div class="section-hdr">AI Gatekeeper & Diagnostic Reports</div>', unsafe_allow_html=True)
        col_log, col_diag = st.columns([1.5, 1])
        with col_log:
            st.markdown('<div class="glass-panel" style="padding:20px;"><div style="font-family:-apple-system, sans-serif; font-size:0.85rem; font-weight:600; color:#ffffff; letter-spacing:0.01em; margin-bottom:10px;">DEVICE DIAGNOSTIC LOG</div>', unsafe_allow_html=True)
            log_lines = []
            for _, row in df.tail(15).iloc[::-1].iterrows():
                ts = str(row.get("timestamp",""))
                st_r = str(row.get("status","normal"))
                cls = {"warning":"log-warn","critical":"log-crit"}.get(st_r,"log-ok")
                ft = str(row.get("fault_type","none"))
                reason = str(row.get("anomaly_reason","")) if pd.notna(row.get("anomaly_reason")) else ""
                msg = f"Fault: {ft.replace('_',' ').title()}" if ft != "none" else (reason if reason and reason not in ("nan","") else "Systems nominal")
                log_lines.append(f'<span class="log-ts">{ts}</span> <span class="{cls}">[{st_r.upper():^8s}]</span> {msg}')
            st.markdown(f'<div class="alert-log">{"<br>".join(log_lines)}</div></div>', unsafe_allow_html=True)
            
        with col_diag:
            st.markdown(f"""<div class="glass-panel">
                <div style="font-family:-apple-system, sans-serif; font-size:0.85rem; font-weight:600; color:#ffffff; letter-spacing:0.01em; margin-bottom:12px;">DECISION SUMMARY</div>
                <table style="width:100%; font-family:-apple-system, sans-serif; font-size:0.85rem; border-collapse:collapse; color:#94a3b8;">
                <tr><td style="padding:8px 0; color:#94a3b8; font-weight:400; border-bottom:1px solid rgba(255, 255, 255, 0.08);">Total Telemetry Reads</td><td style="text-align:right; color:#ffffff; font-family:\'JetBrains Mono\', monospace; font-weight:600; border-bottom:1px solid rgba(255, 255, 255, 0.08);">{len(df)}</td></tr>
                <tr><td style="padding:8px 0; color:#94a3b8; font-weight:400; border-bottom:1px solid rgba(255, 255, 255, 0.08);">Active Fault Flag</td><td style="text-align:right; color:#f87171; font-family:\'JetBrains Mono\', monospace; font-weight:600; border-bottom:1px solid rgba(255, 255, 255, 0.08);">{latest.get("fault_type", "none").replace("_"," ").title()}</td></tr>
                <tr><td style="padding:8px 0; color:#94a3b8; font-weight:400; border-bottom:1px solid rgba(255, 255, 255, 0.08);">Anomaly Counter (Recent)</td><td style="text-align:right; color:#fbbf24; font-family:\'JetBrains Mono\', monospace; font-weight:600; border-bottom:1px solid rgba(255, 255, 255, 0.08);">{df.tail(30)["status"].isin(["warning","critical"]).sum()}</td></tr>
                <tr><td style="padding:8px 0; color:#94a3b8; font-weight:400; border-bottom:1px solid rgba(255, 255, 255, 0.08);">Deviation Level</td><td style="text-align:right; color:#ffffff; font-family:\'JetBrains Mono\', monospace; font-weight:600; border-bottom:1px solid rgba(255, 255, 255, 0.08);">{dev_score:.1f}%</td></tr>
                </table>
            </div>""", unsafe_allow_html=True)

    with st_sync:
        st.markdown('<div class="section-hdr">Synchronization & Deviation metrics</div>', unsafe_allow_html=True)
        col_sync_lhs, col_sync_rhs = st.columns([1, 2.5])
        with col_sync_lhs:
            sync_cls = {"Aligned":"sync-aligned","Diverging":"sync-diverge","Desynced":"sync-desynced"}.get(twin_st,"")
            st.markdown(f"""<div class="glass-panel-sm" style="margin-bottom:12px; text-align:center;">
                <div style="font-size:1.6rem; font-weight:600;" class="{sync_cls}">{twin_st}</div>
                <div style="color:#94a3b8; font-size:0.8rem; margin-top:4px; font-weight:400;">Deviation: <b style="color:#ffffff; font-family:'JetBrains Mono', sans-serif;">{dev_score}%</b></div>
            </div>""", unsafe_allow_html=True)
            
            params = [("RPM Deviation","rpm","expected_rpm"),("Temp Deviation","temperature","expected_temperature"),
                      ("Vib Deviation","vibration","expected_vibration"),("Current Deviation","current","expected_current"),
                      ("Volt Deviation","voltage","expected_voltage"),("Power Deviation","power","expected_power"),
                      ("Pres Deviation","pressure","expected_pressure")]
            for lbl, ak, ek in params:
                av = float(latest.get(ak, 0)); ev = float(latest.get(ek, av)) if ek in latest.index else av
                p = pct_dev(av, ev); c = dev_cls(p)
                st.markdown(f"""<div class="dev-card {c}"><b style="color:#f1f5f9; font-size:0.85rem; font-family:-apple-system;">{lbl}</b>
                    <span style="float:right; font-family:'JetBrains Mono'; font-size:0.78rem; color:#ffffff; font-weight:600;">{av:.1f} / {ev:.1f} <span style="color:#94a3b8; font-family:-apple-system; font-weight:400;">({p}%)</span></span></div>""", unsafe_allow_html=True)
                    
        with col_sync_rhs:
            COLORS = {"RPM":"#ffffff","Temperature":"#94a3b8","Vibration":"#fbbf24","Current":"#475569",
                      "Voltage":"#ffffff","Power":"#94a3b8"}
            sp = [("RPM","rpm","expected_rpm"),("Temperature","temperature","expected_temperature"),
                  ("Vibration","vibration","expected_vibration"),("Current","current","expected_current"),
                  ("Voltage","voltage","expected_voltage"),("Power","power","expected_power")]
            fig = make_subplots(rows=3, cols=2, subplot_titles=[s[0] for s in sp], vertical_spacing=0.12, horizontal_spacing=0.1)
            pos = [(1,1),(1,2),(2,1),(2,2),(3,1),(3,2)]
            for (t,ac,ec),(r,c2) in zip(sp, pos):
                clr = COLORS[t]; sl = (r==1 and c2==1)
                if ec in plot_df.columns:
                    fig.add_trace(go.Scatter(x=plot_df["timestamp"], y=plot_df[ec], name="Baseline",
                        line=dict(color=clr, width=1, dash="dot"), opacity=0.4, showlegend=sl, legendgroup="b"), row=r, col=c2)
                if ac in plot_df.columns:
                    fig.add_trace(go.Scatter(x=plot_df["timestamp"], y=plot_df[ac], name="Actual",
                        line=dict(color=clr, width=2), showlegend=sl, legendgroup="a"), row=r, col=c2)
            fig = styled_fig(fig, 520)
            fig.update_xaxes(showticklabels=False)
            for ann in fig['layout']['annotations']: ann['font'] = dict(size=12, color='#ffffff', family='-apple-system', weight='bold')
            st.plotly_chart(fig, use_container_width=True, key="sync_charts")

elif nav == "Live Stream":
    st.markdown('<div class="section-hdr">Real-time Telemetry Data Stream</div>', unsafe_allow_html=True)
    st.markdown("""<div class="glass-panel">
        <p style="margin-bottom:15px; font-family:-apple-system; color:#94a3b8;">Viewing high-refresh raw telemetry data points collected from the electric motor sensors.</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("### Telemetry Data Logger")
    st.dataframe(df.tail(100).iloc[::-1], use_container_width=True)

elif nav == "Digital Twin":
    st.markdown('<div class="section-hdr">Immersive Digital Twin Viewer</div>', unsafe_allow_html=True)
    st.markdown(f'<div id="live-temp-data" style="display:none;">{latest.get("temperature", 50)}</div>', unsafe_allow_html=True)
    st.iframe(three_js_model_html("app/static/dc_motor.glb", s_color), height=550)
    st.markdown(f'<div style="text-align:center;margin-top:10px;"><span class="pill pill-{status}">Active Model Serving: dc_motor.glb ({s_label})</span></div>', unsafe_allow_html=True)

elif nav == "AI Diagnostics":
    st.markdown('<div class="section-hdr">AI Diagnostics & Predictive Modeling</div>', unsafe_allow_html=True)
    col_lh, col_rh = st.columns(2)
    with col_lh:
        st.markdown(f"""<div class="glass-panel">
            <h3 style="margin-top:0; color:#ffffff;">Diagnostic Inference Engine</h3>
            <p style="font-family:-apple-system; color:#94a3b8;">Predictive anomaly engine analyzing multi-axis vibration, magnetic coil thermal expansion, and brush load variations.</p>
            <hr>
            <div style="font-family:-apple-system; color:#f3f4f6; line-height:1.8;">
                <b>Health State:</b> {health:.1f}%<br>
                <b>Risk Score:</b> {dev_score:.1f}%<br>
                <b>Action Log:</b> {latest.get("ai_action", "No active mitigation triggered.")}
            </div>
        </div>""", unsafe_allow_html=True)
    with col_rh:
        st.markdown(f"""<div class="glass-panel">
            <h3 style="margin-top:0; color:#ffffff;">Autonomous Mitigation Strategy</h3>
            <p style="font-family:-apple-system; color:#94a3b8;">Active closed-loop controller responds to anomaly detection by adjusting PWM frequency thresholds dynamically to prevent damage.</p>
            <hr>
            <div style="font-family:-apple-system; color:#f3f4f6; line-height:1.8;">
                <b>Controller Action:</b> Active Duty Cycle Regulation<br>
                <b>Thermal Buffer:</b> Safe Mode Threshold at 80°C
            </div>
        </div>""", unsafe_allow_html=True)

elif nav == "Alerts Center":
    st.markdown('<div class="section-hdr">System Alerts & Diagnostics</div>', unsafe_allow_html=True)
    anom_df = df[df["status"].isin(["warning", "critical"])].tail(50).iloc[::-1]
    if len(anom_df) > 0:
        st.dataframe(anom_df, use_container_width=True)
    else:
        st.success("✓ No anomalies detected in recent telemetry.")

elif nav == "Summary Reports":
    st.markdown('<div class="section-hdr">System Diagnostics Summary Reports</div>', unsafe_allow_html=True)
    min_max_df = pd.DataFrame({
        "Metric": ["RPM", "Temperature", "Vibration", "Current", "Voltage", "Power", "Pressure"],
        "Min Value": [df["rpm"].min(), df["temperature"].min(), df["vibration"].min(), df["current"].min(), df.get("voltage", pd.Series([0])).min(), df.get("power", pd.Series([0])).min(), df.get("pressure", pd.Series([0])).min()],
        "Max Value": [df["rpm"].max(), df["temperature"].max(), df["vibration"].max(), df["current"].max(), df.get("voltage", pd.Series([0])).max(), df.get("power", pd.Series([0])).max(), df.get("pressure", pd.Series([0])).max()],
        "Average": [df["rpm"].mean(), df["temperature"].mean(), df["vibration"].mean(), df["current"].mean(), df.get("voltage", pd.Series([0])).mean(), df.get("power", pd.Series([0])).mean(), df.get("pressure", pd.Series([0])).mean()],
    })
    st.table(min_max_df)

elif nav == "System Settings":
    st.markdown('<div class="section-hdr">Telemetry Configuration & Settings</div>', unsafe_allow_html=True)
    st.markdown("""<div class="glass-panel">
        <h3 style="margin-top:0; color:#ffffff;">Motor Simulation Control Panel</h3>
        <p style="font-family:-apple-system; color:#94a3b8;">Trigger anomalies or adjust diagnostic thresholds for testing the Digital Triplet Gatekeeper and autonomous mitigation loop.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Inject Telemetry Data for Trinity AI ──
try:
    import math
    telemetry_dict = {}
    for k, v in latest.items():
        if pd.isna(v) or v is None:
            telemetry_dict[str(k)] = 0.0
        elif isinstance(v, (int, float)):
            telemetry_dict[str(k)] = float(v)
        else:
            telemetry_dict[str(k)] = str(v)
    st.markdown(f"<div id='live-telemetry-data' style='display:none;'>{json.dumps(telemetry_dict)}</div>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Telemetry injection failed: {e}")

# ── TRINITY AI CORE (Floating Overlay) ──
import streamlit.components.v1 as components
components.html(diagnostics_assistant_html(), height=450)

# ── Auto-refresh ──
time.sleep(4)
st.rerun()
