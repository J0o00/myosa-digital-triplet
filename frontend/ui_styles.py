"""
Minimalist iOS-Style Bento Dashboard — CSS & HTML Templates
Designed with SF Pro typography, high-gloss glassmorphism, and dynamic Spline background integration.
"""

GLOBAL_CSS = """
<style>
/* ── GLOBAL RESET (IPHONE SF PRO TYPOGRAPHY) ── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "SF Pro", "SFNS Display", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    color: #f3f4f6 !important;
}
html, body {
    background-color: #05070a !important; /* ultra dark midnight base */
    background-attachment: fixed !important;
}
.stApp {
    background: transparent !important;
    background-color: transparent !important;
}

/* ── UNICORNSTUDIO BACKGROUND (Tailwind-class support) ── */
.absolute { position: fixed !important; }
.top-0    { top: 0 !important; }
.left-0   { left: 0 !important; }
.w-full   { width: 100vw !important; }
.h-full   { height: 100vh !important; }
.-z-10    { z-index: -10 !important; }
/* UnicornStudio injects a canvas/iframe inside the div */
[data-us-project] > * {
    pointer-events: none !important;
}

/* ── iOS MINIMALIST SPACING & PADDING ── */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    max-width: 95% !important;
}
div[data-testid="column"] {
    padding: 0 10px !important;
}
h1, h2, h3 { 
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro", sans-serif !important; 
    color: #ffffff !important; 
    font-weight: 600 !important;
    letter-spacing: -0.015em;
    text-shadow: none !important;
}
.stMarkdown p { 
    color: #a0aec0; 
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
    line-height: 1.6;
}

/* ── HIDE DEFAULT STREAMLIT ── */
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDecoration"] { display:none; }
div[data-testid="stToolbar"] { display:none; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.12); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.25); }

/* ── SIDEBAR OVERHAUL (iOS BLUR COLUMN) ── */
section[data-testid="stSidebar"] {
    background: rgba(10, 12, 16, 0.45) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(30px) !important;
    -webkit-backdrop-filter: blur(30px) !important;
}
section[data-testid="stSidebar"] .stRadio > label { display: none; }
section[data-testid="stSidebar"] .stRadio > div {
    display: flex; flex-direction: column; gap: 6px !important;
    padding: 10px 0 !important;
}
section[data-testid="stSidebar"] .stRadio > div > label {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
    font-size: 0.85rem !important; font-weight: 500 !important;
    color: #a0aec0 !important; padding: 10px 18px !important;
    border-radius: 8px !important; cursor: pointer !important;
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    margin-bottom: 0px !important;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(255, 255, 255, 0.07) !important; 
    color: #ffffff !important; 
    border-color: rgba(255, 255, 255, 0.15) !important;
    transform: translateY(-1px) !important;
}
section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
section[data-testid="stSidebar"] .stRadio > div [aria-checked="true"] {
    background: rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important; 
    border-color: rgba(255, 255, 255, 0.25) !important;
    border-top-color: rgba(255, 255, 255, 0.35) !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    transform: translateY(-1px) !important;
}

/* ── HIGH-GLOSS BENTO GLASS PANELS ── */
.glass-panel {
    background: linear-gradient(135deg, rgba(20, 24, 33, 0.4) 0%, rgba(10, 12, 16, 0.55) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 8px !important;
    padding: 24px !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease !important;
    margin-bottom: 16px !important;
}
.glass-panel:hover {
    border-color: rgba(255, 255, 255, 0.18) !important;
    border-top-color: rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45), inset 0 1px 2px rgba(255, 255, 255, 0.1) !important;
    transform: translateY(-1.5px) !important;
}
.glass-panel-sm {
    background: linear-gradient(135deg, rgba(20, 24, 33, 0.4) 0%, rgba(10, 12, 16, 0.55) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 8px !important;
    padding: 16px 20px !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
    transition: border-color 0.3s ease, transform 0.3s ease !important;
}
.glass-panel-sm:hover {
    border-color: rgba(255, 255, 255, 0.15) !important;
    transform: translateY(-1px) !important;
}

/* ── STATUS CARD ── */
.status-card {
    background: linear-gradient(135deg, rgba(20, 24, 33, 0.4) 0%, rgba(10, 12, 16, 0.55) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 8px !important;
    padding: 20px 22px !important;
    text-align: center !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
    transition: border-color 0.3s, box-shadow 0.3s, transform 0.3s !important;
}
.status-card:hover {
    border-color: rgba(255, 255, 255, 0.18) !important;
    border-top-color: rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 12px 32px rgba(255, 255, 255, 0.08), inset 0 1px 2px rgba(255, 255, 255, 0.1) !important;
    transform: translateY(-2px) !important;
}
.status-card .card-icon { 
    font-size: 1.6rem; 
    margin-bottom: 8px; 
    display: flex;
    justify-content: center;
    align-items: center;
    height: 38px;
}
.status-card .card-icon .card-svg {
    width: 24px;
    height: 24px;
    stroke: rgba(255, 255, 255, 0.85);
    filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.2));
}
.status-card .card-label {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; font-size: 0.76rem; font-weight: 500;
    color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.status-card .card-value {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif; font-size: 1.2rem; font-weight: 600;
    margin: 4px 0;
}
.val-green  { color: #34d399; }
.val-cyan   { color: #ffffff; }
.val-yellow { color: #fbbf24; }
.val-red    { color: #f87171; }

/* ── METRIC CARD ── */
.metric-card {
    background: linear-gradient(135deg, rgba(20, 24, 33, 0.4) 0%, rgba(10, 12, 16, 0.55) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 8px !important;
    padding: 20px 18px !important;
    text-align: center !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
    transition: border-color 0.3s, box-shadow 0.3s, transform 0.3s !important;
}
.metric-card:hover { 
    border-color: rgba(255, 255, 255, 0.18) !important; 
    border-top-color: rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 12px 32px rgba(255, 255, 255, 0.08), inset 0 1px 2px rgba(255, 255, 255, 0.1) !important; 
    transform: translateY(-2px) !important;
}
.metric-label {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; font-size: 0.76rem; font-weight: 500;
    color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em;
}
.metric-value {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif; font-size: 1.35rem; font-weight: 600;
    color: #ffffff; margin: 10px 0 4px;
}
.metric-delta { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; font-weight: 500; font-size: 0.78rem; margin-top: 4px; }
.delta-up   { color: #34d399; }
.delta-down { color: #f87171; }
.delta-neutral { color: #94a3b8; }

/* ── DEVIATION CARD ── */
.dev-card {
    background: rgba(255, 255, 255, 0.02); border-radius: 8px;
    padding: 14px 18px; margin-bottom: 10px;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-left: 3px solid rgba(255, 255, 255, 0.2);
    transition: all 0.2s;
}
.dev-card:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.1);
}
.dev-ok   { border-left-color: #34d399; }
.dev-warn { border-left-color: #fbbf24; }
.dev-crit { border-left-color: #f87171; }

/* ── MYOSA COLOR COMMAND BADGES ── */
.cmd-badge {
    display: inline-block; padding: 6px 18px; border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; text-align: center;
}
.cmd-green   { background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.3); color: #34d399; }
.cmd-red     { background: rgba(248, 113, 113, 0.1); border: 1px solid rgba(248, 113, 113, 0.3); color: #f87171; animation: pulse-red 2s infinite; }
.cmd-blue    { background: rgba(96, 165, 250, 0.1); border: 1px solid rgba(96, 165, 250, 0.3); color: #60a5fa; }
.cmd-monitor { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #ffffff; }

/* ── AI GATEKEEPER ── */
.ai-box {
    background: linear-gradient(135deg, rgba(20, 24, 33, 0.45) 0%, rgba(10, 12, 16, 0.6) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 8px !important;
    padding: 20px !important;
    margin-bottom: 16px !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25) !important;
}
.ai-badge {
    display: inline-block; padding: 6px 18px; border-radius: 6px;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; font-size: 0.78rem; font-weight: 600;
    letter-spacing: 0.02em; text-transform: uppercase;
}
.badge-normal  { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); color: #ffffff; }
.badge-warning { background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.3); color: #fbbf24; }
.badge-critical { background: rgba(248, 113, 113, 0.1); border: 1px solid rgba(248, 113, 113, 0.3); color: #f87171;
    animation: pulse-red 2s infinite;
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 5px rgba(248, 113, 113, 0.2); border-color: rgba(248, 113, 113, 0.3); }
    50% { box-shadow: 0 0 20px rgba(248, 113, 113, 0.5); border-color: rgba(248, 113, 113, 0.8); }
}

/* ── iOS GLASS TABS OVERHAUL ── */
div[data-testid="stTabBar"], [data-testid="stTabBar"] {
    background: rgba(10, 12, 16, 0.45) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 8px !important;
    padding: 5px !important;
    gap: 4px !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
    margin: 20px 0 24px 0 !important;
    display: flex !important;
    width: max-content !important;
    max-width: 100% !important;
}
div[data-testid="stTabBar"]::after {
    display: none !important;
}
div[data-testid="stTabBar"] button, 
div[data-testid="stTabBar"] div[role="tab"],
div[data-testid="stTabBar"] button[role="tab"],
button[data-baseweb="tab"] {
    background: transparent !important;
    color: #94a3b8 !important;
    border: none !important;
    padding: 6px 20px !important;
    height: 32px !important;
    border-radius: 6px !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    margin: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
}
div[data-testid="stTabBar"] button:hover, 
button[data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #ffffff !important;
}
div[data-testid="stTabBar"] button[aria-selected="true"],
div[data-testid="stTabBar"] button[data-baseweb="tab"][aria-selected="true"],
button[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    font-weight: 600 !important;
}

/* ── STREAMLIT DEFAULT BUTTON OVERRIDES ── */
.stButton > button {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
    font-weight: 500 !important;
}
.stButton > button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
}

/* ── ALERT LOG ── */
.alert-log {
    background: rgba(0, 0, 0, 0.35); border: 1px solid rgba(255, 255, 255, 0.04) !important;
    border-radius: 8px; padding: 14px 18px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
    max-height: 220px; overflow-y: auto; color: #a0aec0;
    line-height: 1.75;
}
.alert-log .log-warn { color: #fbbf24; font-weight: 500; }
.alert-log .log-crit { color: #f87171; font-weight: 500; }
.alert-log .log-ok   { color: #34d399; }
.alert-log .log-ts   { color: #8892b0; }

/* ── MINIMALISTIC SECTION HEADER ── */
.section-hdr {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important; font-size: 0.88rem; font-weight: 600;
    color: #e2e8f0; letter-spacing: 0.01em;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 6px; margin-bottom: 16px;
}
.section-hdr::before { content: ''; }

/* ── PILL ── */
.pill {
    display: inline-block; padding: 4px 14px;
    border-radius: 9999px; font-weight: 600; font-size: 0.76rem;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif; letter-spacing: 0.01em;
}
.pill-normal   { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1); color: #ffffff; }
.pill-warning  { background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.25); color: #fbbf24; }
.pill-critical { background: rgba(248, 113, 113, 0.1); border: 1px solid rgba(248, 113, 113, 0.25); color: #f87171; }

/* ── SYNC BADGE ── */
.sync-aligned  { color:#34d399; font-weight:600; }
.sync-diverge  { color:#fbbf24; font-weight:600; }
.sync-desynced { color:#f87171; font-weight:600; }

/* ── OVERRIDE STREAMLIT METRICS ── */
div[data-testid="stMetric"] {
    background: transparent !important; border: none !important;
}
div[data-testid="stMetric"] label { color: #94a3b8 !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important; font-weight: 600 !important; color: #ffffff !important;
}

/* ── DIVIDER ── */
hr { border-color: rgba(255, 255, 255, 0.08) !important; }
</style>
"""

