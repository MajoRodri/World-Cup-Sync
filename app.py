# =============================================================================
# WORLD CUP SYNC 
# =============================================================================

import base64 as _b64mod
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.set_page_config(
    page_title="World Cup Sync | Analytics Platform",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paleta "Copa del Mundo" · Transmisión Oficial FIFA ───────────────────────
COLOR_RED   = "#E8002D"
COLOR_LIME  = "#CDFF00"   # Flash Lime — acento principal
COLOR_BLUE  = "#1565C0"   # Royal Blue corporativo
COLOR_WHITE = "#F8FAFC"   # Bone White — texto principal
COLOR_NAVY  = "#0D1321"   # Corporate Navy — fondo app
COLOR_STEEL = "#1D2436"   # Steel Blue — tarjetas y bloques
COLOR_MUTED = "#8899B0"   # Texto secundario/apagado
COLOR_TEXT  = "#C8D8E8"   # Cuerpo de texto

PLOT_BG  = "rgba(13,19,33,0.92)"
PAPER_BG = "rgba(0,0,0,0)"

STAGE_ORDER = ["Fase de Grupos", "Eliminatorias", "Cuartos de Final", "Semifinal", "Final"]

BASE_LAYOUT = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=PLOT_BG,
    font=dict(color=COLOR_TEXT, family="'Segoe UI', Arial, sans-serif"),
    margin=dict(t=60, b=45, l=15, r=15),
)

# ── Pre-compute slider ball SVG ──────────────────────────────────────────────
_BALL_B64 = _b64mod.b64encode(
    b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">'
    b'<text x="1" y="24" font-size="24">\xe2\x9a\xbd</text></svg>'
).decode()

# ── Logo ──────────────────────────────────────────────────────────────────────
try:
    with open("docs/LogoWorldCup.png", "rb") as _logo_f:
        _LOGO_SRC = f"data:image/png;base64,{_b64mod.b64encode(_logo_f.read()).decode()}"
except FileNotFoundError:
    _LOGO_SRC = None

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