# ── Vector SVG Stroke Icons ──
SVG_ACTIVITY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="card-svg"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>"""

SVG_HEART = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="card-svg"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>"""

SVG_SYNC = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="card-svg" style="{style}"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"></path></svg>"""

SVG_SHIELD = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="card-svg"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>"""

SVG_DATABASE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="card-svg"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"></path></svg>"""


def status_card(icon: str, label: str, value: str, val_class: str = "val-cyan") -> str:
    return f"""
    <div class="status-card">
        <div class="card-icon">{icon}</div>
        <div class="card-label">{label}</div>
        <div class="card-value {val_class}">{value}</div>
    </div>"""


def metric_card(label: str, value: str, delta: float, unit: str = "",
                color: str = "#ffffff", inverse: bool = False) -> str:
    if delta > 0:
        d_cls = "delta-down" if inverse else "delta-up"
        d_sym = "▲"
    elif delta < 0:
        d_cls = "delta-up" if inverse else "delta-down"
        d_sym = "▼"
    else:
        d_cls = "delta-neutral"
        d_sym = "–"
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color};">{value}<span style="font-size:0.75rem; color:#94a3b8;"> {unit}</span></div>
        <div class="metric-delta {d_cls}">{d_sym} {abs(delta):.2f}</div>
    </div>"""


def three_js_model_html(model_url: str, status_color: str) -> str:
    """Generate a Digital Twin visualization HTML block.

    Uses Three.js with an iterative GLTF traversal to prevent call stack issues.
    Safely clones and updates materials for dynamic temperature response.
    
    model_url: Served URL path to the GLB model file.
    """
    return f"""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{background:transparent;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text",sans-serif}}
    #container{{
      position:relative;width:100%;height:480px;
      background:radial-gradient(circle at center, rgba(13, 17, 23, 0.4) 0%, rgba(5, 7, 10, 0.7) 90%);
      border-radius:8px;overflow:hidden;
      border:1px solid rgba(255, 255, 255, 0.08);
      box-shadow:0 8px 32px rgba(0,0,0,0.3);
    }}
    #canvas-container{{width:100%;height:100%;display:block}}
    
    /* Subtly animated glow rings */
    .holo-ring{{
      position:absolute;bottom:60px;left:50%;transform:translateX(-50%);
      width:280px;height:60px;
      border:2px solid {status_color}22;
      border-radius:50%;opacity:0.35;
      box-shadow:0 0 20px {status_color}08,inset 0 0 20px {status_color}08;
      animation:ring-pulse 4s ease-in-out infinite;pointer-events:none;
    }}
    .holo-ring-2{{
      position:absolute;bottom:50px;left:50%;transform:translateX(-50%);
      width:340px;height:70px;
      border:1px solid {status_color}08;
      border-radius:50%;opacity:0.2;
      animation:ring-pulse 4s ease-in-out infinite .8s;pointer-events:none;
    }}
    @keyframes ring-pulse{{
      0%,100%{{opacity:.15;transform:translateX(-50%) scale(1)}}
      50%{{opacity:.4;transform:translateX(-50%) scale(1.03)}}
    }}
    
    .status-glow{{
      position:absolute;top:14px;right:16px;
      font-size:.72rem;font-weight:600;
      color:{status_color};letter-spacing:.08em;
      pointer-events:none;
    }}
    #temp-display{{
      position:absolute;bottom:14px;right:16px;
      font-family:monospace;font-size:1.3rem;font-weight:bold;
      color:#fff;text-shadow:0 0 10px rgba(255,255,255,.5);pointer-events:none;
    }}
    #temp-label{{
      position:absolute;bottom:14px;left:16px;
      font-size:.72rem;font-weight:600;
      color:#9ca3af;letter-spacing:.1em;pointer-events:none;
    }}
    </style>
    <script type="importmap">
      {{
        "imports": {{
          "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
          "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
        }}
      }}
    </script>
    </head>
    <body>
    <div id="container">
      <div id="canvas-container"></div>
      <div class="holo-ring"></div>
      <div class="holo-ring-2"></div>
      <div class="status-glow">● LIVE FEED</div>
      <div id="temp-label">MOTOR TEMP</div>
      <div id="temp-display">-- °C</div>
    </div>
    
    <script type="module">
    import * as THREE from 'three';
    import {{OrbitControls}} from 'three/addons/controls/OrbitControls.js';
    import {{GLTFLoader}} from 'three/addons/loaders/GLTFLoader.js';
    
    console.log('[DT] Three.js Digital Twin initializing…');
    
    /* ── Scene Setup ── */
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(2.5, 2.5, 3.5);
    
    const renderer = new THREE.WebGLRenderer({{antialias:true, alpha:true}});
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.3;
    container.appendChild(renderer.domElement);
    
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 1.5;
    
    /* ── Lights ── */
    scene.add(new THREE.AmbientLight(0xffffff, 0.7));
    const dirLight = new THREE.DirectionalLight(0xffffff, 2.0);
    dirLight.position.set(5, 10, 5);
    scene.add(dirLight);
    
    const modelUrl = '{model_url}';
    
    /* ── Load Model ── */
    const motorMaterials = [];
    const loader = new GLTFLoader();
    
    loader.load(modelUrl, function(gltf) {{
        console.log('[DT] Model loaded');
        const model = gltf.scene;
    
        // Force world-matrix update before measuring
        model.updateMatrixWorld(true);
    
        // Iterative traversal to safely modify materials
        const queue = [model];
        while (queue.length > 0) {{
            const node = queue.shift();
            
            if (node.isMesh === true && node.material) {{
                const mat = Array.isArray(node.material) ? node.material[0] : node.material;
                
                // Initialize colors matching the clean white style
                if (mat.color && mat.color.setHex) mat.color.setHex(0x3e3532);
                if (mat.emissive && mat.emissive.setHex) mat.emissive.setHex(0xffffff);
                mat.emissiveIntensity = 0.2;
                
                if (!motorMaterials.includes(mat)) {{
                    motorMaterials.push(mat);
                }}
            }}
    
            if (node.children) {{
                for (let i = 0; i < node.children.length; i++) {{
                    queue.push(node.children[i]);
                }}
            }}
        }}
    
        // Calculate bounding box iteratively
        const min = new THREE.Vector3(Infinity, Infinity, Infinity);
        const max = new THREE.Vector3(-Infinity, -Infinity, -Infinity);
        const boxQueue = [model];
        
        while (boxQueue.length > 0) {{
            const node = boxQueue.shift();
            if (node.isMesh && node.geometry) {{
                node.geometry.computeBoundingBox();
                const bBox = node.geometry.boundingBox;
                if (bBox) {{
                    const worldMin = bBox.min.clone().applyMatrix4(node.matrixWorld);
                    const worldMax = bBox.max.clone().applyMatrix4(node.matrixWorld);
                    min.min(worldMin);
                    max.max(worldMax);
                }}
            }}
            if (node.children) {{
                for (let i = 0; i < node.children.length; i++) {{
                    boxQueue.push(node.children[i]);
                }}
            }}
        }}
    
        // Center and scale
        const center = new THREE.Vector3().addVectors(min, max).multiplyScalar(0.5);
        const size = new THREE.Vector3().subVectors(max, min).length();
        
        model.position.sub(center);
        const scale = (size > 0 && size !== Infinity) ? (2.8 / size) : 1;
        model.scale.setScalar(scale);
    
        scene.add(model);
    }}, undefined, function(err) {{
        console.error('[DT] GLTFLoader error:', err);
    }});
    
    /* ── Resize Handler ── */
    window.addEventListener('resize', () => {{
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }});
    
    /* ── Temperature and Color Mapping ── */
    const C = {{
        blue:   new THREE.Color(0x60a5fa),
        green:  new THREE.Color(0xffffff),
        yellow: new THREE.Color(0xfbbf24),
        orange: new THREE.Color(0xfbbf24),
        red:    new THREE.Color(0xf87171)
    }};
    
    let targetColor = C.green.clone();
    let targetIntensity = 0.2;
    let currentTemp = 50.0;
    const tempDisp = document.getElementById('temp-display');
    
    /* ── Render Loop ── */
    function animate() {{
        requestAnimationFrame(animate);
        controls.update();
    
        // Read temperature from parent Streamlit page
        try {{
            const el = window.parent.document.getElementById('live-telemetry-data');
            if (el) {{
                const data = JSON.parse(el.textContent);
                if (data && typeof data.temperature === 'number') {{
                    currentTemp = data.temperature;
                }}
            }}
        }} catch(_) {{}}
    
        tempDisp.textContent = currentTemp.toFixed(1) + ' °C';
    
        // Map temperature to color and intensity
        if (currentTemp < 35)      {{ targetColor.copy(C.blue);   targetIntensity = 0.3; }}
        else if (currentTemp < 50) {{ targetColor.copy(C.green);  targetIntensity = 0.4; }}
        else if (currentTemp < 65) {{ targetColor.copy(C.yellow); targetIntensity = 0.6; }}
        else if (currentTemp < 80) {{ targetColor.copy(C.orange); targetIntensity = 0.8; }}
        else                       {{ targetColor.copy(C.red);    targetIntensity = 1.0 + Math.sin(Date.now() / 150) * 0.8; }}
    
        // Smoothly lerp material properties
        for (const mat of motorMaterials) {{
            mat.emissive.lerp(targetColor, 0.05);
            mat.color.lerp(targetColor.clone().multiplyScalar(0.4), 0.05);
            mat.emissiveIntensity += (targetIntensity - mat.emissiveIntensity) * 0.1;
        }}
    
        renderer.render(scene, camera);
    }}
    animate();
    </script>
    </body>
    </html>"""


def diagnostics_assistant_html() -> str:
    return """<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