/* ── Base ── */
.stApp {{
    background: radial-gradient(ellipse at 20% 0%, #142240 0%, {COLOR_NAVY} 40%, #090F1C 100%);
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
}}

/* ── Field grid overlay ── */
[data-testid="stMainBlockContainer"] {{
    background-image:
        linear-gradient(rgba(205,255,0,0.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(205,255,0,0.018) 1px, transparent 1px);
    background-size: 80px 80px;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #07090F 0%, {COLOR_NAVY} 100%);
    border-right: 1px solid {COLOR_LIME}22;
}}
[data-testid="stSidebar"] .stMarkdown p {{
    font-size: .82rem;
}}

/* ── Hero banner ── */
.wc-hero {{
    background: linear-gradient(135deg, #0E1E34 0%, #132650 45%, #0C162E 100%);
    border: 1px solid {COLOR_LIME}20;
    border-left: 4px solid {COLOR_LIME};
    border-radius: 14px;
    padding: 30px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.04);
}}
.wc-hero::after {{
    content: "⚽";
    position: absolute;
    right: 32px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 90px;
    opacity: 0.055;
    pointer-events: none;
}}
.wc-hero::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, {COLOR_LIME}, {COLOR_BLUE}, {COLOR_RED});
    border-radius: 14px 14px 0 0;
}}
.wc-hero-eyebrow {{
    font-size: .68rem;
    font-weight: 700;
    color: {COLOR_LIME};
    text-transform: uppercase;
    letter-spacing: 2.5px;
    margin: 0 0 6px 0;
}}
.wc-hero-title {{
    font-size: 1.65rem;
    font-weight: 900;
    color: {COLOR_WHITE};
    letter-spacing: -.3px;
    margin: 0 0 8px 0;
    line-height: 1.2;
}}
.wc-hero-sub {{
    color: {COLOR_MUTED};
    font-size: .84rem;
    margin: 0;
    line-height: 1.7;
}}
.wc-hero-pills {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
}}
.wc-pill {{
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .8px;
    text-transform: uppercase;
}}
.wc-pill-lime  {{ background:{COLOR_LIME}18; border:1px solid {COLOR_LIME}45; color:{COLOR_LIME}; }}
.wc-pill-red   {{ background:{COLOR_RED}18;  border:1px solid {COLOR_RED}45;  color:#FF6B8A; }}
.wc-pill-blue  {{ background:{COLOR_BLUE}22; border:1px solid {COLOR_BLUE}55; color:#6AB0E8; }}
.wc-pill-white {{ background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.2); color:{COLOR_WHITE}; }}

/* ── Question blocks ── */
.wc-q {{
    margin: 40px 0 0 0;
    padding: 22px 26px 20px;
    background: linear-gradient(90deg, {COLOR_LIME}06 0%, transparent 80%);
    border-left: 3px solid {COLOR_LIME};
    border-radius: 0 10px 10px 0;
    position: relative;
}}
.wc-q-red  {{ background: linear-gradient(90deg,{COLOR_RED}08 0%,transparent 80%); border-left-color:{COLOR_RED}; }}
.wc-q-blue {{ background: linear-gradient(90deg,{COLOR_BLUE}0A 0%,transparent 80%); border-left-color:{COLOR_BLUE}; }}
.wc-q-num {{
    font-size: 5rem;
    font-weight: 900;
    color: rgba(255,255,255,.04);
    position: absolute;
    right: 16px; top: -6px;
    line-height: 1;
    pointer-events: none;
    font-variant-numeric: tabular-nums;
}}
.wc-q-label {{
    font-size: .64rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: {COLOR_LIME};
    margin: 0 0 5px 0;
}}
.wc-q-label-red  {{ color:{COLOR_RED}; }}
.wc-q-label-blue {{ color:#6AB0E8; }}
.wc-q-text {{
    font-size: 1.22rem;
    font-weight: 800;
    color: {COLOR_WHITE};
    line-height: 1.35;
    margin: 0 0 5px 0;
}}
.wc-q-context {{
    font-size: .72rem;
    color: {COLOR_MUTED};
    letter-spacing: .3px;
    margin: 0;
}}

/* ── Insight cards ── */
.wc-insight {{
    background: {COLOR_LIME}07;
    border: 1px solid {COLOR_LIME}25;
    border-radius: 8px;
    padding: 11px 16px;
    margin: 6px 0 20px;
    font-size: .80rem;
    color: {COLOR_TEXT};
    line-height: 1.6;
}}
.wc-insight-red  {{ background:{COLOR_RED}08; border-color:{COLOR_RED}30; }}
.wc-insight-blue {{ background:{COLOR_BLUE}0A; border-color:{COLOR_BLUE}35; }}

/* ── KPI Cards ── */
.kpi-card {{
    background: linear-gradient(145deg, {COLOR_STEEL} 0%, #1B2A42 100%);
    border: 1px solid rgba(255,255,255,.06);
    border-top: 3px solid {COLOR_LIME};
    border-radius: 12px;
    padding: 18px 20px 16px;
    text-align: center;
    box-shadow: 0 6px 24px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.04);
    min-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    transition: transform .18s ease, box-shadow .18s ease;
}}
.kpi-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 36px {COLOR_LIME}1A, 0 4px 12px rgba(0,0,0,.5);
}}
.kpi-card-red   {{ border-top-color:{COLOR_RED}; }}
.kpi-card-red:hover   {{ box-shadow:0 12px 36px {COLOR_RED}18,0 4px 12px rgba(0,0,0,.5); }}
.kpi-card-blue  {{ border-top-color:{COLOR_BLUE}; }}
.kpi-card-blue:hover  {{ box-shadow:0 12px 36px {COLOR_BLUE}20,0 4px 12px rgba(0,0,0,.5); }}
.kpi-card-white {{ border-top-color:{COLOR_WHITE}; }}
.kpi-label      {{ font-size:.61rem; color:{COLOR_LIME}; font-weight:700;
                    text-transform:uppercase; letter-spacing:1.5px; line-height:1.4; }}
.kpi-label-red  {{ color:{COLOR_RED}; }}
.kpi-label-blue {{ color:#6AB0E8; }}
.kpi-label-white{{ color:{COLOR_WHITE}; }}
.kpi-value      {{ font-size:2.1rem; font-weight:900; color:{COLOR_WHITE}; line-height:1.05; }}
.kpi-sub        {{ font-size:.62rem; color:{COLOR_MUTED}; letter-spacing:.3px; }}

/* ── Edition cards ── */
.edition-card {{
    background: linear-gradient(135deg,{COLOR_STEEL} 0%,#162338 100%);
    border: 1px solid {COLOR_BLUE}35;
    border-top: 3px solid {COLOR_BLUE};
    border-radius: 10px;
    padding: 14px 16px;
    font-size: .82rem;
    line-height: 1.9;
    transition: transform .18s ease, border-color .18s ease;
}}
.edition-card:hover {{ transform:translateY(-2px); border-color:{COLOR_BLUE}70; }}
.edition-year {{ font-size:1.4rem; font-weight:900; color:{COLOR_LIME}; line-height:1.1; }}
.edition-host {{ font-size:.68rem; color:{COLOR_MUTED}; text-transform:uppercase;
                  letter-spacing:1px; margin-bottom:6px; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: rgba(29,36,54,0.7);
    border-radius: 10px;
    padding: 5px;
    gap: 3px;
    border: 1px solid rgba(255,255,255,.05);
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border-radius: 7px;
    color: {COLOR_MUTED};
    font-weight: 600;
    font-size: .84rem;
    padding: 8px 16px;
    transition: all .18s ease;
    border-bottom: none !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    background: rgba(205,255,0,.07);
    color: {COLOR_TEXT};
}}
.stTabs [aria-selected="true"] {{
    background: rgba(205,255,0,.12) !important;
    color: {COLOR_LIME} !important;
    box-shadow: 0 0 0 1px {COLOR_LIME}30;
}}

/* ── Slider: balón ── */
div[data-testid="stSlider"] div:has(> [role="slider"]),
div[data-testid="stSlider"] div:has(> [role="slider"]):focus,
div[data-testid="stSlider"] div:has(> [role="slider"]):active {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}}
div[data-testid="stSlider"] [role="slider"],
div[data-testid="stSlider"] [role="slider"]:focus,
div[data-testid="stSlider"] [role="slider"]:active,
div[data-testid="stSlider"] [role="slider"]:focus-visible {{
    background: transparent !important;
    background-image: url("data:image/svg+xml;base64,{_BALL_B64}") !important;
    background-size: 26px 26px !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    width: 28px !important;
    height: 28px !important;
    cursor: grab !important;
}}
div[data-testid="stSlider"] [role="slider"]:active {{ cursor: grabbing !important; }}
div[data-testid="stSlider"] [role="slider"] > * {{ display: none !important; }}
div[data-testid="stSlider"] > div > div > div > div:first-child > div {{
    background-color: #9EC500 !important;
}}
div[data-baseweb="slider"] > div:first-child > div:nth-child(2) {{
    background-color: #9EC500 !important;
}}

/* ── Misc ── */
hr {{ border-color:{COLOR_LIME}18 !important; }}
.stDataFrame {{ border-radius: 10px; overflow: hidden; }}

/* ── Storytelling / La Historia ── */
.story-hook-box {{
    text-align: center;
    padding: 36px 24px 24px;
    background: linear-gradient(135deg, #0E1E34 0%, #112444 50%, {COLOR_NAVY} 100%);
    border: 1px solid {COLOR_LIME}18;
    border-radius: 14px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}}
.story-hook-box::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, {COLOR_RED}, {COLOR_LIME}, {COLOR_BLUE});
    border-radius: 14px 14px 0 0;
}}
.story-hook-eyebrow {{
    font-size: .68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 2.5px; color: {COLOR_LIME}; margin: 0 0 10px 0;
}}
.story-hook-title {{
    font-size: 2.2rem; font-weight: 900; color: {COLOR_WHITE};
    line-height: 1.2; margin: 0 0 12px 0;
}}
.story-hook-body {{
    font-size: .92rem; color: {COLOR_MUTED}; line-height: 1.8;
    max-width: 680px; margin: 0 auto;
}}
.big-stat {{
    background: {COLOR_STEEL}; border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 22px 20px 18px; text-align: center; height: 100%;
}}
.big-stat-num {{
    font-size: 3.2rem; font-weight: 900; line-height: 1; margin: 0 0 4px 0;
}}
.big-stat-label {{
    font-size: .72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: {COLOR_MUTED}; margin: 0 0 8px 0;
}}
.big-stat-context {{
    font-size: .76rem; color: {COLOR_TEXT}; line-height: 1.5;
}}
.story-persona {{
    border-radius: 14px; padding: 22px 20px; height: 100%;
}}
.story-persona-role {{
    font-size: .65rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 2px; margin: 0 0 6px 0;
}}
.story-persona-name {{
    font-size: 1.05rem; font-weight: 800; color: {COLOR_WHITE};
    margin: 0 0 12px 0; line-height: 1.3;
}}
.story-persona-quote {{
    font-size: .80rem; color: {COLOR_MUTED}; line-height: 1.75;
    font-style: italic; border-left: 3px solid; padding-left: 12px; margin: 0;
}}
.story-ch {{
    margin: 44px 0 0 0; padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}}
.story-ch-number {{
    font-size: .65rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 3px; color: {COLOR_MUTED}; margin: 0 0 5px 0;
}}
.story-ch-title {{
    font-size: 1.4rem; font-weight: 900; color: {COLOR_WHITE};
    margin: 0; line-height: 1.2;
}}
.story-body {{
    font-size: .88rem; color: {COLOR_TEXT}; line-height: 1.95; margin: 16px 0;
}}
.story-plain {{
    background: rgba(205,255,0,0.04); border: 1px solid rgba(205,255,0,0.18);
    border-left: 4px solid {COLOR_LIME}; border-radius: 0 10px 10px 0;
    padding: 14px 20px; margin: 16px 0 20px 0;
    font-size: .83rem; color: {COLOR_TEXT}; line-height: 1.7;
}}
.story-exec {{
    background: rgba(21,101,192,0.07); border: 1px solid rgba(21,101,192,0.22);
    border-left: 4px solid {COLOR_BLUE}; border-radius: 0 10px 10px 0;
    padding: 14px 20px; margin: 16px 0 20px 0;
    font-size: .83rem; color: {COLOR_TEXT}; line-height: 1.7;
}}
.story-risk {{
    background: rgba(232,0,45,0.05); border: 1px solid rgba(232,0,45,0.22);
    border-left: 4px solid {COLOR_RED}; border-radius: 0 10px 10px 0;
    padding: 14px 20px; margin: 16px 0 10px 0;
    font-size: .83rem; color: {COLOR_TEXT}; line-height: 1.7;
}}
.story-action {{
    border-radius: 12px; padding: 22px 20px; height: 100%;
    border: 1px solid rgba(255,255,255,0.06); border-top: 3px solid;
}}
.story-action-num {{
    font-size: 2.5rem; font-weight: 900; opacity: 0.12;
    line-height: 1; margin: 0 0 -6px 0;
}}
.story-action-title {{
    font-size: .78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; margin: 0 0 10px 0;
}}
.story-action-body {{
    font-size: .82rem; color: {COLOR_TEXT}; line-height: 1.75; margin: 0;
}}

/* ══════════════════════════════════════════════════════════════
   glassmorphism, chart wrappers, sidebar
   ══════════════════════════════════════════════════════════════ */

/* ── Gradient animated top-border for hero on load ── */
@keyframes shimmer {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position:  200% center; }}
}}
.wc-hero::before {{
    background: linear-gradient(90deg,
        {COLOR_LIME}, {COLOR_BLUE}, {COLOR_RED}, {COLOR_LIME});
    background-size: 200% auto;
    animation: shimmer 4s linear infinite;
}}

/* ── Glassmorphism chart card ── */
.chart-card {{
    background: linear-gradient(145deg,
        rgba(29,36,54,0.85) 0%,
        rgba(13,19,33,0.70) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(205,255,0,0.10);
    border-radius: 14px;
    padding: 20px 20px 8px;
    margin-bottom: 18px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.45),
                inset 0 1px 0 rgba(255,255,255,0.04);
    transition: border-color .25s ease, box-shadow .25s ease;
}}
.chart-card:hover {{
    border-color: rgba(205,255,0,0.22);
    box-shadow: 0 12px 40px rgba(205,255,0,0.07),
                0 4px 16px rgba(0,0,0,0.5);
}}
.chart-card-title {{
    font-size: .68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 2px; color: {COLOR_LIME}; margin: 0 0 14px 0;
}}
.chart-card-blue  {{ border-color: rgba(21,101,192,0.20); }}
.chart-card-blue:hover {{ border-color: rgba(21,101,192,0.40);
    box-shadow: 0 12px 40px rgba(21,101,192,0.10), 0 4px 16px rgba(0,0,0,0.5); }}
.chart-card-red   {{ border-color: rgba(232,0,45,0.16); }}
.chart-card-red:hover {{ border-color: rgba(232,0,45,0.35);
    box-shadow: 0 12px 40px rgba(232,0,45,0.08), 0 4px 16px rgba(0,0,0,0.5); }}

/* ── Streamlit native container border=True override ── */
[data-testid="stVerticalBlockBorderWrapper"] > div {{
    background: linear-gradient(145deg,
        rgba(29,36,54,0.90) 0%,
        rgba(13,19,33,0.75) 100%) !important;
    border: 1px solid rgba(205,255,0,0.12) !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 24px rgba(0,0,0,0.4),
                inset 0 1px 0 rgba(255,255,255,0.03) !important;
}}

/* ── st.metric premium style ── */
[data-testid="stMetric"] {{
    background: linear-gradient(145deg, {COLOR_STEEL} 0%, #162338 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-top: 2px solid {COLOR_LIME};
    border-radius: 12px;
    padding: 16px 18px 14px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    transition: transform .18s ease, box-shadow .18s ease;
}}
[data-testid="stMetric"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(205,255,0,0.10), 0 4px 12px rgba(0,0,0,0.4);
}}
[data-testid="stMetricLabel"] > div {{
    font-size: .62rem !important; font-weight: 700 !important;
    text-transform: uppercase; letter-spacing: 1.5px;
    color: {COLOR_LIME} !important;
}}
[data-testid="stMetricValue"] > div {{
    font-size: 2rem !important; font-weight: 900 !important;
    color: {COLOR_WHITE} !important; line-height: 1.1;
}}
[data-testid="stMetricDelta"] > div {{
    font-size: .72rem !important;
}}

/* ── Sidebar: premium glass panel ── */
[data-testid="stSidebar"] > div:first-child {{
    background: linear-gradient(180deg,
        rgba(6,8,16,0.97) 0%,
        rgba(13,19,33,0.97) 100%) !important;
    border-right: 1px solid rgba(205,255,0,0.12) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.5);
}}
[data-testid="stSidebar"] .stSlider > div > div > div > div:first-child {{
    background: {COLOR_LIME}35 !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: rgba(29,36,54,0.9) !important;
    border-color: rgba(205,255,0,0.20) !important;
    border-radius: 8px !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {{
    border-color: {COLOR_LIME}55 !important;
}}
[data-testid="stSidebar"] [data-baseweb="tag"] {{
    background: rgba(205,255,0,0.12) !important;
    border: 1px solid rgba(205,255,0,0.28) !important;
    border-radius: 6px !important;
    color: {COLOR_LIME} !important;
    font-size: .70rem !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, rgba(205,255,0,0.10) 0%,
        rgba(205,255,0,0.06) 100%) !important;
    border: 1px solid rgba(205,255,0,0.30) !important;
    border-radius: 8px !important;
    color: {COLOR_LIME} !important;
    font-weight: 700 !important; font-size: .82rem !important;
    letter-spacing: .5px;
    padding: 8px 20px !important;
    transition: all .18s ease !important;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, rgba(205,255,0,0.18) 0%,
        rgba(205,255,0,0.10) 100%) !important;
    border-color: {COLOR_LIME}70 !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(205,255,0,0.15) !important;
}}
.stButton > button:active {{
    transform: translateY(0) !important;
}}

/* ── Multiselect / selectbox ── */
[data-baseweb="select"] > div {{
    background: rgba(29,36,54,0.90) !important;
    border-color: rgba(205,255,0,0.16) !important;
    border-radius: 9px !important;
    transition: border-color .18s ease;
}}
[data-baseweb="select"] > div:hover {{
    border-color: rgba(205,255,0,0.38) !important;
}}

/* ── Warning / info / error banners ── */
[data-testid="stAlert"] {{
    border-radius: 10px !important;
    border-left-width: 4px !important;
}}

/* ── Plotly chart container ── */
[data-testid="stPlotlyChart"] > div {{
    border-radius: 10px;
    overflow: hidden;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {COLOR_NAVY}; }}
::-webkit-scrollbar-thumb {{
    background: rgba(205,255,0,0.25); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{
    background: rgba(205,255,0,0.45); }}

/* ── Section divider ── */
.section-divider {{
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%, {COLOR_LIME}30 30%,
        {COLOR_LIME}30 70%, transparent 100%);
    margin: 32px 0;
    border: none;
}}