/* ── RESET ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
    margin: 0; padding: 10px;
    background: transparent;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', sans-serif;
    color: #e2e8f0;
    height: 100vh;
    overflow: hidden;
}

/* ── MAIN PANEL (Glassmorphism) ── */
.trinity-panel {
    background: linear-gradient(135deg, rgba(20, 24, 33, 0.4) 0%, rgba(10, 12, 16, 0.55) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 8px;
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.05);
    height: calc(100vh - 20px);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

/* ── HEADER BAR ── */
.trinity-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    flex-shrink: 0;
}
.header-left {
    display: flex;
    align-items: center;
    gap: 10px;
}
.header-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 8px rgba(52, 211, 153, 0.5);
    animation: dot-pulse 2.5s ease-in-out infinite;
}
@keyframes dot-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.35; }
}
.header-title {
    font-size: 0.68rem;
    font-weight: 600;
    color: #94a3b8;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.status-pill {
    font-size: 0.6rem;
    font-weight: 600;
    color: #64748b;
    letter-spacing: 0.08em;
    padding: 4px 12px;
    border-radius: 100px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.status-pill.active {
    color: #60a5fa;
    background: rgba(96, 165, 250, 0.08);
    border-color: rgba(96, 165, 250, 0.2);
    box-shadow: 0 0 14px rgba(96, 165, 250, 0.08);
}
.status-pill.speaking {
    color: #34d399;
    background: rgba(52, 211, 153, 0.08);
    border-color: rgba(52, 211, 153, 0.2);
    box-shadow: 0 0 14px rgba(52, 211, 153, 0.08);
}
.status-pill.critical {
    color: #f87171;
    background: rgba(248, 113, 113, 0.08);
    border-color: rgba(248, 113, 113, 0.2);
    box-shadow: 0 0 14px rgba(248, 113, 113, 0.08);
    animation: pill-pulse 1.5s ease-in-out infinite;
}
@keyframes pill-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.55; }
}