/* ── Gradient text utility ── */
.grad-text {{
    background: linear-gradient(90deg, {COLOR_LIME} 0%, #A8FF00 50%, {COLOR_WHITE} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.story-hook-box {{
    text-align: left;
    padding: 42px 44px 36px;
    background:
        linear-gradient(120deg, rgba(13,19,33,0.20), rgba(13,19,33,0.92) 58%),
        linear-gradient(135deg, rgba(21,101,192,0.28), rgba(232,0,45,0.12) 46%, rgba(255,199,44,0.12));
    border: 1px solid rgba(255,199,44,0.22);
    border-radius: 8px;
    box-shadow: 0 22px 70px rgba(0,0,0,0.46), inset 0 1px 0 rgba(255,255,255,0.06);
}}
.story-hook-box::after {{
    content: "";
    position: absolute;
    inset: 18px 18px auto auto;
    width: 132px;
    height: 132px;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 50%;
    background:
        linear-gradient(90deg, transparent 48%, rgba(255,255,255,0.08) 49%, rgba(255,255,255,0.08) 51%, transparent 52%),
        linear-gradient(0deg, transparent 48%, rgba(255,255,255,0.08) 49%, rgba(255,255,255,0.08) 51%, transparent 52%);
    opacity: 0.55;
}}
.story-hook-title {{
    max-width: 760px;
    font-size: clamp(2.05rem, 4vw, 3.45rem);
    letter-spacing: 0;
}}
.story-hook-body {{
    max-width: 760px;
    margin: 0;
    color: #D8E3F1;
}}
.story-section-label {{
    color: {COLOR_MUTED};
    font-size: .68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 12px 0 14px 0;
}}
.story-persona,
.big-stat,
.story-action,
.story-risk {{
    border-radius: 8px;
    box-shadow: 0 14px 34px rgba(0,0,0,0.30), inset 0 1px 0 rgba(255,255,255,0.04);
}}
.story-persona {{
    position: relative;
    overflow: hidden;
    min-height: 220px;
    border-left: 4px solid rgba(255,255,255,0.16);
}}
.story-persona::after {{
    content: "";
    position: absolute;
    inset: auto 18px 18px auto;
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: rgba(255,255,255,0.035);
}}
.story-persona-name {{
    font-size: 1.25rem;
}}
.story-persona-quote {{
    color: #D2DCEB;
}}
.big-stat {{
    background: linear-gradient(160deg, rgba(29,36,54,0.92), rgba(11,18,32,0.96));
    border: 1px solid rgba(255,255,255,0.08);
    padding: 24px 22px;
}}
.big-stat-num {{
    font-size: clamp(2.45rem, 5vw, 3.85rem);
}}
.story-ch {{
    display: grid;
    grid-template-columns: 86px 1fr;
    gap: 18px;
    align-items: start;
    margin: 56px 0 16px;
    padding: 0 0 18px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}}
.story-ch-number {{
    margin: 2px 0 0 0;
    color: {COLOR_LIME};
}}
.story-ch-title {{
    font-size: clamp(1.45rem, 2.6vw, 2.05rem);
    letter-spacing: 0;
}}
.story-body {{
    max-width: 980px;
    font-size: .96rem;
    color: #D8E3F1;
}}
.story-plain,
.story-exec,
.story-risk {{
    border-radius: 8px;
    padding: 16px 20px;
}}
.story-plain {{
    background: linear-gradient(135deg, rgba(255,199,44,0.08), rgba(255,199,44,0.025));
}}
.story-exec {{
    background: linear-gradient(135deg, rgba(21,101,192,0.12), rgba(21,101,192,0.035));
}}
.story-risk {{
    background: linear-gradient(135deg, rgba(232,0,45,0.11), rgba(232,0,45,0.03));
}}
.story-action {{
    min-height: 285px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}}
.story-action-title {{
    font-size: .84rem;
}}
.story-action-body {{
    color: #D8E3F1;
}}
.wc-hero {{
    border-radius: 8px;
    background:
        linear-gradient(120deg, rgba(8,14,26,0.86), rgba(15,33,61,0.86)),
        linear-gradient(90deg, rgba(232,0,45,0.10), rgba(255,199,44,0.08), rgba(21,101,192,0.12));
}}
.wc-pill {{
    border-radius: 999px;
}}
@media (max-width: 760px) {{
    .story-hook-box {{ padding: 30px 24px 26px; }}
    .story-hook-box::after {{ display: none; }}
    .story-ch {{ grid-template-columns: 1fr; gap: 4px; }}
    .story-action {{ min-height: auto; }}
}}

</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Cargando base de datos FIFA…")
def load_matches(path):
    df = pd.read_csv(path)
    df["year"]        = pd.to_numeric(df["year"],        errors="coerce")
    df["total_goals"] = pd.to_numeric(df["total_goals"], errors="coerce")
    df["attendance"]  = pd.to_numeric(df["attendance"],  errors="coerce")
    return df.dropna(subset=["year", "total_goals"])

@st.cache_data(show_spinner=False)
def load_wc(path):
    try:
        wc = pd.read_csv(path, encoding="latin-1")
        wc.columns = [c.strip() for c in wc.columns]
        wc["Year"] = pd.to_numeric(wc["Year"], errors="coerce")
        return wc.dropna(subset=["Year"])
    except Exception:
        return pd.DataFrame()

_DEMO_MODE = False
try:
    df_raw = load_matches("data/matches_limpio.csv")
except FileNotFoundError:
    from data.demo_data import make_matches_df, make_wc_df as _make_wc
    df_raw = make_matches_df()
    _DEMO_MODE = True

if _DEMO_MODE:
    from data.demo_data import make_wc_df as _make_wc
    wc_df = _make_wc()
else:
    wc_df = load_wc("data/world_cup.csv")

if _DEMO_MODE:
    st.info(
        "⚠️ **Modo Demo** — Los datos reales no están disponibles en este entorno. "
        "Se muestran datos sintéticos con el mismo esquema para fines de demostración.",
        icon="🔒",
    )


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if _LOGO_SRC:
        st.markdown(
            f"<div style='text-align:center;padding:12px 8px 4px;'>"
            f"<img src='{_LOGO_SRC}' style='width:82%;max-width:170px;"
            f"border-radius:12px;filter:drop-shadow(0 0 10px {COLOR_LIME}30);'/>"
            f"</div>"
            f"<p style='text-align:center;color:{COLOR_MUTED};font-size:.62rem;"
            f"letter-spacing:2.5px;margin:4px 0 0 0;text-transform:uppercase;'>"
            f"Analytics Platform</p>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<h2 style='color:{COLOR_LIME};text-align:center;letter-spacing:3px;"
            f"margin-bottom:2px;font-size:1.25rem;'>🏆 WORLD CUP</h2>"
            f"<p style='text-align:center;color:{COLOR_MUTED};font-size:.68rem;"
            f"letter-spacing:2px;margin-top:0;'>SYNC ANALYTICS · v4.0</p>",
            unsafe_allow_html=True,
        )
    st.markdown("---")

    st.markdown(
        f"<p style='color:{COLOR_LIME};font-size:.70rem;font-weight:700;"
        f"text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;'>"
        f"📅 Edición (Año)</p>", unsafe_allow_html=True,
    )
    yr_min, yr_max = int(df_raw["year"].min()), int(df_raw["year"].max())
    year_range = st.slider("Período", yr_min, yr_max, (yr_min, yr_max),
                           step=1, label_visibility="collapsed")
    st.markdown(
        f"<p style='text-align:center;color:{COLOR_WHITE};font-size:.95rem;font-weight:800;"
        f"letter-spacing:1px;margin:2px 0 0;line-height:1;'>"
        f"{year_range[0]}"
        f"<span style='color:{COLOR_LIME};margin:0 8px;'>—</span>"
        f"{year_range[1]}</p>",
        unsafe_allow_html=True,
    )
    n_total    = int(df_raw["year"].nunique())
    n_editions = int(df_raw.loc[df_raw["year"].between(*year_range), "year"].nunique())
    n_removed  = n_total - n_editions
    bar_pct    = int(n_editions / n_total * 100) if n_total else 100
    if n_removed == 0:
        removed_html = (
            f"<span style='color:{COLOR_LIME};font-weight:700;'>✔ todas incluidas</span>"
        )
    else:
        removed_html = (
            f"<span style='color:{COLOR_RED};font-weight:700;'>−{n_removed}</span>"
            f"<span style='color:{COLOR_MUTED};'> excluidas</span>"
        )
    st.markdown(
        f"""<div style='margin-top:4px;'>
          <div style='display:flex;justify-content:space-between;align-items:baseline;
                      font-size:.82rem;margin-bottom:3px;'>
            <span style='color:{COLOR_WHITE};font-weight:800;'>{n_editions}
              <span style='color:{COLOR_MUTED};font-weight:400;'>/ {n_total} ediciones</span>
            </span>
            {removed_html}
          </div>
          <div style='background:{COLOR_STEEL};border-radius:4px;height:5px;overflow:hidden;'>
            <div style='width:{bar_pct}%;height:100%;
                        background:linear-gradient(90deg,{COLOR_LIME},{COLOR_BLUE});
                        border-radius:4px;transition:width .15s ease;'></div>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:{COLOR_LIME};font-size:.70rem;font-weight:700;"
        f"text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;'>"
        f"🏅 Fase de Torneo</p>", unsafe_allow_html=True,
    )
    available_stages = sorted(df_raw["stage_clean"].dropna().unique().tolist())
    selected_stages  = st.multiselect("Fases", available_stages, available_stages,
                                      label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:{COLOR_LIME};font-size:.70rem;font-weight:700;"
        f"text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;'>"
        f"🌍 Equipo</p>", unsafe_allow_html=True,
    )
    all_teams     = sorted(set(df_raw["home_team"]) | set(df_raw["away_team"]))
    selected_team = st.selectbox("Equipo", ["— Todos —"] + all_teams,
                                 label_visibility="collapsed")
    team_active   = selected_team != "— Todos —"

    st.markdown("---")
    st.markdown(
        f"<p style='color:{COLOR_MUTED};font-size:.64rem;margin-top:12px;'>",
        unsafe_allow_html=True,
    )


# ── Reactive filter ───────────────────────────────────────────────────────────
if not selected_stages:
    st.warning("⚠️ Selecciona al menos una **Fase** en el panel lateral.")
    st.stop()

mask_team = (
    (df_raw["home_team"] == selected_team) | (df_raw["away_team"] == selected_team)
    if team_active else pd.Series(True, index=df_raw.index)
)
df = df_raw[
    df_raw["year"].between(*year_range) &
    df_raw["stage_clean"].isin(selected_stages) &
    mask_team
].copy()

if df.empty:
    st.warning("⚠️ Sin datos con los filtros actuales. Amplía el rango, fases o equipo.")
    st.stop()


# ── Hero banner ───────────────────────────────────────────────────────────────
stages_label = (", ".join(selected_stages) if len(selected_stages) <= 3
                else f"{len(selected_stages)} fases")
team_label   = (f"&nbsp;·&nbsp; <b style='color:{COLOR_LIME};'>{selected_team}</b>"
                if team_active else "")

_logo_html = (
    f"<div style='flex:0 0 auto;display:flex;align-items:center;justify-content:center;"
    f"padding:0 8px 0 0;'>"
    f"<img src='{_LOGO_SRC}' style='width:200px;border-radius:14px;"
    f"filter:drop-shadow(0 0 18px {COLOR_LIME}40) drop-shadow(0 0 6px rgba(0,0,0,0.6));'/>"
    f"</div>"
    if _LOGO_SRC else ""
)

st.markdown(
    f"""<div class="wc-hero" style="display:flex;align-items:center;gap:28px;flex-wrap:wrap;">
        {_logo_html}
        <div style="flex:1;min-width:260px;">
            <p class="wc-hero-eyebrow">FIFA World Cup 1930–2022 · Analytics Platform</p>
            <h1 class="wc-hero-title" style="margin-top:6px;">WORLD CUP SYNC</h1>
            <p class="wc-hero-sub">
                Inteligencia operativa para
                <b style="color:{COLOR_RED};">Streaming</b> y
                <b style="color:#6AB0E8;">Fan Zones Urbanas</b>
                &nbsp;·&nbsp; Ediciones
                <b style="color:{COLOR_WHITE};">{year_range[0]}–{year_range[1]}</b>
                &nbsp;·&nbsp; {stages_label}{team_label}
            </p>
<div class="wc-hero-pills">
                <span class="wc-pill wc-pill-lime">⚽ {len(df):,} partidos</span>
                <span class="wc-pill wc-pill-red">📺 Streaming</span>
                <span class="wc-pill wc-pill-blue">🌆 Fan Zones</span>
                <span class="wc-pill wc-pill-white">📅 {n_editions} ediciones</span>
            </div>
        </div>
    </div>""",
    unsafe_allow_html=True,
)


# ── KPI row ───────────────────────────────────────────────────────────────────
total_matches = len(df)
avg_goals     = df["total_goals"].mean()
att_df        = df.dropna(subset=["attendance"])

peak_att  = att_df["attendance"].max() if not att_df.empty else 0
peak_row  = att_df.loc[att_df["attendance"].idxmax()] if not att_df.empty else None
peak_fmt  = (f"{peak_att/1_000:.0f}K" if peak_att >= 100_000 else f"{peak_att:,.0f}")
peak_sub  = (f"{peak_row['home_team']} vs {peak_row['away_team']}, {int(peak_row['year'])}"
             if peak_row is not None else "")

max_g_row   = df.loc[df["total_goals"].idxmax()]
max_g_val   = int(max_g_row["total_goals"])
max_g_label = (f"{max_g_row['home_team']} {int(max_g_row['home_goals'])}–"
               f"{int(max_g_row['away_goals'])} {max_g_row['away_team']}")
max_g_year  = int(max_g_row["year"])

by_ed    = df.groupby("year")["total_goals"].mean()
best_yr  = int(by_ed.idxmax())
best_gpg = by_ed.max()

_, c1, _, c2, _, c3, _, c4, _, c5, _ = st.columns(
    [.01, 1, .03, 1, .03, 1, .03, 1, .03, 1, .01]
)
for col, card_cls, lbl_cls, icon, label, value, sub in [
    (c1, "",              "",               "⚽", "Partidos Analizados",    f"{total_matches:,}",    f"en {n_editions} ediciones"),
    (c2, "kpi-card-red",  "kpi-label-red",  "📺", "Espectáculo Digital",    f"{avg_goals:.2f}",      "goles/partido · predictor CDN"),
    (c3, "kpi-card-blue", "kpi-label-blue", "🏟️", "Pico de Afluencia",      peak_fmt,                peak_sub),
    (c4, "",              "",               "🔥", "Mayor Goleada Histórica", f"{max_g_val} goles",    f"{max_g_label} · {max_g_year}"),
    (c5, "kpi-card-white","kpi-label-white","🏅", "Edición Más Golera",     str(best_yr),            f"{best_gpg:.2f} g/p promedio"),
]:
    with col:
        st.markdown(
            f'<div class="kpi-card {card_cls}">'
            f'<div class="kpi-label {lbl_cls}">{icon} {label}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-sub">{sub}</div></div>',
            unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Pre-computations for storytelling ─────────────────────────────────────────
_df_mod  = df[df["year"] >= 2010]["total_goals"]
_df_hist = df[df["year"] <= 1966]["total_goals"]
era_modern     = float(_df_mod.mean())  if not _df_mod.empty  else avg_goals
era_historical = float(_df_hist.mean()) if not _df_hist.empty else avg_goals
pct_decline    = ((era_historical - era_modern) / era_historical * 100) if era_historical > 0 else 0

_att_all   = df.dropna(subset=["attendance"])["attendance"]
att_median = float(_att_all.median()) if not _att_all.empty else 0
att_p75    = float(_att_all.quantile(.75)) if not _att_all.empty else 0
att_p90    = float(_att_all.quantile(.90)) if not _att_all.empty else 0

_sagg_story = (df.groupby("stage_clean")
               .agg(avg_goals_st=("total_goals","mean"), avg_att_st=("attendance","mean"))
               .reset_index())
_final_row  = _sagg_story[_sagg_story["stage_clean"] == "Final"]
_grupos_row = _sagg_story[_sagg_story["stage_clean"] == "Fase de Grupos"]
final_avg_att  = float(_final_row["avg_att_st"].values[0])  if not _final_row.empty  else 0
grupos_avg_att = float(_grupos_row["avg_att_st"].values[0]) if not _grupos_row.empty else 1
att_multiplier = final_avg_att / grupos_avg_att if grupos_avg_att > 0 else 1
final_avg_goals  = float(_final_row["avg_goals_st"].values[0])  if not _final_row.empty  else 0
grupos_avg_goals = float(_grupos_row["avg_goals_st"].values[0]) if not _grupos_row.empty else 0


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  📊  Resumen Ejecutivo  ",
    "  🌆  Fan Zones y Venues  ",
    "  🏅  Análisis por Fase  ",
    "  🌍  Equipos  ",
    "  🔍  Match Explorer  ",
])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — RESUMEN EJECUTIVO
# ═════════════════════════════════════════════════════════════════════════════
with tab1:

    st.markdown(
        f'<div class="wc-q wc-q-red"><span class="wc-q-num">01</span>'
        f'<p class="wc-q-label wc-q-label-red">📺 Streaming · Planificación CDN y pauta premium</p>'
        f'<p class="wc-q-text">¿Cómo ha evolucionado el espectáculo goleador en 92 años de Mundial?</p>'
        f'<p class="wc-q-context">Goles promedio por partido · tendencia y campeones por edición</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    gby = (df.groupby("year")["total_goals"]
           .agg(["mean", "min", "max"]).reset_index().sort_values("year"))
    gby["rolling"] = gby["mean"].rolling(3, center=True, min_periods=1).mean()
    global_mean    = df["total_goals"].mean()

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=pd.concat([gby["year"], gby["year"].iloc[::-1]]),
        y=pd.concat([gby["max"],  gby["min"].iloc[::-1]]),
        fill="toself", fillcolor="rgba(255,199,44,0.07)",
        line=dict(color="rgba(0,0,0,0)"), name="Rango Mín–Máx", hoverinfo="skip",
    ))
    fig1.add_trace(go.Scatter(
        x=gby["year"], y=gby["mean"], name="Goles Promedio / Partido",
        mode="lines+markers",
        line=dict(color=COLOR_LIME, width=2.5),
        marker=dict(size=8, color=COLOR_LIME, line=dict(color=COLOR_NAVY, width=1.5)),
        fill="tozeroy", fillcolor="rgba(255,199,44,0.09)",
        hovertemplate="<b>Mundial %{x}</b><br>Promedio: %{y:.2f} g/p<extra></extra>",
    ))
    fig1.add_trace(go.Scatter(
        x=gby["year"], y=gby["rolling"], name="Tendencia MM-3",
        mode="lines", line=dict(color=COLOR_RED, width=2.5, dash="dot"),
        hovertemplate="Tendencia: %{y:.2f}<extra></extra>",
    ))
    fig1.add_hline(y=global_mean, line_dash="dash", line_color=COLOR_MUTED, opacity=0.4,
                   annotation_text=f"Media: {global_mean:.2f} g/p",
                   annotation_position="bottom right",
                   annotation_font=dict(color=COLOR_MUTED, size=10))

    if not wc_df.empty:
        for _, wc_row in wc_df.iterrows():
            yr  = int(wc_row["Year"])
            row = gby[gby["year"] == yr]
            if row.empty or not (year_range[0] <= yr <= year_range[1]):
                continue
            val  = float(row["mean"].values[0])
            chmp = str(wc_row.get("Champion", "")).strip()
            if chmp:
                fig1.add_annotation(
                    x=yr, y=val, text=f"🏆 {chmp}",
                    showarrow=True, arrowhead=2,
                    arrowcolor=COLOR_LIME, arrowwidth=1.2, ax=0, ay=-38,
                    font=dict(size=8, color=COLOR_LIME),
                    bgcolor="rgba(13,19,33,0.85)",
                    bordercolor=COLOR_LIME, borderwidth=0.8, borderpad=3,
                )

    fig1.update_layout(
        **BASE_LAYOUT,
        xaxis=dict(title="Edición del Mundial", showgrid=False,
                   tickfont=dict(size=10, color=COLOR_MUTED)),
        yaxis=dict(title="Goles Promedio por Partido",
                   showgrid=True, gridcolor="#1C2840", gridwidth=0.5,
                   tickfont=dict(size=10, color=COLOR_MUTED)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)", font=dict(color=COLOR_MUTED, size=10)),
        height=390, hovermode="x unified",
    )
    with st.container(border=True):
        st.plotly_chart(fig1, width="stretch")

    pico_yr = int(gby.loc[gby["mean"].idxmax(), "year"])
    pico_v  = gby["mean"].max()
    st.markdown(
        f'<div class="wc-insight wc-insight-red">📺 <b>Insight CDN:</b> La media del período es '
        f'<b>{global_mean:.2f} g/p</b>. El pico histórico fue <b>{pico_yr}</b> con '
        f'<b>{pico_v:.2f} g/p</b>. Ediciones anteriores a 1966 superan consistentemente '
        f'la media actual — considera filtrar 2010–2022 para proyecciones operativas.</div>',
        unsafe_allow_html=True,
    )

    # ── Edition context cards ─────────────────────────────────────────────────
    if not wc_df.empty:
        wc_period = (wc_df[wc_df["Year"].between(*year_range)]
                     .sort_values("Year", ascending=False))
        if not wc_period.empty:
            st.markdown(
                f'<div class="wc-q"><span class="wc-q-num">02</span>'
                f'<p class="wc-q-label">🏆 Inteligencia histórica · contenido y Fan Zone</p>'
                f'<p class="wc-q-text">¿Qué campeones, sedes y goleadores marcaron cada edición?</p>'
                f'<p class="wc-q-context">Contexto editorial para campañas de activación y experiencias inmersivas</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            rows = [wc_period.iloc[i:i+3] for i in range(0, len(wc_period), 3)]
            for chunk in rows:
                cols = st.columns(len(chunk))
                for col, (_, r) in zip(cols, chunk.iterrows()):
                    yr    = int(r["Year"])
                    host  = str(r.get("Host", "")).strip()
                    champ = str(r.get("Champion", "")).strip()
                    runup = str(r.get("Runner-Up", "")).strip()
                    scr   = (str(r.get("TopScorrer", ""))
                             .encode("ascii", "replace").decode()
                             .replace("??", "").strip())
                    att   = r.get("Attendance", 0)
                    mtch  = r.get("Matches", "?")
                    att_f = (f"{int(att)/1e6:.1f}M" if att >= 1_000_000
                             else f"{int(att):,}")
                    with col:
                        st.markdown(
                            f'<div class="edition-card">'
                            f'<div class="edition-year">{yr}</div>'
                            f'<div class="edition-host">📍 {host}</div>'
                            f'<div>🏆 <b style="color:{COLOR_LIME};">{champ}</b></div>'
                            f'<div>🥈 <span style="color:{COLOR_MUTED};">{runup}</span></div>'
                            f'<div>⚽ <span style="color:{COLOR_TEXT};font-size:.76rem;">{scr}</span></div>'
                            f'<div style="margin-top:8px;">'
                            f'<span class="wc-pill wc-pill-blue" style="font-size:.62rem;">{att_f} esp.</span>&nbsp;'
                            f'<span class="wc-pill wc-pill-lime" style="font-size:.62rem;">{mtch} partidos</span>'
                            f'</div></div>',
                            unsafe_allow_html=True,
                        )


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — FAN ZONES Y VENUES
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown(
            f'<div class="wc-q wc-q-blue"><span class="wc-q-num">01</span>'
            f'<p class="wc-q-label wc-q-label-blue">🌆 Fan Zones · Seguridad y logística</p>'
            f'<p class="wc-q-text">¿Qué ciudades concentran mayor presión de afluencia?</p>'
            f'<p class="wc-q-context">Top 12 sedes · dimensionamiento de accesos y zonas de servicio</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        city_df = (df.groupby("city")["attendance"]
                   .agg(["mean", "count", "max"]).reset_index()
                   .rename(columns={"mean": "avg", "count": "n", "max": "pk"})
                   .nlargest(12, "avg").sort_values("avg", ascending=True))
        n = len(city_df)
        bar_cols = [
            f"rgba({int(21+(255-21)*i/max(n-1,1))},"
            f"{int(101+(199-101)*i/max(n-1,1))},"
            f"{int(192+(44-192)*i/max(n-1,1))},0.88)"
            for i in range(n)
        ]
        fig2 = go.Figure(go.Bar(
            x=city_df["avg"], y=city_df["city"], orientation="h",
            marker=dict(color=bar_cols, line=dict(color=COLOR_NAVY, width=0.5)),
            customdata=np.column_stack([city_df["n"], city_df["pk"]]),
            hovertemplate=(
                "<b>%{y}</b><br>Afluencia promedio: <b>%{x:,.0f}</b><br>"
                "Partidos: %{customdata[0]}<br>Pico: %{customdata[1]:,.0f}<extra></extra>"
            ),
        ))
        fig2.update_layout(
            **BASE_LAYOUT,
            xaxis=dict(title="Afluencia Promedio", showgrid=True, gridcolor="#1C2840",
                       tickformat=",", tickfont=dict(size=9, color=COLOR_MUTED)),
            yaxis=dict(title="", tickfont=dict(size=10, color=COLOR_TEXT)),
            height=420, showlegend=False,
        )
        with st.container(border=True):
            st.plotly_chart(fig2, width="stretch")
        if not city_df.empty:
            top_city = city_df.iloc[-1]
            st.markdown(
                f'<div class="wc-insight wc-insight-blue">🌆 <b>Alerta Fan Zone:</b> '
                f'<b>{top_city["city"]}</b> encabeza con un promedio de '
                f'<b>{top_city["avg"]:,.0f}</b> espectadores y un pico de '
                f'<b>{top_city["pk"]:,.0f}</b>. Priorizar dimensionamiento de seguridad.</div>',
                unsafe_allow_html=True,
            )

    with col_r:
        st.markdown(
            f'<div class="wc-q wc-q-red"><span class="wc-q-num">02</span>'
            f'<p class="wc-q-label wc-q-label-red">📊 Probabilidad de saturación</p>'
            f'<p class="wc-q-text">¿Cuán probable es una saturación en streaming o Fan Zone?</p>'
            f'<p class="wc-q-context">Distribución estadística · percentiles P75 y P90 como umbrales operativos</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        tab_s, tab_f = st.tabs(["  📺  Streaming  ", "  🌆  Fan Zones  "])

        with tab_s:
            m_g  = df["total_goals"].mean(); std_g = df["total_goals"].std()
            q75g = df["total_goals"].quantile(.75); q90g = df["total_goals"].quantile(.90)
            psat = float((df["total_goals"] >= m_g + std_g).mean() * 100)
            fig3a = go.Figure(go.Histogram(
                x=df["total_goals"], nbinsx=18,
                marker=dict(color=COLOR_RED, opacity=.82,
                            line=dict(color=COLOR_NAVY, width=.8)),
                hovertemplate="Goles/partido: %{x}<br>Encuentros: %{y}<extra></extra>",
            ))
            for xv, lbl, col in [(m_g, f"Media: {m_g:.1f}", COLOR_WHITE),
                                  (q75g, f"P75: {q75g:.0f}", COLOR_MUTED),
                                  (q90g, f"P90: {q90g:.0f}", COLOR_LIME)]:
                fig3a.add_vline(x=xv, line_dash="dash", line_color=col, line_width=2,
                                annotation_text=lbl, annotation_position="top right",
                                annotation_font=dict(color=col, size=10))
            fig3a.update_layout(**BASE_LAYOUT,
                xaxis=dict(title="Goles por Partido", showgrid=False, dtick=1,
                           tickfont=dict(size=9, color=COLOR_MUTED)),
                yaxis=dict(title="Encuentros", showgrid=True, gridcolor="#1C2840",
                           tickfont=dict(size=10, color=COLOR_MUTED)),
                showlegend=False, height=300, bargap=.08)
            st.plotly_chart(fig3a, width="stretch")
            st.markdown(
                f'<div class="wc-insight wc-insight-red">📺 <b>{psat:.1f}%</b> de partidos '
                f'superan media+1σ ({m_g+std_g:.1f} g) → escenario de pico CDN.</div>',
                unsafe_allow_html=True)

        with tab_f:
            dfa = df.dropna(subset=["attendance"])
            m_a = dfa["attendance"].mean(); std_a = dfa["attendance"].std()
            q75a = dfa["attendance"].quantile(.75); q90a = dfa["attendance"].quantile(.90)
            psta = float((dfa["attendance"] >= q75a).mean() * 100)
            fig3b = go.Figure(go.Histogram(
                x=dfa["attendance"], nbinsx=22,
                marker=dict(color=COLOR_BLUE, opacity=.82,
                            line=dict(color=COLOR_NAVY, width=.8)),
                hovertemplate="Espectadores: %{x:,.0f}<br>Encuentros: %{y}<extra></extra>",
            ))
            for xv, lbl, col in [(m_a, f"Media: {m_a:,.0f}", COLOR_WHITE),
                                  (q75a, f"P75: {q75a:,.0f}", COLOR_MUTED),
                                  (q90a, f"P90: {q90a:,.0f}", COLOR_LIME)]:
                fig3b.add_vline(x=xv, line_dash="dash", line_color=col, line_width=2,
                                annotation_text=lbl, annotation_position="top right",
                                annotation_font=dict(color=col, size=10))
            fig3b.update_layout(**BASE_LAYOUT,
                xaxis=dict(title="Espectadores", showgrid=False, tickformat=",",
                           tickfont=dict(size=9, color=COLOR_MUTED)),
                yaxis=dict(title="Encuentros", showgrid=True, gridcolor="#1C2840",
                           tickfont=dict(size=10, color=COLOR_MUTED)),
                showlegend=False, height=300, bargap=.08)
            st.plotly_chart(fig3b, width="stretch")
            st.markdown(
                f'<div class="wc-insight wc-insight-blue">🌆 <b>{psta:.1f}%</b> de partidos '
                f'superan P75 ({q75a:,.0f} esp.) → umbral de alerta Fan Zone.</div>',
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f'<div class="wc-q wc-q-blue"><span class="wc-q-num">03</span>'
        f'<p class="wc-q-label wc-q-label-blue">🏟️ Infraestructura · Fan Zones de alta densidad</p>'
        f'<p class="wc-q-text">¿Qué estadios son los verdaderos templos del fútbol mundial?</p>'
        f'<p class="wc-q-context">Top 10 recintos por afluencia promedio · referencia para benchmarks de capacidad</p>'
        f'</div>',
        unsafe_allow_html=True,
    )
    stad = (df.dropna(subset=["attendance"])
            .groupby(["stadium", "city"])["attendance"]
            .agg(["mean", "count", "max"]).reset_index()
            .rename(columns={"mean": "avg", "count": "n", "max": "pk"})
            .nlargest(10, "avg").sort_values("avg", ascending=True))
    stad["label"] = stad["stadium"] + "  ·  " + stad["city"]
    fig_s = go.Figure(go.Bar(
        x=stad["avg"], y=stad["label"], orientation="h",
        marker=dict(color=stad["avg"],
                    colorscale=[[0, "#1D2436"], [.5, COLOR_BLUE], [1, COLOR_LIME]],
                    showscale=False, line=dict(color=COLOR_NAVY, width=.5)),
        customdata=np.column_stack([stad["n"], stad["pk"]]),
        hovertemplate=(
            "<b>%{y}</b><br>Promedio: %{x:,.0f}<br>"
            "Partidos: %{customdata[0]}<br>Récord: %{customdata[1]:,.0f}<extra></extra>"
        ),
        text=stad["avg"].apply(lambda v: f"{v/1000:.0f}K"),
        textposition="outside", textfont=dict(color=COLOR_MUTED, size=9),
    ))
    fig_s.update_layout(**BASE_LAYOUT,
        xaxis=dict(title="Afluencia Promedio", showgrid=True, gridcolor="#1C2840",
                   tickformat=",", tickfont=dict(size=9, color=COLOR_MUTED)),
        yaxis=dict(title="", tickfont=dict(size=9, color=COLOR_TEXT)),
        height=380, showlegend=False)
    st.plotly_chart(fig_s, width="stretch")


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANÁLISIS POR FASE
# ═════════════════════════════════════════════════════════════════════════════
with tab3:

    st.markdown(
        f'<div class="wc-q"><span class="wc-q-num">01</span>'
        f'<p class="wc-q-label">⚡ Riesgo simultáneo · saturación digital y logística</p>'
        f'<p class="wc-q-text">¿Qué fases del torneo generan más espectáculo y más público simultáneamente?</p>'
        f'<p class="wc-q-context">Goles promedio vs. afluencia promedio por fase · eje dual</p>'
        f'</div>',
        unsafe_allow_html=True,
    )
    sagg = (df.groupby("stage_clean")
            .agg(avg_goals=("total_goals","mean"), avg_att=("attendance","mean"),
                 n=("total_goals","count")).reset_index())
    sagg["_o"] = sagg["stage_clean"].map({s: i for i, s in enumerate(STAGE_ORDER)}).fillna(99)
    sagg = sagg.sort_values("_o")

    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Bar(
        x=sagg["stage_clean"], y=sagg["avg_goals"], name="Goles Promedio",
        marker=dict(color=sagg["avg_goals"],
                    colorscale=[[0,"#1D2436"],[.5,COLOR_LIME],[1,"#FFE090"]],
                    showscale=False, line=dict(color=COLOR_NAVY, width=.8)),
        text=sagg["avg_goals"].apply(lambda v: f"{v:.2f}"), textposition="outside",
        customdata=sagg["n"],
        hovertemplate="<b>%{x}</b><br>Goles prom: %{y:.2f}<br>Partidos: %{customdata}<extra></extra>",
    ), secondary_y=False)
    fig4.add_trace(go.Scatter(
        x=sagg["stage_clean"], y=sagg["avg_att"], name="Afluencia Promedio",
        mode="lines+markers",
        line=dict(color=COLOR_BLUE, width=2.5),
        marker=dict(size=12, color=COLOR_BLUE, symbol="diamond",
                    line=dict(color=COLOR_NAVY, width=1.5)),
        hovertemplate="<b>%{x}</b><br>Afluencia prom: %{y:,.0f}<extra></extra>",
    ), secondary_y=True)
    fig4.update_layout(**BASE_LAYOUT,
        xaxis=dict(title="Fase de Torneo", showgrid=False,
                   tickfont=dict(size=11, color=COLOR_TEXT)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)", font=dict(color=COLOR_MUTED, size=10)),
        height=400, barmode="group")
    fig4.update_yaxes(title_text="Goles Promedio", secondary_y=False,
                      showgrid=True, gridcolor="#1C2840",
                      tickfont=dict(color=COLOR_LIME), title_font=dict(color=COLOR_LIME))
    fig4.update_yaxes(title_text="Afluencia Promedio", secondary_y=True,
                      showgrid=False, tickformat=",",
                      tickfont=dict(color=COLOR_BLUE), title_font=dict(color=COLOR_BLUE))
    st.plotly_chart(fig4, width="stretch")

    if not sagg.empty:
        fase_max_g = sagg.loc[sagg["avg_goals"].idxmax(), "stage_clean"]
        fase_max_a = sagg.dropna(subset=["avg_att"]).loc[sagg.dropna(subset=["avg_att"])["avg_att"].idxmax(), "stage_clean"] if sagg["avg_att"].notna().any() else "—"
        st.markdown(
            f'<div class="wc-insight">⚡ <b>Mayor espectáculo goleador:</b> <b>{fase_max_g}</b> · '
            f'<b>Mayor presión de afluencia:</b> <b>{fase_max_a}</b>. '
            f'Cuando coinciden en la misma jornada, el riesgo de saturación simultánea es máximo.</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="wc-q wc-q-red"><span class="wc-q-num">02</span>'
        f'<p class="wc-q-label wc-q-label-red">🗺️ Mapa de calor · pauta publicitaria premium</p>'
        f'<p class="wc-q-text">¿En qué año y fase se concentró el mayor rendimiento goleador?</p>'
        f'<p class="wc-q-context">Combinaciones edición × fase con mayor potencial de espectáculo</p>'
        f'</div>',
        unsafe_allow_html=True,
    )
    pivot = df.pivot_table(values="total_goals", index="year",
                           columns="stage_clean", aggfunc="mean").round(2)
    pivot_cols = [c for c in STAGE_ORDER if c in pivot.columns]
    pivot = pivot[pivot_cols]

    fig_heat = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0,"#0D1321"],[.35,COLOR_BLUE],[.70,COLOR_LIME],[1,COLOR_RED]],
        text=[[f"{v:.1f}" if not np.isnan(v) else "—" for v in row]
              for row in pivot.values],
        texttemplate="%{text}", textfont=dict(size=10, color="#F8FAFC"),
        hovertemplate="<b>%{y} · %{x}</b><br>Goles promedio: %{z:.2f}<extra></extra>",
        showscale=True,
        colorbar=dict(title=dict(text="g/p", font=dict(color=COLOR_MUTED, size=10)),
                      tickfont=dict(color=COLOR_MUTED, size=9), thickness=12),
    ))
    fig_heat.update_layout(**BASE_LAYOUT,
        xaxis=dict(title="Fase", showgrid=False, tickfont=dict(size=10, color=COLOR_TEXT)),
        yaxis=dict(title="Edición", showgrid=False,
                   tickfont=dict(size=9, color=COLOR_MUTED), autorange="reversed"),
        height=max(320, min(700, len(pivot) * 22 + 100)))
    st.plotly_chart(fig_heat, width="stretch")


# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — EQUIPOS
# ═════════════════════════════════════════════════════════════════════════════
with tab4:
    hs  = df[["year","home_team","home_goals","away_goals"]].copy()
    hs.columns = ["year","team","scored","conceded"]
    aws = df[["year","away_team","away_goals","home_goals"]].copy()
    aws.columns = ["year","team","scored","conceded"]
    tall = pd.concat([hs, aws])
    tall["win"]  = tall["scored"] > tall["conceded"]
    tall["draw"] = tall["scored"] == tall["conceded"]
    tall["loss"] = tall["scored"] < tall["conceded"]

    tagg = (tall.groupby("team").agg(
        partidos=("scored","count"), gf=("scored","sum"), gc=("conceded","sum"),
        avg_gf=("scored","mean"), avg_gc=("conceded","mean"),
        victorias=("win","sum"), empates=("draw","sum"), derrotas=("loss","sum"),
    ).reset_index())
    tagg["diff"]    = tagg["gf"] - tagg["gc"]
    tagg["win_pct"] = (tagg["victorias"] / tagg["partidos"] * 100).round(1)

    min_p  = max(3, len(df) // 80)
    tfilt  = tagg[tagg["partidos"] >= min_p]

    if tfilt.empty:
        st.info(f"Amplía los filtros para ver estadísticas de equipos (mín. {min_p} partidos).")
    else:
        cl, cr = st.columns([3, 2], gap="large")

        with cl:
            st.markdown(
                f'<div class="wc-q"><span class="wc-q-num">01</span>'
                f'<p class="wc-q-label">🥇 Ranking ofensivo histórico</p>'
                f'<p class="wc-q-text">¿Qué selecciones han dominado el ataque en el Mundial?</p>'
                f'<p class="wc-q-context">Top 15 · goles anotados por partido · mín. {min_p} encuentros en el período</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            top15 = tfilt.nlargest(15, "avg_gf").sort_values("avg_gf", ascending=True)
            q80 = top15["avg_gf"].quantile(.80); q50 = top15["avg_gf"].quantile(.50)
            bc  = [COLOR_LIME if v >= q80 else COLOR_RED if v >= q50 else COLOR_BLUE
                   for v in top15["avg_gf"]]
            fig_t = go.Figure(go.Bar(
                x=top15["avg_gf"], y=top15["team"], orientation="h",
                marker=dict(color=bc, line=dict(color=COLOR_NAVY, width=.5)),
                customdata=np.column_stack([top15["partidos"], top15["gf"],
                                            top15["win_pct"], top15["diff"]]),
                hovertemplate=(
                    "<b>%{y}</b><br>Goles/partido: <b>%{x:.2f}</b><br>"
                    "Partidos: %{customdata[0]}<br>Total GF: %{customdata[1]}<br>"
                    "% Victorias: %{customdata[2]:.1f}%<br>"
                    "Dif. goles: %{customdata[3]:+d}<extra></extra>"
                ),
                text=top15["avg_gf"].apply(lambda v: f"{v:.2f}"),
                textposition="outside", textfont=dict(color=COLOR_MUTED, size=9),
            ))
            fig_t.update_layout(**BASE_LAYOUT,
                xaxis=dict(title="Goles Anotados / Partido", showgrid=True,
                           gridcolor="#1C2840", tickfont=dict(size=9, color=COLOR_MUTED)),
                yaxis=dict(title="", tickfont=dict(size=10, color=COLOR_TEXT)),
                height=480, showlegend=False)
            st.plotly_chart(fig_t, width="stretch")
            best_team = top15.iloc[-1]
            st.markdown(
                f'<div class="wc-insight">🥇 Líder ofensivo: <b>{best_team["team"]}</b> con '
                f'<b>{best_team["avg_gf"]:.2f} g/p</b> en {int(best_team["partidos"])} partidos · '
                f'<b>{best_team["win_pct"]:.0f}% de victorias</b>.</div>',
                unsafe_allow_html=True,
            )

        with cr:
            st.markdown(
                f'<div class="wc-q wc-q-red"><span class="wc-q-num">02</span>'
                f'<p class="wc-q-label wc-q-label-red">⚔️ Posicionamiento táctico histórico</p>'
                f'<p class="wc-q-text">¿Cómo se posicionan las selecciones entre ataque y defensa?</p>'
                f'<p class="wc-q-context">Ataque vs. Defensa · tamaño = partidos jugados · color = diferencia de goles</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            mx = tfilt["partidos"].clip(upper=80).max()
            fig_sc = go.Figure()
            fig_sc.add_hline(y=tfilt["avg_gc"].median(), line_dash="dot",
                             line_color=COLOR_MUTED, opacity=.3)
            fig_sc.add_vline(x=tfilt["avg_gf"].median(), line_dash="dot",
                             line_color=COLOR_MUTED, opacity=.3)
            fig_sc.add_trace(go.Scatter(
                x=tfilt["avg_gf"], y=tfilt["avg_gc"],
                mode="markers+text",
                marker=dict(
                    size=tfilt["partidos"].clip(upper=80) / mx * 30 + 6,
                    color=tfilt["diff"],
                    colorscale=[[0,COLOR_RED],[.5,COLOR_BLUE],[1,COLOR_LIME]],
                    cmid=0, showscale=True,
                    colorbar=dict(title=dict(text="Dif.",
                                            font=dict(color=COLOR_MUTED, size=9)),
                                  tickfont=dict(color=COLOR_MUTED, size=8),
                                  thickness=10, x=1.02),
                    line=dict(color=COLOR_NAVY, width=1),
                ),
                text=tfilt["team"],
                textposition="top center",
                textfont=dict(size=7, color=COLOR_MUTED),
                customdata=np.column_stack([tfilt["partidos"], tfilt["win_pct"], tfilt["diff"]]),
                hovertemplate=(
                    "<b>%{text}</b><br>GF/PJ: %{x:.2f}<br>GC/PJ: %{y:.2f}<br>"
                    "Partidos: %{customdata[0]}<br>% Vict.: %{customdata[1]:.1f}%<br>"
                    "Dif: %{customdata[2]:+d}<extra></extra>"
                ),
            ))
            fig_sc.update_layout(**BASE_LAYOUT,
                xaxis=dict(title="Goles Anotados / Partido",
                           showgrid=True, gridcolor="#1C2840",
                           tickfont=dict(size=9, color=COLOR_MUTED)),
                yaxis=dict(title="Goles Recibidos / Partido",
                           showgrid=True, gridcolor="#1C2840",
                           tickfont=dict(size=9, color=COLOR_MUTED)),
                height=480, showlegend=False)
            st.plotly_chart(fig_sc, width="stretch")

        st.markdown(
            f'<div class="wc-q"><span class="wc-q-num">03</span>'
            f'<p class="wc-q-label">📋 Tabla completa de rendimiento</p>'
            f'<p class="wc-q-text">Ranking completo — todos los indicadores por selección</p>'
            f'<p class="wc-q-context">Ordenable por columna · solo equipos con ≥{min_p} partidos en el período</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        disp = (tfilt[["team","partidos","victorias","empates","derrotas",
                        "gf","gc","diff","avg_gf","avg_gc","win_pct"]]
                .sort_values("avg_gf", ascending=False)
                .rename(columns={"team":"Equipo","partidos":"PJ",
                                  "victorias":"G","empates":"E","derrotas":"P",
                                  "gf":"GF","gc":"GC","diff":"+/-",
                                  "avg_gf":"GF/PJ","avg_gc":"GC/PJ","win_pct":"% Vict."}))
        disp["GF/PJ"] = disp["GF/PJ"].round(2)
        disp["GC/PJ"] = disp["GC/PJ"].round(2)
        st.dataframe(disp, width="stretch", height=320, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 5 — MATCH EXPLORER
# ═════════════════════════════════════════════════════════════════════════════
with tab5:

    st.markdown(
        f'<div class="wc-q"><span class="wc-q-num">01</span>'
        f'<p class="wc-q-label">🔍 Base de datos histórica · análisis individual</p>'
        f'<p class="wc-q-text">¿Cuál fue el partido más memorable de la historia del Mundial?</p>'
        f'<p class="wc-q-context">Filtra por goles, afluencia y ordenación para encontrar los partidos que definieron una era</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        fe_min_g = st.number_input("Goles mínimos", 0, int(df["total_goals"].max()), 0, 1)
    with fc2:
        fe_min_a = st.number_input("Afluencia mínima", 0, int(df["attendance"].max()), 0, 10000)
    with fc3:
        fe_sort = st.selectbox("Ordenar por", [
            "Año (reciente)", "Goles (más goles)", "Afluencia (mayor)", "Año (antiguo)"
        ])

    edf = df[(df["total_goals"] >= fe_min_g) & (df["attendance"] >= fe_min_a)].copy()
    sort_map = {"Año (reciente)": ("year", False), "Goles (más goles)": ("total_goals", False),
                "Afluencia (mayor)": ("attendance", False), "Año (antiguo)": ("year", True)}
    sc, sa = sort_map[fe_sort]
    edf = edf.sort_values(sc, ascending=sa)

    edf["Resultado"]  = (edf["home_goals"].astype(int).astype(str) + " – " +
                         edf["away_goals"].astype(int).astype(str))
    edf["Asistencia"] = edf["attendance"].apply(
        lambda v: f"{int(v):,}" if pd.notna(v) else "—")

    show = edf[["year","stage_clean","home_team","Resultado","away_team",
                "total_goals","Asistencia","city","stadium"]].rename(columns={
        "year":"Año","stage_clean":"Fase","home_team":"Local",
        "away_team":"Visitante","total_goals":"Goles",
        "city":"Ciudad","stadium":"Estadio",
    })

    st.markdown(
        f'<span class="wc-pill wc-pill-lime">{len(show):,} partidos encontrados</span>',
        unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(show, width="stretch", height=500, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
# ── Governance ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f'<div style="background:{COLOR_STEEL};border:1px solid {COLOR_RED}30;border-left:3px solid {COLOR_RED};'
    f'border-radius:8px;padding:14px 20px;margin:8px 0;">'
    f'<p style="color:{COLOR_RED};font-size:.65rem;font-weight:700;text-transform:uppercase;'
    f'letter-spacing:1.5px;margin:0 0 4px 0;">⚠️ Nota de Gobernanza · Sesgo de Época</p>'
    f'<p style="color:{COLOR_TEXT};font-size:.78rem;line-height:1.7;margin:0;">'
    f'Este cuadro abarca <b>92 años de competencia FIFA (1930–2022)</b>. Los promedios históricos '
    f'<b>no deben usarse directamente como insumo operativo</b> sin filtrar por período reciente '
    f'(2010–2022). Aforos pre-1970 carecen de metodología verificable — aplica el filtro de año '
    f'en el panel lateral antes de comprometer presupuestos o dimensionar infraestructura.</p>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"<p style='text-align:center;color:{COLOR_MUTED};font-size:.68rem;line-height:2;'>"
    f"🏆 <b style='color:{COLOR_TEXT};'>World Cup Sync Analytics Platform</b>"
    f"&nbsp;·&nbsp;Fuente: FIFA / Kaggle (piterfm)&nbsp"
    f"&nbsp;·&nbsp;<b>USO INTERNO — CONFIDENCIAL</b></p>",
    unsafe_allow_html=True,
)