/* ── BODY (3-Column) ── */
.trinity-body {
    display: flex;
    flex: 1;
    overflow: hidden;
    gap: 0;
}

/* ── LEFT: AI CORE ── */
.col-orb {
    flex: 0 0 150px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 16px 12px;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    gap: 10px;
}
.orb-container {
    position: relative;
    width: 105px;
    height: 105px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.orb-ring {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.06);
}
.ring-outer {
    width: 105px; height: 105px;
    animation: ring-rotate 25s linear infinite;
    border-style: dashed;
    border-color: rgba(255, 255, 255, 0.07);
}
.ring-inner {
    width: 85px; height: 85px;
    animation: ring-rotate 16s linear infinite reverse;
    border-color: rgba(96, 165, 250, 0.1);
}
@keyframes ring-rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
.orb {
    width: 64px; height: 64px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%,
        rgba(255, 255, 255, 0.14) 0%,
        rgba(96, 165, 250, 0.07) 40%,
        rgba(15, 23, 42, 0.6) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow:
        0 0 20px rgba(96, 165, 250, 0.08),
        inset 0 -8px 16px rgba(0, 0, 0, 0.3),
        inset 0 2px 4px rgba(255, 255, 255, 0.1);
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    z-index: 2;
}
.orb::before {
    content: '';
    width: 22px; height: 22px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.25), transparent);
    position: absolute;
    top: 10px; left: 14px;
    filter: blur(3px);
}
.orb.standby { animation: orb-breathe 4s ease-in-out infinite; }
.orb.listening {
    background: radial-gradient(circle at 35% 35%,
        rgba(96, 165, 250, 0.28) 0%,
        rgba(96, 165, 250, 0.1) 40%,
        rgba(15, 23, 42, 0.6) 100%);
    border-color: rgba(96, 165, 250, 0.3);
    box-shadow:
        0 0 30px rgba(96, 165, 250, 0.18),
        0 0 60px rgba(96, 165, 250, 0.05),
        inset 0 -8px 16px rgba(0, 0, 0, 0.3),
        inset 0 2px 4px rgba(96, 165, 250, 0.2);
    animation: orb-listen 1.5s ease-in-out infinite;
}
.orb.speaking {
    background: radial-gradient(circle at 35% 35%,
        rgba(52, 211, 153, 0.22) 0%,
        rgba(52, 211, 153, 0.08) 40%,
        rgba(15, 23, 42, 0.6) 100%);
    border-color: rgba(52, 211, 153, 0.25);
    box-shadow:
        0 0 25px rgba(52, 211, 153, 0.12),
        inset 0 -8px 16px rgba(0, 0, 0, 0.3),
        inset 0 2px 4px rgba(52, 211, 153, 0.15);
    animation: orb-speak 0.8s ease-in-out infinite;
}
.orb.critical {
    background: radial-gradient(circle at 35% 35%,
        rgba(248, 113, 113, 0.22) 0%,
        rgba(248, 113, 113, 0.08) 40%,
        rgba(15, 23, 42, 0.6) 100%);
    border-color: rgba(248, 113, 113, 0.3);
    box-shadow: 0 0 30px rgba(248, 113, 113, 0.18),
        inset 0 -8px 16px rgba(0, 0, 0, 0.3);
    animation: orb-critical 1s ease-in-out infinite;
}
@keyframes orb-breathe {
    0%, 100% { transform: scale(1); opacity: 0.85; }
    50% { transform: scale(1.04); opacity: 1; }
}
@keyframes orb-listen {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.07); }
}
@keyframes orb-speak {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.04); }
}
@keyframes orb-critical {
    0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(248, 113, 113, 0.12); }
    50% { transform: scale(1.05); box-shadow: 0 0 40px rgba(248, 113, 113, 0.25); }
}
.orb-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: #e2e8f0;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}
.orb-status {
    font-size: 0.58rem;
    font-weight: 500;
    color: #64748b;
    letter-spacing: 0.06em;
    text-align: center;
    transition: color 0.4s;
}
.mic-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    margin-top: 6px;
}
.mic-btn {
    width: 34px; height: 34px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #64748b;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
}
.mic-btn::after {
    content: '';
    position: absolute;
    width: 100%; height: 100%;
    border-radius: 50%;
    background: rgba(96, 165, 250, 0.12);
    transform: scale(0);
    transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.mic-btn.active {
    color: #60a5fa;
    border-color: rgba(96, 165, 250, 0.3);
    box-shadow: 0 0 14px rgba(96, 165, 250, 0.1);
}
.mic-btn.active::after {
    transform: scale(2.5);
    animation: mic-ripple 2s ease-out infinite;
}
@keyframes mic-ripple {
    0% { transform: scale(1); opacity: 0.25; }
    100% { transform: scale(2.5); opacity: 0; }
}
.mic-label {
    font-size: 0.5rem;
    font-weight: 500;
    color: #475569;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── CENTER: CONVERSATION ── */
.col-chat {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 14px;
    gap: 10px;
    min-width: 0;
}
.chat-window {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding-right: 4px;
}
.msg {
    max-width: 88%;
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 0.8rem;
    line-height: 1.55;
    animation: msg-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes msg-in {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
.msg.user {
    align-self: flex-start;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    color: #cbd5e1;
}
.msg.trinity {
    align-self: flex-end;
    background: linear-gradient(135deg, rgba(96, 165, 250, 0.06) 0%, rgba(52, 211, 153, 0.03) 100%);
    border: 1px solid rgba(96, 165, 250, 0.1);
    color: #e2e8f0;
    text-align: left;
}
.sender-tag {
    font-size: 0.55rem;
    font-weight: 600;
    color: #60a5fa;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
    text-transform: uppercase;
}

/* ── PROOF CARDS (Inline Visualizations) ── */
.proof-card {
    margin-top: 8px;
    padding: 10px 12px;
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    animation: msg-in 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
}
.proof-row {
    display: flex;
    align-items: center;
    gap: 10px;
}
.proof-value {
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff;
}
.proof-label {
    font-size: 0.6rem;
    font-weight: 500;
    color: #64748b;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.proof-bar-wrap { width: 100%; margin-top: 6px; }
.proof-bar {
    height: 3px;
    border-radius: 2px;
    background: rgba(255, 255, 255, 0.05);
    overflow: hidden;
}
.proof-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.proof-bar-fill.green  { background: linear-gradient(90deg, #34d399, #059669); }
.proof-bar-fill.yellow { background: linear-gradient(90deg, #fbbf24, #d97706); }
.proof-bar-fill.red    { background: linear-gradient(90deg, #f87171, #dc2626); }
.proof-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    width: 100%;
    margin-top: 8px;
}
.proof-item {
    padding: 6px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.04);
    text-align: center;
}
.proof-item-val {
    font-size: 0.85rem;
    font-weight: 600;
    color: #ffffff;
    font-variant-numeric: tabular-nums;
}
.proof-item-lbl {
    font-size: 0.5rem;
    font-weight: 500;
    color: #64748b;
    margin-top: 1px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.proof-badge {
    padding: 3px 10px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    font-size: 0.6rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: capitalize;
}

/* ── INPUT AREA ── */
.input-row {
    display: flex;
    gap: 8px;
    flex-shrink: 0;
}
.input-row input[type="text"] {
    flex: 1;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 10px 16px;
    font-family: 'Inter', -apple-system, sans-serif;
    font-size: 0.78rem;
    font-weight: 400;
    color: #e2e8f0;
    outline: none;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.input-row input[type="text"]::placeholder { color: #475569; }
.input-row input[type="text"]:focus {
    border-color: rgba(96, 165, 250, 0.3);
    background: rgba(255, 255, 255, 0.05);
    box-shadow: 0 0 20px rgba(96, 165, 250, 0.05);
}
.send-btn {
    width: 38px; height: 38px;
    border-radius: 12px;
    background: rgba(96, 165, 250, 0.1);
    border: 1px solid rgba(96, 165, 250, 0.15);
    color: #60a5fa;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    flex-shrink: 0;
}
.send-btn:hover {
    background: rgba(96, 165, 250, 0.18);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(96, 165, 250, 0.1);
}

/* ── RIGHT: LIVE TELEMETRY ── */
.col-telemetry {
    flex: 0 0 190px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 14px 12px;
    border-left: 1px solid rgba(255, 255, 255, 0.05);
    gap: 8px;
    overflow-y: auto;
}
.gauge-label {
    font-size: 0.55rem;
    font-weight: 600;
    color: #64748b;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: -2px;
}
#health-gauge { flex-shrink: 0; }
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
    width: 100%;
}
.mini-card {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 7px 5px;
    text-align: center;
    transition: all 0.3s;
}
.mini-card:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
}
.mc-label {
    font-size: 0.46rem;
    font-weight: 600;
    color: #475569;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.mc-value {
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
    margin: 1px 0;
    font-variant-numeric: tabular-nums;
}
.mc-unit {
    font-size: 0.46rem;
    font-weight: 500;
    color: #475569;
}

/* Anomaly bar */
.anomaly-section { width: 100%; padding: 0 2px; }
.anomaly-label {
    font-size: 0.46rem;
    font-weight: 600;
    color: #475569;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.anomaly-bar {
    width: 100%;
    height: 3px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 2px;
    overflow: hidden;
}
.anomaly-fill {
    height: 100%;
    width: 0%;
    border-radius: 2px;
    background: linear-gradient(90deg, #34d399, #fbbf24, #f87171);
    transition: width 1s cubic-bezier(0.16, 1, 0.3, 1);
}
.anomaly-value {
    font-size: 0.6rem;
    font-weight: 600;
    color: #94a3b8;
    margin-top: 2px;
    text-align: right;
    font-variant-numeric: tabular-nums;
}

/* Waveform */
.wave-label {
    font-size: 0.46rem;
    font-weight: 600;
    color: #475569;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    align-self: flex-start;
    margin-left: 2px;
    margin-bottom: -2px;
}
#vib-waveform {
    width: 100%;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.015);
    border: 1px solid rgba(255, 255, 255, 0.04);
}

/* Predictive pill */
.pred-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 11px;
    border-radius: 100px;
    background: rgba(52, 211, 153, 0.06);
    border: 1px solid rgba(52, 211, 153, 0.12);
    transition: all 0.5s;
}
.pred-pill.warning {
    background: rgba(251, 191, 36, 0.06);
    border-color: rgba(251, 191, 36, 0.12);
}
.pred-pill.warning .pred-dot { background: #fbbf24; box-shadow: 0 0 6px rgba(251, 191, 36, 0.4); }
.pred-pill.warning .pred-text { color: #fbbf24; }
.pred-pill.critical {
    background: rgba(248, 113, 113, 0.06);
    border-color: rgba(248, 113, 113, 0.12);
}
.pred-pill.critical .pred-dot { background: #f87171; box-shadow: 0 0 6px rgba(248, 113, 113, 0.4); }
.pred-pill.critical .pred-text { color: #f87171; }
.pred-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 6px rgba(52, 211, 153, 0.4);
}
.pred-text {
    font-size: 0.5rem;
    font-weight: 600;
    color: #34d399;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* Scrollbar */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.08); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.15); }
</style>
</head>
<body>

<div class="trinity-panel">
    <div class="trinity-header">
        <div class="header-left">
            <div class="header-dot" id="header-dot"></div>
            <span class="header-title">TRINITY AI CORE</span>
        </div>
        <div class="header-right">
            <span class="status-pill" id="status-pill">STANDBY</span>
        </div>
    </div>

    <div class="trinity-body">
        <!-- LEFT: AI Core -->
        <div class="col-orb">
            <div class="orb-container">
                <div class="orb-ring ring-outer"></div>
                <div class="orb-ring ring-inner"></div>
                <div class="orb standby" id="trinity-orb"></div>
            </div>
            <div class="orb-label">TRINITY</div>
            <div class="orb-status" id="trinity-status">Awaiting</div>
            <div class="mic-area">
                <button class="mic-btn" id="mic-btn" title="Microphone">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"></path>
                        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                        <line x1="12" y1="19" x2="12" y2="23"></line>
                    </svg>
                </button>
                <span class="mic-label" id="mic-text">MIC OFF</span>
            </div>
        </div>

        <!-- CENTER: Conversation -->
        <div class="col-chat">
            <div class="chat-window" id="chat">
                <div class="msg trinity">
                    <div class="sender-tag">TRINITY</div>
                    Systems online. Monitoring all sensor channels.<br><br>
                    Say <strong>"Hey Trinity"</strong> or type a query below.
                </div>
            </div>
            <div class="input-row">
                <input type="text" id="query-input" placeholder="Ask Trinity anything..." />
                <button class="send-btn" id="send-btn" title="Send" style="width:auto; padding:0 12px; font-weight:600; letter-spacing:0.05em; font-size:0.75rem;">
                    SEND
                </button>
            </div>
        </div>

        <!-- RIGHT: Live Telemetry -->
        <div class="col-telemetry">
            <div class="gauge-label">SYSTEM HEALTH</div>
            <canvas id="health-gauge" width="160" height="125"></canvas>
            <div class="metric-grid">
                <div class="mini-card"><div class="mc-label">TEMP</div><div class="mc-value" id="mv-temp">--</div><div class="mc-unit">&deg;C</div></div>
                <div class="mini-card"><div class="mc-label">RPM</div><div class="mc-value" id="mv-rpm">--</div><div class="mc-unit">rev/m</div></div>
                <div class="mini-card"><div class="mc-label">VIB</div><div class="mc-value" id="mv-vib">--</div><div class="mc-unit">mm/s</div></div>
                <div class="mini-card"><div class="mc-label">AMPS</div><div class="mc-value" id="mv-cur">--</div><div class="mc-unit">A</div></div>
            </div>
            <div class="anomaly-section">
                <div class="anomaly-label">ANOMALY CONFIDENCE</div>
                <div class="anomaly-bar"><div class="anomaly-fill" id="anomaly-fill"></div></div>
                <div class="anomaly-value" id="anomaly-value">0%</div>
            </div>
            <div class="wave-label">VIBRATION WAVEFORM</div>
            <canvas id="vib-waveform" width="166" height="48"></canvas>
            <div class="pred-pill" id="pred-pill">
                <span class="pred-dot"></span>
                <span class="pred-text" id="pred-text">NOMINAL</span>
            </div>
        </div>
    </div>
</div>

<script>
/* ── DOM REFS ── */
const orb = document.getElementById('trinity-orb');
const statusText = document.getElementById('trinity-status');
const statusPill = document.getElementById('status-pill');
const headerDot = document.getElementById('header-dot');
const chatEl = document.getElementById('chat');
const queryInput = document.getElementById('query-input');
const micBtn = document.getElementById('mic-btn');
const micText = document.getElementById('mic-text');
const sendBtn = document.getElementById('send-btn');
const gaugeCanvas = document.getElementById('health-gauge');
const waveCanvas = document.getElementById('vib-waveform');
const anomalyFill = document.getElementById('anomaly-fill');
const anomalyValue = document.getElementById('anomaly-value');
const predPill = document.getElementById('pred-pill');
const predText = document.getElementById('pred-text');

let recognition = null;
let isAwake = false;
let isSpeaking = false;
let awakeTimeout = null;
let animHealthTarget = 0;
let animHealthCurrent = 0;

/* ── AUDIO ── */
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function playWakeSound() {
    if (!audioCtx) audioCtx = new AudioContext();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(660, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(1320, audioCtx.currentTime + 0.12);
    gain.gain.setValueAtTime(0, audioCtx.currentTime);
    gain.gain.linearRampToValueAtTime(0.07, audioCtx.currentTime + 0.04);
    gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.25);
    osc.start(audioCtx.currentTime);
    osc.stop(audioCtx.currentTime + 0.25);
}

/* ── TELEMETRY ── */
function getTelemetry() {
    try {
        const el = window.parent.document.getElementById('live-telemetry-data');
        if (el) return JSON.parse(el.textContent);
    } catch(e) {}
    return null;
}

/* ── GREETING ── */
function getGreeting() {
    const h = new Date().getHours();
    if (h < 12) return 'Good morning';
    if (h < 17) return 'Good afternoon';
    return 'Good evening';
}

/* ── VISUAL STATE ── */
function updateVisualState() {
    const t = getTelemetry();
    const isCritical = t && (t.fault_severity === 'Severe' || t.status === 'critical');

    orb.className = 'orb';
    statusPill.className = 'status-pill';

    if (isSpeaking) {
        orb.classList.add('speaking');
        statusText.textContent = 'Responding';
        statusPill.textContent = 'RESPONDING';
        statusPill.classList.add('speaking');
    } else if (isAwake) {
        orb.classList.add('listening');
        statusText.textContent = 'Listening';
        statusPill.textContent = 'LISTENING';
        statusPill.classList.add('active');
    } else if (isCritical) {
        orb.classList.add('critical');
        statusText.textContent = 'Alert Active';
        statusPill.textContent = 'CRITICAL';
        statusPill.classList.add('critical');
        headerDot.style.background = '#f87171';
        headerDot.style.boxShadow = '0 0 8px rgba(248,113,113,0.5)';
    } else {
        orb.classList.add('standby');
        statusText.textContent = 'Awaiting';
        statusPill.textContent = 'STANDBY';
        headerDot.style.background = '#34d399';
        headerDot.style.boxShadow = '0 0 8px rgba(52,211,153,0.5)';
    }

    /* Update right panel telemetry */
    if (t) {
        document.getElementById('mv-temp').textContent = parseFloat(t.temperature || 0).toFixed(1);
        document.getElementById('mv-rpm').textContent = parseInt(t.rpm || 0);
        document.getElementById('mv-vib').textContent = parseFloat(t.vibration || 0).toFixed(2);
        document.getElementById('mv-cur').textContent = parseFloat(t.current || 0).toFixed(2);

        animHealthTarget = parseFloat(t.health_score || 0);

        const devScore = parseFloat(t.deviation_score || 0);
        anomalyFill.style.width = Math.min(devScore, 100) + '%';
        anomalyValue.textContent = devScore.toFixed(1) + '%';

        predPill.className = 'pred-pill';
        const hs = parseFloat(t.health_score || 100);
        if (hs >= 80) { predText.textContent = 'NOMINAL'; }
        else if (hs >= 50) { predText.textContent = 'MONITOR'; predPill.classList.add('warning'); }
        else { predText.textContent = 'CRITICAL'; predPill.classList.add('critical'); }
    }
}

/* ── HEALTH GAUGE (Canvas) ── */
function drawHealthGauge() {
    animHealthCurrent += (animHealthTarget - animHealthCurrent) * 0.08;
    const health = animHealthCurrent;

    const ctx = gaugeCanvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const w = 160, h = 125;
    gaugeCanvas.width = w * dpr;
    gaugeCanvas.height = h * dpr;
    gaugeCanvas.style.width = w + 'px';
    gaugeCanvas.style.height = h + 'px';
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, w, h);

    const cx = w / 2, cy = 68;
    const r = 48;
    const startAngle = Math.PI * 0.8;
    const endAngle = Math.PI * 2.2;
    const totalArc = endAngle - startAngle;

    /* Background arc */
    ctx.beginPath();
    ctx.arc(cx, cy, r, startAngle, endAngle, false);
    ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    ctx.lineWidth = 6;
    ctx.lineCap = 'round';
    ctx.stroke();

    /* Colored arc */
    const pct = Math.max(0, Math.min(100, health));
    const arcEnd = startAngle + (pct / 100) * totalArc;
    let color;
    if (pct >= 80) color = '#34d399';
    else if (pct >= 50) color = '#fbbf24';
    else color = '#f87171';

    if (pct > 0) {
        ctx.beginPath();
        ctx.arc(cx, cy, r, startAngle, arcEnd, false);
        ctx.strokeStyle = color;
        ctx.lineWidth = 6;
        ctx.lineCap = 'round';
        ctx.shadowColor = color;
        ctx.shadowBlur = 10;
        ctx.stroke();
        ctx.shadowBlur = 0;
    }

    /* Center value */
    ctx.fillStyle = '#ffffff';
    ctx.font = '700 22px Inter, -apple-system, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(Math.round(pct) + '%', cx, cy - 2);

    ctx.fillStyle = '#475569';
    ctx.font = '600 7px Inter, -apple-system, sans-serif';
    ctx.fillText('MOTOR HEALTH', cx, cy + 16);
}

/* ── VIBRATION WAVEFORM (Canvas) ── */
let wavePhase = 0;
let analyser, dataArray;
let micStream = null;

async function setupLiveAudio() {
    if (audioCtx) return;
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        micStream = stream;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        analyser.fftSize = 256;
        const source = audioCtx.createMediaStreamSource(stream);
        source.connect(analyser);
        dataArray = new Uint8Array(analyser.frequencyBinCount);
    } catch(err) {
        console.error('Audio capture failed:', err);
    }
}

function drawWaveform() {
    const ctx = waveCanvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const w = 166, h = 48;
    waveCanvas.width = w * dpr;
    waveCanvas.height = h * dpr;
    waveCanvas.style.width = '100%';
    waveCanvas.style.height = h + 'px';
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, w, h);

    let amplitude = 0;
    
    // If Trinity is awake and listening, use live mic input for the waveform
    if (isAwake && analyser) {
        analyser.getByteTimeDomainData(dataArray);
        let maxDev = 0;
        for (let i = 0; i < dataArray.length; i++) {
            let dev = Math.abs(dataArray[i] - 128);
            if (dev > maxDev) maxDev = dev;
        }
        amplitude = Math.min((maxDev / 128) * h, h * 0.45);
    } else {
        // Otherwise use the motor vibration telemetry
        const t = getTelemetry();
        const vib = t ? parseFloat(t.vibration || 0) : 0;
        amplitude = Math.min(vib * 2.5, h * 0.38);
    }
    
    wavePhase += 0.04;

    /* Glow layer */
    ctx.beginPath();
    for (let x = 0; x < w; x++) {
        const p = x / w;
        const y = h / 2
            + Math.sin(p * Math.PI * 4 + wavePhase) * amplitude * 0.7
            + Math.sin(p * Math.PI * 7 + wavePhase * 1.3) * amplitude * 0.3;
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = 'rgba(96, 165, 250, 0.12)';
    ctx.lineWidth = 5;
    ctx.stroke();

    /* Sharp line */
    ctx.beginPath();
    for (let x = 0; x < w; x++) {
        const p = x / w;
        const y = h / 2
            + Math.sin(p * Math.PI * 4 + wavePhase) * amplitude * 0.7
            + Math.sin(p * Math.PI * 7 + wavePhase * 1.3) * amplitude * 0.3;
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = 'rgba(96, 165, 250, 0.45)';
    ctx.lineWidth = 1.5;
    ctx.stroke();
}

/* ── ANIMATION LOOP ── */
function animationLoop() {
    requestAnimationFrame(animationLoop);
    drawHealthGauge();
    drawWaveform();
}
animationLoop();

/* ── WAKE / SLEEP ── */
function wakeTrinity() {
    if (isAwake) return;
    isAwake = true;
    setupLiveAudio();
    playWakeSound();
    updateVisualState();
    clearTimeout(awakeTimeout);
    awakeTimeout = setTimeout(() => { sleepTrinity(); }, 15000);
}
function sleepTrinity() {
    isAwake = false;
    clearTimeout(awakeTimeout);
    updateVisualState();
}

/* ── SPEECH RECOGNITION ── */
function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SR();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            micBtn.classList.add('active');
            micText.textContent = 'LIVE';
            setupLiveAudio();
        };
        recognition.onerror = function(event) {
            if (event.error !== 'no-speech') {
                micBtn.classList.remove('active');
                micText.textContent = 'ERROR';
                setTimeout(() => { try { recognition.start(); } catch(e){} }, 2000);
            }
        };
        recognition.onend = function() {
            micBtn.classList.remove('active');
            micText.textContent = 'RESTART';
            setTimeout(() => { try { recognition.start(); } catch(e){} }, 1000);
        };
        recognition.onresult = function(event) {
            let finalT = '', interimT = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) finalT += event.results[i][0].transcript;
                else interimT += event.results[i][0].transcript;
            }
            const text = (finalT + interimT).toLowerCase();
            
            if (!isAwake && (text.includes('hey trinity') || text.includes('hey, trinity'))) {
                wakeTrinity();
                return;
            }
            if (isAwake && finalT.trim() !== '') {
                let query = finalT.toLowerCase().split('hey trinity').join('').split('hey, trinity').join('').trim();
                if (query.length > 2) {
                    clearTimeout(awakeTimeout);
                    handleQuery(query);
                    sleepTrinity();
                }
            }
        };
        try { recognition.start(); } catch(e) {}
    } else {
        micText.textContent = 'N/A';
        console.error('Speech recognition not supported in this browser.');
    }
}

/* ── TTS ── */
function speak(text) {
    if (!('speechSynthesis' in window)) return;
    const utt = new SpeechSynthesisUtterance(text);
    utt.rate = 1.0;
    utt.pitch = 0.85;
    const voices = window.speechSynthesis.getVoices();
    const voice = voices.find(v => v.name.includes('Google UK English Female') || v.name.includes('Samantha') || v.lang === 'en-GB');
    if (voice) utt.voice = voice;
    utt.onstart = () => { isSpeaking = true; updateVisualState(); };
    utt.onend = () => { isSpeaking = false; updateVisualState(); };
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utt);
}

/* ── MESSAGES ── */
function addMessage(text, sender) {
    const msg = document.createElement('div');
    msg.className = 'msg ' + sender;
    if (sender === 'trinity') {
        msg.innerHTML = '<div class="sender-tag">TRINITY</div>' + text.split(String.fromCharCode(10)).join('<br>');
    } else {
        msg.textContent = text;
    }
    chatEl.appendChild(msg);
    chatEl.scrollTop = chatEl.scrollHeight;
    return msg;
}

/* ── PROOF VISUALIZATIONS ── */
function addProof(type, t) {
    if (!t) return;
    let html = '';

    if (type === 'health') {
        const h = parseFloat(t.health_score || 0);
        const color = h >= 80 ? '#34d399' : (h >= 50 ? '#fbbf24' : '#f87171');
        const cls = h >= 80 ? 'green' : (h >= 50 ? 'yellow' : 'red');
        html = '<div class="proof-card">' +
            '<div class="proof-row"><div class="proof-value" style="color:' + color + '">' + h.toFixed(1) + '%</div>' +
            '<div class="proof-label">Motor Health Score</div></div>' +
            '<div class="proof-bar-wrap"><div class="proof-bar"><div class="proof-bar-fill ' + cls + '" style="width:' + h + '%"></div></div></div>' +
            '<div class="proof-grid">' +
            '<div class="proof-item"><div class="proof-item-val">' + parseFloat(t.temperature||0).toFixed(1) + '&deg;</div><div class="proof-item-lbl">Temp</div></div>' +
            '<div class="proof-item"><div class="proof-item-val">' + parseFloat(t.vibration||0).toFixed(2) + '</div><div class="proof-item-lbl">Vibration</div></div>' +
            '<div class="proof-item"><div class="proof-item-val">' + parseInt(t.rpm||0) + '</div><div class="proof-item-lbl">RPM</div></div>' +
            '<div class="proof-item"><div class="proof-item-val">' + parseFloat(t.current||0).toFixed(2) + 'A</div><div class="proof-item-lbl">Current</div></div>' +
            '</div></div>';
    } else if (type === 'temperature') {
        const temp = parseFloat(t.temperature || 0);
        const pct = Math.min((temp / 120) * 100, 100);
        const color = temp < 50 ? '#34d399' : (temp < 75 ? '#fbbf24' : '#f87171');
        const cls = temp < 50 ? 'green' : (temp < 75 ? 'yellow' : 'red');
        html = '<div class="proof-card">' +
            '<div class="proof-row"><div class="proof-value" style="color:' + color + '">' + temp.toFixed(1) + '&deg;C</div>' +
            '<div class="proof-label">Core Temperature</div></div>' +
            '<div class="proof-bar-wrap"><div class="proof-bar"><div class="proof-bar-fill ' + cls + '" style="width:' + pct + '%"></div></div></div>' +
            '</div>';
    } else if (type === 'vibration') {
        const vib = parseFloat(t.vibration || 0);
        const pct = Math.min((vib / 10) * 100, 100);
        const color = vib < 3 ? '#34d399' : (vib < 6 ? '#fbbf24' : '#f87171');
        const cls = vib < 3 ? 'green' : (vib < 6 ? 'yellow' : 'red');
        html = '<div class="proof-card">' +
            '<div class="proof-row"><div class="proof-value" style="color:' + color + '">' + vib.toFixed(2) + ' mm/s</div>' +
            '<div class="proof-label">Axial Vibration</div></div>' +
            '<div class="proof-bar-wrap"><div class="proof-bar"><div class="proof-bar-fill ' + cls + '" style="width:' + pct + '%"></div></div></div>' +
            '</div>';
    } else if (type === 'anomaly') {
        const dev = parseFloat(t.deviation_score || 0);
        const ft = (t.fault_type && t.fault_type !== 'none') ? t.fault_type.split('_').join(' ') : 'None';
        const color = dev < 10 ? '#34d399' : (dev < 25 ? '#fbbf24' : '#f87171');
        const cls = dev < 10 ? 'green' : (dev < 25 ? 'yellow' : 'red');
        html = '<div class="proof-card">' +
            '<div style="display:flex;justify-content:space-between;align-items:center;">' +
            '<div><div class="proof-value" style="color:' + color + '">' + dev.toFixed(1) + '%</div><div class="proof-label">Deviation Score</div></div>' +
            '<div class="proof-badge">' + ft + '</div></div>' +
            '<div class="proof-bar-wrap"><div class="proof-bar"><div class="proof-bar-fill ' + cls + '" style="width:' + Math.min(dev, 100) + '%"></div></div></div>' +
            '</div>';
    } else if (type === 'rpm') {
        const rpm = parseInt(t.rpm || 0);
        const pct = Math.min((rpm / 5000) * 100, 100);
        html = '<div class="proof-card">' +
            '<div class="proof-row"><div class="proof-value">' + rpm + '</div>' +
            '<div class="proof-label">Rotor Speed (RPM)</div></div>' +
            '<div class="proof-bar-wrap"><div class="proof-bar"><div class="proof-bar-fill green" style="width:' + pct + '%"></div></div></div>' +
            '</div>';
    } else if (type === 'current') {
        const cur = parseFloat(t.current || 0);
        const pct = Math.min((cur / 20) * 100, 100);
        html = '<div class="proof-card">' +
            '<div class="proof-row"><div class="proof-value">' + cur.toFixed(2) + ' A</div>' +
            '<div class="proof-label">Electrical Draw</div></div>' +
            '<div class="proof-bar-wrap"><div class="proof-bar"><div class="proof-bar-fill green" style="width:' + pct + '%"></div></div></div>' +
            '</div>';
    } else if (type === 'status') {
        html = '<div class="proof-card"><div class="proof-grid">' +
            '<div class="proof-item"><div class="proof-item-val">' + parseFloat(t.health_score||0).toFixed(0) + '%</div><div class="proof-item-lbl">Health</div></div>' +
            '<div class="proof-item"><div class="proof-item-val">' + (t.twin_status||'N/A') + '</div><div class="proof-item-lbl">Twin Sync</div></div>' +
            '<div class="proof-item"><div class="proof-item-val">' + parseFloat(t.deviation_score||0).toFixed(1) + '%</div><div class="proof-item-lbl">Deviation</div></div>' +
            '<div class="proof-item"><div class="proof-item-val">' + parseFloat(t.temperature||0).toFixed(1) + '&deg;</div><div class="proof-item-lbl">Temperature</div></div>' +
            '</div></div>';
    }

    if (html) {
        const wrapper = document.createElement('div');
        wrapper.style.alignSelf = 'flex-end';
        wrapper.style.maxWidth = '88%';
        wrapper.innerHTML = html;
        chatEl.appendChild(wrapper);
        chatEl.scrollTop = chatEl.scrollHeight;
    }
}

/* ── QUERY HANDLER ── */
async function handleQuery(query) {
    addMessage(query, 'user');
    const t = getTelemetry();
    if (!t) {
        addMessage('Telemetry stream unavailable. Unable to access sensor data.', 'trinity');
        speak('Telemetry stream unavailable.');
        return;
    }

    try {
        // Show typing indicator
        const thinkingMsg = addMessage('Analyzing telemetry...', 'trinity');
        
        let host = 'localhost';
        try { host = window.location.hostname || window.parent.location.hostname || 'localhost'; } catch(e) {}
        
        const response = await fetch('http://' + host + ':8000/ask-trinity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query, telemetry: t })
        });
        
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        // Remove thinking message
        thinkingMsg.remove();
        
        // Render Response
        addMessage(data.response, 'trinity');
        
        // If a specific proof type was requested and it's not 'none', try to render it.
        // Fall back to general status if the type isn't explicitly supported in addProof yet.
        const supportedProofs = ['health', 'temperature', 'vibration', 'current', 'rpm', 'anomaly', 'status'];
        let pType = supportedProofs.includes(data.proof_type) ? data.proof_type : 'status';
        if (data.proof_type !== 'none') {
            addProof(pType, t);
        }
        
        speak(data.response);
        
    } catch (err) {
        console.error('Trinity API Error:', err);
        addMessage('Connection to AI Core lost. Operating on local cache.', 'trinity');
        speak('Connection to AI Core lost.');
    }
}

/* ── INPUT HANDLERS ── */
document.body.addEventListener('click', () => {
    if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
});

micBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
    if (!isAwake) {
        wakeTrinity();
    } else {
        sleepTrinity();
    }
});

queryInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const text = queryInput.value.trim();
        if (text) {
            wakeTrinity();
            handleQuery(text);
            queryInput.value = '';
            sleepTrinity();
        }
    }
});

sendBtn.addEventListener('click', () => {
    const text = queryInput.value.trim();
    if (text) {
        wakeTrinity();
        handleQuery(text);
        queryInput.value = '';
        sleepTrinity();
    }
});

/* ── INIT ── */
initSpeechRecognition();
setInterval(updateVisualState, 1500);

</script>
</body>
</html>"""
