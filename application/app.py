try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

import requests as _requests
import json

GEMINI_SYSTEM_PROMPT = """You are the C-Suite Chief Decarbonization & Financial Engineering AI Specialist for the NYC Local Law 97 Carbon Heist Mitigation Platform.
You speak both English and Arabic fluently and professionally based on the language of the user query.
Your comprehensive knowledge base covers:
1. 11,639 audited commercial and residential properties across New York City's 5 boroughs.
2. Borough Breakdown of Properties, Annual CO2e Emissions, and Statutory Liability ($268/MT CO2e):
   - Manhattan: 4,821 properties (41.4%) | 4,963,059 MT CO2e/year | $1.33 Billion/year unmitigated fine exposure.
   - Brooklyn: 3,142 properties (27.0%) | 2,428,731 MT CO2e/year | $650.9 Million/year unmitigated fine exposure.
   - Queens: 2,211 properties (19.0%) | 1,900,746 MT CO2e/year | $509.4 Million/year unmitigated fine exposure.
   - Bronx: 1,164 properties (10.0%) | 950,373 MT CO2e/year | $254.7 Million/year unmitigated fine exposure.
   - Staten Island: 301 properties (2.6%) | 316,791 MT CO2e/year | $84.9 Million/year unmitigated fine exposure.
   - Total Portfolio: 11,639 properties | 10,559,701.49 MT CO2e/year | $2.83 Billion/year statutory penalty.
3. Building Archetype / Sector Liability Distribution:
   - Commercial Office & Retail: 45% of total carbon liability.
   - Multifamily Residential (Pre-1974 & Modern): 38% of total carbon liability.
   - Institutional / Hospitality / Healthcare: 17% of total carbon liability.
4. Financial Engineering & Playbook Execution Summary:
   - Total Portfolio CAPEX: $4.98 Billion across 5 Playbooks.
   - Gross Annual Savings: $656.63 Million/yr | Itemized Annual OPEX: $15.70 Million/yr | Net Recurring Operational Annual Cash Flow: $640.93 Million/yr.
   - Blended Portfolio Payback Period: Exactly 7.58 Years.
5. The 5 Decarbonization Playbooks:
   - Playbook 01 (Surgical Strike): Level 2 energy audits & BMS setback scheduling across Top 10 offenders -> $500K CAPEX -> $20.55M/yr Net Cash Flow -> 8-Day Payback (0.02 yrs).
   - Playbook 02 (Retro-commissioning): Comprehensive RCx & DDC upgrades -> $802.17M CAPEX -> $240.37M/yr Net Cash Flow -> 3.29-Year Payback.
   - Playbook 03 (1960s Smart Scale): LED lighting & VFD motor retrofits -> $785.24M CAPEX -> $85.23M/yr Net Cash Flow -> 8.92-Year Payback.
   - Playbook 04 (1930s WET Systems): Historic sewer wastewater heat recovery leveraging 50% PPP Grants -> $1.50B Net CAPEX -> $117.89M/yr Net Cash Flow -> 12.25-Year Payback.
   - Playbook 05 (Electrification Push): Replacing Fuel Oil #4 boilers with Electric Heat Pumps -> $1.89B CAPEX -> $176.89M/yr Net Cash Flow -> 10.38-Year Payback.

UNIVERSAL DYNAMIC CHART GENERATION CAPABILITY:
Whenever the user asks for ANY chart, graph, plot, visual comparison, or asks an analytical question where a chart would enhance executive decision-making, provide a thorough executive analysis AND append a JSON block formatted exactly like this at the very end of your response:
```plotly_json
{
  "title": "Clear Chart Title",
  "chart_type": "bar",
  "x": ["Category A", "Category B", "Category C"],
  "y": [100, 250, 400],
  "x_label": "X Axis Title",
  "y_label": "Y Axis Title"
}
```
Supported chart_type values: "bar" (vertical bar chart), "hbar" (horizontal bar chart), "pie" (donut chart), "line" (line chart).
Always make sure the JSON inside ```plotly_json ... ``` is valid JSON. Our platform will automatically parse it and render a stunning interactive Plotly chart directly below your text!
If asked in Arabic, respond in sophisticated executive Arabic and generate the chart labels in Arabic as well."""

def call_gemini_ai(prompt_text, api_key, system_instruction=""):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt_text}]}
        ]
    }
    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }
    resp = _requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    res_json = resp.json()
    return res_json["candidates"][0]["content"]["parts"][0]["text"]

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import os
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG · NYC LL97 Decarbonization Intelligence Platform v2.83B
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Carbon Heist Mitigation · ESG Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ──────────────────────────────────────────────────────────────
C_CYAN   = "#00D2FF"
C_BLUE   = "#3B82F6"
C_GREEN  = "#00F59B"
C_RED    = "#FF4B6E"
C_AMBER  = "#FFB800"
C_PURPLE = "#A855F7"
C_BG     = "#060b18"
C_CARD   = "#0d1526"
C_BORDER = "rgba(255,255,255,0.07)"

with st.sidebar:
    IS_LIGHT = st.toggle("☀️ Light Mode", value=False, key="light_mode")

PANEL_BG = "#ffffff" if IS_LIGHT else "rgba(13,21,38,0.9)"
TEXT_MAIN = "#0f172a" if IS_LIGHT else "#ffffff"
TEXT_SUB = "#334155" if IS_LIGHT else "#94a3b8"
TEXT_MUTED = "#64748b"
INPUT_BG = "#f9fafb" if IS_LIGHT else "rgba(13,21,38,0.9)"

# ──────────────────────────────────────────────────────────────
# GLOBAL STYLES
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── ROOT ── */
html, body, .stApp {{
    font-family: 'Inter', sans-serif;
    background: {C_BG};
    color: #e2e8f0;
}}
.stApp {{
    background: radial-gradient(ellipse at 0% 0%, rgba(0,210,255,0.05) 0%, transparent 60%),
                radial-gradient(ellipse at 100% 100%, rgba(168,85,247,0.05) 0%, transparent 60%),
                {C_BG};
}}

/* ── STREAMLIT CHROME & SIDEBAR TOGGLE ── */
#MainMenu, footer {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}
[data-testid="stHeader"] {{
    background: transparent !important;
}}
[data-testid="collapsedControl"] {{
    display: flex !important;
    visibility: visible !important;
    color: {C_CYAN} !important;
    background: {PANEL_BG} !important;
    border: 1px solid {C_BORDER} !important;
    border-radius: 8px !important;
    padding: 4px !important;
    z-index: 999999 !important;
}}

/* ── TYPOGRAPHY ── */
h1 {{
    font-size: 2rem !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, {C_CYAN}, {C_PURPLE}, {C_GREEN}) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: -0.03em;
    margin-bottom: 0.25rem !important;
}}
h2 {{ font-size: 1.35rem !important; font-weight: 700 !important; color: #ffffff !important; letter-spacing: -0.02em; }}
h3 {{ font-size: 1.1rem  !important; font-weight: 600 !important; color: #e2e8f0 !important; }}
h4 {{ font-size: 0.95rem !important; font-weight: 600 !important; color: #94a3b8 !important; }}
p  {{ color: #cbd5e1; line-height: 1.75; font-size: 0.93rem; }}
b, strong {{ color: #ffffff !important; }}

/* ── SECTION HEADER PILL ── */
.section-pill {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: linear-gradient(135deg, rgba(0,210,255,0.12), rgba(168,85,247,0.08));
    border: 1px solid rgba(0,210,255,0.2);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    font-size: 0.78rem;
    font-weight: 700;
    color: {C_CYAN};
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}}

/* ── KPI GRID ── */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 0.85rem;
    margin-bottom: 1.75rem;
}}
.kpi-card {{
    background: linear-gradient(145deg, rgba(13,21,38,0.95), rgba(13,21,38,0.75));
    border: 1px solid {C_BORDER};
    border-top: 2px solid {C_CYAN};
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}}
.kpi-card::before {{
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(0,210,255,0.03), transparent);
    border-radius: 14px;
}}
.kpi-card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 28px rgba(0,210,255,0.1); }}
.kpi-card.red  {{ border-top-color: {C_RED};    }}
.kpi-card.red:hover  {{ box-shadow: 0 12px 28px rgba(255,75,110,0.12); }}
.kpi-card.green {{ border-top-color: {C_GREEN}; }}
.kpi-card.green:hover {{ box-shadow: 0 12px 28px rgba(0,245,155,0.12); }}
.kpi-card.amber {{ border-top-color: {C_AMBER}; }}
.kpi-card.purple {{ border-top-color: {C_PURPLE}; }}
.kpi-label {{
    font-size: 0.68rem; font-weight: 600; color: #475569;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.4rem;
}}
.kpi-val {{
    font-size: 1.45rem; font-weight: 700; color: #ffffff;
    letter-spacing: -0.02em; line-height: 1.25;
}}
.kpi-sub {{ font-size: 0.75rem; color: #64748b; margin-top: 0.2rem; }}

/* ── GLASS PANELS ── */
.glass-panel {{
    background: linear-gradient(145deg, rgba(13,21,38,0.9), rgba(13,21,38,0.6));
    border: 1px solid {C_BORDER};
    border-left: 3px solid {C_CYAN};
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 1.25rem;
}}
.glass-panel.green {{ border-left-color: {C_GREEN}; }}
.glass-panel.amber {{ border-left-color: {C_AMBER}; }}
.glass-panel h3, .glass-panel h4 {{ color: #ffffff !important; }}

/* ── DIVIDER ── */
.section-div {{
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,210,255,0.15), rgba(168,85,247,0.15), transparent);
    margin: 2rem 0;
    border: none;
}}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {{
    background: rgba(13,21,38,0.7);
    backdrop-filter: blur(12px);
    border: 1px solid {C_BORDER};
    border-radius: 14px;
    padding: 5px;
    gap: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px;
    padding: 9px 16px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #475569;
    transition: all 0.25s;
}}
.stTabs [data-baseweb="tab"]:hover {{ color: #94a3b8; background: rgba(255,255,255,0.03); }}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, rgba(0,210,255,0.15), rgba(168,85,247,0.1)) !important;
    color: {C_CYAN} !important;
    box-shadow: 0 0 16px rgba(0,210,255,0.08);
}}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #080f20 0%, #060b18 100%) !important;
    border-right: 1px solid {C_BORDER};
}}
[data-testid="stSidebar"] .stMarkdown p {{ font-size: 0.8rem; color: #475569; }}

/* ── WIDGETS ── */
.stSlider > label {{ font-size: 0.82rem !important; color: #94a3b8 !important; }}
.stSlider [data-baseweb="slider"] > div:first-child {{
    background: linear-gradient(90deg, {C_CYAN}, {C_PURPLE}) !important;
}}
.stSlider [role="slider"] {{
    background: #ffffff !important; border-color: {C_CYAN} !important;
    box-shadow: 0 0 0 3px rgba(0,210,255,0.2) !important;
}}
.stSelectbox > label, .stMultiSelect > label {{
    font-size: 0.82rem !important; color: #94a3b8 !important;
}}
.stSelectbox [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] > div {{
    background: rgba(13,21,38,0.9) !important;
    border-color: {C_BORDER} !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}}
.stTextInput input, .stNumberInput input {{
    background: rgba(13,21,38,0.9) !important;
    border-color: {C_BORDER} !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-size: 0.9rem !important;
}}
.stTextInput input:focus, .stNumberInput input:focus {{
    border-color: rgba(0,210,255,0.4) !important;
    box-shadow: 0 0 0 2px rgba(0,210,255,0.1) !important;
}}
/* Kill the ugly blue tooltip on slider */
[data-testid="stThumbValue"] {{
    background: {C_CARD} !important;
    color: #ffffff !important;
    border: 1px solid rgba(0,210,255,0.25) !important;
    border-radius: 6px !important;
}}
/* Dropdowns */
[data-baseweb="popover"] > div {{
    background: #0d1526 !important;
    border: 1px solid {C_BORDER} !important;
    border-radius: 12px !important;
}}
[data-baseweb="menu"] li:hover {{
    background: rgba(0,210,255,0.08) !important;
}}
/* Override BaseWeb primary */
[data-baseweb] {{
    --primary: {C_CYAN} !important;
    --primary400: {C_CYAN} !important;
}}

/* ── BUTTONS ── */
.stButton > button {{
    background: linear-gradient(135deg, {C_CYAN}, {C_PURPLE}) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.4rem !important;
    box-shadow: 0 4px 14px rgba(0,210,255,0.2) !important;
    transition: all 0.25s !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(0,210,255,0.3) !important;
}}

/* ── EXPANDERS ── */
.streamlit-expanderHeader {{
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #64748b !important;
}}
.streamlit-expanderContent {{
    background: rgba(13,21,38,0.5) !important;
    border: 1px solid {C_BORDER} !important;
    border-radius: 0 0 12px 12px !important;
}}

/* ── METRICS ── */
[data-testid="stMetric"] > div:first-child {{ color: #64748b !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.08em; }}
[data-testid="stMetricValue"] {{ color: #ffffff !important; font-size: 1.6rem !important; font-weight: 700 !important; }}
[data-testid="stMetricDelta"] {{ font-weight: 600 !important; font-size: 0.82rem !important; }}

/* ── FORMS ── */
[data-testid="stForm"] {{
    background: rgba(13,21,38,0.6);
    border: 1px solid {C_BORDER};
    border-radius: 16px;
    padding: 1.5rem;
}}

/* ── CAPTIONS ── */
.stCaption {{ color: #475569 !important; font-size: 0.78rem !important; }}

/* ── SCROLLBAR ── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: rgba(100,116,139,0.25); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: rgba(100,116,139,0.45); }}

/* ── CHAT INPUT & CHAT MESSAGES BASEWEB HIGH CONTRAST (DARK MODE) ── */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {{
    background-color: rgba(13, 21, 38, 0.98) !important;
    border: 1.5px solid #38bdf8 !important;
    border-radius: 14px !important;
}}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background-color: transparent !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    caret-color: #38bdf8 !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}}
[data-testid="stChatMessage"] {{
    background-color: rgba(13, 21, 38, 0.75) !important;
    border: 1px solid rgba(148, 163, 184, 0.25) !important;
    border-radius: 16px !important;
}}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div {{
    color: #f1f5f9 !important;
    -webkit-text-fill-color: #f1f5f9 !important;
    font-size: 0.96rem !important;
    line-height: 1.65 !important;
}}
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] b {{
    color: #38bdf8 !important;
    -webkit-text-fill-color: #38bdf8 !important;
    font-weight: 700 !important;
}}

</style>
""", unsafe_allow_html=True)

if IS_LIGHT:
    st.markdown(f"""
    <style>
    /* ── ROOT & BACKGROUND ── */
    html, body, .stApp {{ background: #f9fafb !important; color: #374151 !important; }}
    .stApp {{ background: #f9fafb !important; }} /* Strip neon gradients for a clean enterprise look */

    /* ── TYPOGRAPHY ── */
    h1 {{
        background: linear-gradient(90deg, #1d4ed8, #6d28d9, #047857) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }}
    h2 {{ color: #111827 !important; }}
    h3 {{ color: #1f2937 !important; }}
    h4 {{ color: #4b5563 !important; }}
    p  {{ color: #4b5563 !important; }}
    b, strong {{ color: #111827 !important; }}

    /* ── SECTION HEADER PILL ── */
    .section-pill {{
        background: #eff6ff !important;
        border: 1px solid #bfdbfe !important;
        color: #1d4ed8 !important;
    }}

    /* ── KPI GRID ── */
    .kpi-card {{
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-top: 3px solid #3b82f6 !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1) !important;
        border-radius: 12px !important;
    }}
    .kpi-card::before {{ display: none !important; }}
    .kpi-card:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1) !important;
    }}
    .kpi-card.red  {{ border-top-color: #ef4444 !important; }}
    .kpi-card.green {{ border-top-color: #10b981 !important; }}
    .kpi-card.amber {{ border-top-color: #f59e0b !important; }}
    .kpi-card.purple {{ border-top-color: #8b5cf6 !important; }}
    
    .kpi-label {{ color: #6b7280 !important; }}
    .kpi-val {{ color: #111827 !important; }}
    .kpi-sub {{ color: #6b7280 !important; }}

    /* ── GLASS PANELS (Solid Clean Cards in Light Mode) ── */
    .glass-panel {{
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-left: 4px solid #3b82f6 !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        border-radius: 12px !important;
    }}
    .glass-panel.green {{ border-left-color: #10b981 !important; }}
    .glass-panel.amber {{ border-left-color: #f59e0b !important; }}
    .glass-panel h3, .glass-panel h4 {{ color: #111827 !important; }}
    
    .glass-panel.amber .section-pill {{ background: #fffbeb !important; border-color: #fde68a !important; color: #b45309 !important; }}
    .glass-panel.green .section-pill {{ background: #ecfdf5 !important; border-color: #a7f3d0 !important; color: #047857 !important; }}

    /* ── DIVIDER ── */
    .section-div {{ background: #e5e7eb !important; height: 1px !important; margin: 2rem 0 !important; }}
    .header-image {{ border-color: #e5e7eb !important; opacity: 0.9 !important; }}

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {{
        background: #f3f4f6 !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 4px !important;
    }}
    .stTabs [data-baseweb="tab"] {{ color: #6b7280 !important; border-radius: 6px !important; }}
    .stTabs [data-baseweb="tab"]:hover {{ background: #e5e7eb !important; color: #374151 !important; }}
    .stTabs [aria-selected="true"] {{
        background: #ffffff !important;
        color: #111827 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }}

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {{
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb !important;
    }}
    [data-testid="stSidebar"] .stMarkdown p {{ color: #4b5563 !important; }}

    /* ── WIDGETS ── */
    .stSlider > label, .stSelectbox > label, .stMultiSelect > label {{ color: #374151 !important; font-weight: 500 !important; }}
    
    .stSelectbox [data-baseweb="select"] > div,
    .stMultiSelect [data-baseweb="select"] > div {{
        background: #f9fafb !important;
        border-color: #d1d5db !important;
        border-radius: 8px !important;
        color: #111827 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }}
    .stTextInput input, .stNumberInput input {{
        background: #f9fafb !important;
        border-color: #d1d5db !important;
        border-radius: 8px !important;
        color: #111827 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }}
    .stTextInput input:focus, .stNumberInput input:focus, 
    .stSelectbox [data-baseweb="select"] > div:focus-within,
    .stMultiSelect [data-baseweb="select"] > div:focus-within {{
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        background: #ffffff !important;
    }}
    
    .stSlider [data-baseweb="slider"] > div:first-child {{ background: #3b82f6 !important; }}
    .stSlider [role="slider"] {{
        background: #ffffff !important;
        border-color: #d1d5db !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }}
    [data-testid="stThumbValue"] {{
        background: #1f2937 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }}
    
    [data-baseweb="popover"] > div {{
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }}
    [data-baseweb="menu"] li:hover {{ background: #f3f4f6 !important; color: #111827 !important; }}
    [data-baseweb] {{
        --primary: #3b82f6 !important;
        --primary400: #3b82f6 !important;
    }}

    /* ── BUTTONS ── */
    .stButton > button {{
        background: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }}
    .stButton > button:hover {{
        background: #f9fafb !important;
        border-color: #9ca3af !important;
        color: #111827 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-1px) !important;
    }}

    /* ── EXPANDERS ── */
    .streamlit-expanderHeader {{ color: #374151 !important; font-weight: 600 !important; }}
    .streamlit-expanderContent {{
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05) !important;
    }}

    /* ── METRICS ── */
    [data-testid="stMetric"] > div:first-child {{ color: #6b7280 !important; }}
    [data-testid="stMetricValue"] {{ color: #111827 !important; }}

    /* ── FORMS ── */
    [data-testid="stForm"] {{
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
    }}

    /* ── CAPTIONS ── */
    .stCaption {{ color: #6b7280 !important; }}

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar-thumb {{ background: #cbd5e1 !important; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #94a3b8 !important; }}
    </style>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# ML MODEL SETUP
# ──────────────────────────────────────────────────────────────
MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
if str(MODELS_DIR) not in sys.path:
    sys.path.insert(0, str(MODELS_DIR))

try:
    from ll97_playground import get_data_driven_insights, CURRENT_LIMITS
    ML_INSIGHTS_AVAILABLE = True
except ImportError:
    ML_INSIGHTS_AVAILABLE = False
    CURRENT_LIMITS = {"Default": 0.00750}

    def get_data_driven_insights(year, score, emissions, gfa, prop_type, type_avg_data, global_avg):
        return (
            ["Diagnostic engine unavailable — could not import 'll97_playground.py'."],
            ["Verify that 'models/ll97_playground.py' exists and is importable."],
            0.0,
        )


# ──────────────────────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "results.csv"
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error("❌ Data file not found. Ensure 'results.csv' is in the application/ directory.")
        st.stop()

    numeric_cols = [
        "Total GHG Emissions (Metric Tons CO2e)", "Net Emissions (Metric Tons CO2e)",
        "Base LL97 Penalty", "ENERGY STAR Score", "Building Age", "Year Built",
        "Total GHG Emissions Intensity (kgCO2e/ft²)",
        "Avoided Emissions - Onsite and Offsite Green Power (Metric Tons CO2e)",
        "Electricity Use - Grid Purchase (kBtu)", "Natural Gas Use (kBtu)",
        "District Steam Use (kBtu)", "Fuel Oil #2 Use (kBtu)", "Diesel #2 Use (kBtu)",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Total GHG Emissions (Metric Tons CO2e)" in df.columns:
        df["Base LL97 Penalty"] = df["Total GHG Emissions (Metric Tons CO2e)"] * 268
    if "Year Built" in df.columns:
        if "Building Age" not in df.columns:
            df["Building Age"] = 2026 - df["Year Built"]
        df["Decade Built"] = (df["Year Built"] // 10) * 10
    return df


raw_df = load_data()

# Column aliases
CN   = "Property Name"
CGHG = "Total GHG Emissions (Metric Tons CO2e)"
CNET = "Net Emissions (Metric Tons CO2e)"
CPEN = "Base LL97 Penalty"
CSCO = "ENERGY STAR Score"
CINT = "Total GHG Emissions Intensity (kgCO2e/ft²)"
CAVO = "Avoided Emissions - Onsite and Offsite Green Power (Metric Tons CO2e)"
CTYP = "Primary Property Type - Portfolio Manager-Calculated"
CBOR = "Borough"
CCIT = "City"
CAGE = "Building Age"
CDEC = "Decade Built"
CALT = "Alerts"
COCC = "Occupancy"
CCST = "Construction Status"


# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="padding: 1rem 0 0.5rem;">
            <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.25rem;">
                <span style="font-size:1.4rem;">🌍</span>
                <span style="font-size:1rem;font-weight:700;color:{'#111827' if IS_LIGHT else '#ffffff'};">Carbon Heist</span>
            </div>
            <div style="font-size:0.72rem;color:#475569;letter-spacing:0.08em;text-transform:uppercase;">ESG Mitigation Platform</div>
        </div>
        <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,210,255,0.15),transparent);margin:0.75rem 0 1rem;"></div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;'>📍 Location</div>", unsafe_allow_html=True)
    with st.expander("Location Filters", expanded=True):
        sel_cities = st.multiselect("City", raw_df[CCIT].dropna().unique() if CCIT in raw_df.columns else [])
        valid_boros = [b for b in raw_df[CBOR].dropna().unique() if b not in ["Outside NYC", "Invalid/Address", "Unknown", "N/A"]] if CBOR in raw_df.columns else []
        sel_boros  = st.multiselect("Borough", sorted(valid_boros))

    st.markdown("<div style='font-size:0.7rem;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin:0.75rem 0 0.5rem;'>🏢 Property</div>", unsafe_allow_html=True)
    with st.expander("Property Details", expanded=True):
        sel_types   = st.multiselect("Property Type", raw_df[CTYP].dropna().unique() if CTYP in raw_df.columns else [])
        sel_decades = st.multiselect("Decade Built", sorted(raw_df[CDEC].dropna().unique()) if CDEC in raw_df.columns else [])
        sel_occ     = st.multiselect("Occupancy", raw_df[COCC].dropna().unique() if COCC in raw_df.columns else [])
        sel_const   = st.multiselect("Construction Status", raw_df[CCST].dropna().unique() if CCST in raw_df.columns else [])
        age_min = int(raw_df[CAGE].min()) if CAGE in raw_df.columns else 0
        age_max = int(raw_df[CAGE].max()) if CAGE in raw_df.columns else 200
        sel_age = st.slider("Building Age", age_min, age_max, (age_min, age_max))

    st.markdown("<div style='font-size:0.7rem;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin:0.75rem 0 0.5rem;'>📊 Performance</div>", unsafe_allow_html=True)
    with st.expander("Performance & Risk", expanded=False):
        sel_score = st.slider("ENERGY STAR Score", 0, 100, (0, 100))
        ghg_min = float(raw_df[CGHG].min()) if CGHG in raw_df.columns else 0.0
        ghg_max = float(raw_df[CGHG].max()) if CGHG in raw_df.columns else 1e6
        sel_ghg = st.slider("GHG Emissions (tCO₂e)", ghg_min, ghg_max, (ghg_min, ghg_max))
        pen_min = float(raw_df[CPEN].min()) if CPEN in raw_df.columns else 0.0
        pen_max = float(raw_df[CPEN].max()) if CPEN in raw_df.columns else 1e8
        sel_pen = st.slider("LL97 Penalty ($)", pen_min, pen_max, (pen_min, pen_max))



    st.markdown("<div style='height:1px;background:linear-gradient(90deg,transparent,rgba(0,210,255,0.1),transparent);margin:1rem 0;'></div>", unsafe_allow_html=True)
    search_term = st.text_input("🔍 Search Property Name", "")

# Apply filters
df = raw_df.copy()
if search_term and CN in df.columns:                             df = df[df[CN].str.contains(search_term, case=False, na=False)]
if sel_cities and CCIT in df.columns:                            df = df[df[CCIT].isin(sel_cities)]
if sel_boros  and CBOR in df.columns:                            df = df[df[CBOR].isin(sel_boros)]
if sel_types  and CTYP in df.columns:                            df = df[df[CTYP].isin(sel_types)]
if sel_decades and CDEC in df.columns:                           df = df[df[CDEC].isin(sel_decades)]
if sel_occ    and COCC in df.columns:                            df = df[df[COCC].isin(sel_occ)]
if sel_const  and CCST in df.columns:                            df = df[df[CCST].isin(sel_const)]
if CAGE in df.columns:                                           df = df[df[CAGE].between(sel_age[0], sel_age[1])]
if CSCO in df.columns:                                           df = df[df[CSCO].fillna(0).between(sel_score[0], sel_score[1])]
if CGHG in df.columns:                                           df = df[df[CGHG].between(sel_ghg[0], sel_ghg[1])]
if CPEN in df.columns:                                           df = df[df[CPEN].between(sel_pen[0], sel_pen[1])]



# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────
CHART_BASE = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94a3b8", size=12),
    margin=dict(t=48, b=28, l=28, r=28),
    xaxis=dict(gridcolor="rgba(100,116,139,0.1)", zerolinecolor="rgba(100,116,139,0.12)"),
    yaxis=dict(gridcolor="rgba(100,116,139,0.1)", zerolinecolor="rgba(100,116,139,0.12)"),
    hoverlabel=dict(bgcolor="#0d1526", bordercolor=C_BORDER, font_color="#e2e8f0"),
)

if IS_LIGHT:
    CHART_BASE.update(
        template="plotly_white",
        font=dict(family="Inter", color="#4b5563", size=12),
        xaxis=dict(gridcolor="#e5e7eb", zerolinecolor="#d1d5db", tickfont=dict(color="#374151")),
        yaxis=dict(gridcolor="#e5e7eb", zerolinecolor="#d1d5db", tickfont=dict(color="#374151")),
        legend=dict(font=dict(color="#111827")),
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e5e7eb", font_color="#111827"),
    )

def chart(title="", **kwargs):
    cfg = dict(**CHART_BASE)
    cfg["title"] = dict(text=title, font=dict(size=14, color=("#111827" if IS_LIGHT else "#ffffff"), family="Inter"))
    cfg.update(kwargs)
    return cfg

def hbar(data, x, y, title, color, hover_cols=None):
    fig = px.bar(data, x=x, y=y, orientation="h", hover_data=hover_cols)
    fig.update_traces(marker_color=color, marker_line_width=0, opacity=0.88)
    fig.update_layout(chart(title), yaxis={"categoryorder": "total ascending"})
    return fig

def pill(icon, label):
    return f'<div class="section-pill">{icon} {label}</div>'

def kpi(label, value, sub="", cls=""):
    return f"""<div class="kpi-card {cls}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-val">{value}</div>
        {'<div class="kpi-sub">'+sub+'</div>' if sub else ''}
    </div>"""

def kpi_row(*cards):
    inner = "".join(cards)
    return f'<div class="kpi-grid">{inner}</div>'

def section_div():
    return '<div class="section-div"></div>'


@st.cache_resource
def load_ml_assets():
    model_path    = MODELS_DIR / "ll97_model.joblib"
    encoders_path = MODELS_DIR / "ll97_encoders.joblib"
    try:
        if not model_path.exists() or not encoders_path.exists():
            return None, None
        return joblib.load(model_path), joblib.load(encoders_path)
    except Exception:
        return None, None


def compute_peer_benchmarks(dataset, encoders):
    if isinstance(encoders, dict) and "type_avg" in encoders and "global_avg" in encoders:
        return encoders["type_avg"], encoders["global_avg"]
    if CGHG not in dataset.columns or CTYP not in dataset.columns:
        return {}, 1.0
    working = dataset.dropna(subset=[CGHG, CTYP]).copy()
    if CINT in working.columns:
        working["_gfa"] = np.where(working[CINT] > 0, (working[CGHG]*1000)/working[CINT], np.nan)
        working = working.dropna(subset=["_gfa"])
        if len(working) > 0:
            g = working.groupby(CTYP)
            return (g[CGHG].sum() / g["_gfa"].sum()).to_dict(), working[CGHG].sum()/working["_gfa"].sum()
    type_avg = working.groupby(CTYP)[CGHG].mean().to_dict()
    return type_avg, working[CGHG].mean() if len(working) > 0 else 1.0


def validate_ml_inputs(year_built, gfa, score):
    errs = []
    if year_built is None or not (1800 <= year_built <= 2026): errs.append("⚠️ Year Built must be 1800–2026.")
    if gfa is None or gfa <= 0:                                errs.append("⚠️ Gross Floor Area must be positive.")
    if score is None or not (0 <= score <= 100):               errs.append("⚠️ ENERGY STAR Score must be 0–100.")
    return errs


# ══════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════
col_t, col_meta = st.columns([3, 1])
with col_t:
    st.title("🌍 Carbon Heist Mitigation")
    st.markdown(f"<p style='color:#64748b;margin-top:-0.4rem;font-size:0.88rem;'>ESG & LL97 Analytics Platform · {len(df):,} properties in view</p>", unsafe_allow_html=True)
with col_meta:
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    if len(df) < len(raw_df):
        st.info(f"🔽 Filters active: {len(raw_df)-len(df):,} properties hidden")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  📊  Problem Analysis  ",
    "  🛠️  Mitigation Scenarios  ",
    "  🤖  ML Predictor  ",
    "  💼  Financial Modeling  ",
    "  💬  AI C-Suite Co-Pilot & Chart Bot  ",
])


# ══════════════════════════════════════════════════════════════
# TAB 1 — PROBLEM ANALYSIS
# ══════════════════════════════════════════════════════════════
with tab1:
    kpi_ghg     = df[CGHG].sum()  if CGHG in df.columns else 0
    kpi_net     = df[CNET].sum()  if CNET in df.columns else 0
    kpi_penalty = df[CPEN].sum()  if CPEN in df.columns else 0
    kpi_score   = df[CSCO].mean() if CSCO in df.columns else 0
    kpi_intens  = df[CINT].mean() if CINT in df.columns else 0
    kpi_avoided = df[CAVO].sum()  if CAVO in df.columns else 0
    high_risk   = len(df[df[CPEN] > df[CPEN].quantile(0.75)]) if CPEN in df.columns else 0
    n_bldg      = len(df)

    st.markdown(kpi_row(
        kpi("Total Properties", f"{n_bldg:,}",    sub="in current filter"),
        kpi("Total GHG",        f"{kpi_ghg/1e6:.2f}M tCO₂e", sub="metric tons CO₂ equiv.", cls="red"),
        kpi("LL97 Penalty",     f"${kpi_penalty/1e9:.2f}B",   sub="aggregate exposure",     cls="red"),
        kpi("Avg ENERGY STAR",  f"{kpi_score:.1f}",            sub="out of 100",             cls="green"),
        kpi("Avoided Emissions",f"{kpi_avoided/1e3:.1f}K tCO₂e", sub="via clean power",    cls="green"),
        kpi("High-Risk Assets", f"{high_risk:,}",             sub="top 25% penalty",        cls="amber"),
    ), unsafe_allow_html=True)

    # CSO Panel
    highest_emitter = df.loc[df[CGHG].idxmax()][CN] if CGHG in df.columns and not df[CGHG].isna().all() else "N/A"
    highest_fine    = df.loc[df[CPEN].idxmax()][CN] if CPEN in df.columns and not df[CPEN].isna().all() else "N/A"
    best_star       = df.loc[df[CSCO].idxmax()][CN] if CSCO in df.columns and not df[CSCO].isna().all() else "N/A"

    st.markdown(f"""
    <div class="glass-panel">
        <div class="section-pill">📑 Chief Sustainability Officer Briefing</div>
        <p>The portfolio currently carries an aggregate LL97 exposure of <b>${kpi_penalty:,.0f}</b> driven by
        <b>{kpi_ghg:,.0f} metric tons</b> of CO₂e across <b>{n_bldg:,} properties</b>. The primary
        emissions bottleneck is <b>{highest_emitter}</b>, while <b>{highest_fine}</b> represents the most acute
        financial liability. <b>{best_star}</b> leads the portfolio as the benchmark for decarbonization performance.
        Capital allocation should be front-loaded toward the worst-offending assets to achieve the fastest
        penalty-avoidance ROI.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── High Risk
    st.markdown(pill("🚨", "High-Risk Identification"), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if all(c in df.columns for c in [CN, CGHG]):
            top_ghg = df.nlargest(10, CGHG).sort_values(CGHG, ascending=True)
            fig = hbar(top_ghg, CGHG, CN, "Top 10 Buildings by GHG Emissions", C_RED, [CTYP, CBOR])
            st.plotly_chart(fig, width='stretch')
            st.caption("Gross tCO₂e contributions from the worst-emitting properties.")
            with st.expander("🔍 Insights: Top Polluters"):
                h = top_ghg.iloc[-1]
                pct = (h[CGHG]/kpi_ghg*100) if kpi_ghg > 0 else 0
                st.info(f"* **Highest Emitter:** {h[CN]} — {h[CGHG]:,.0f} tCO₂e\n* **Concentration:** This property alone accounts for **{pct:.1f}%** of filtered emissions.\n* **Outlier:** Emits {h[CGHG]-(top_ghg.iloc[-2][CGHG] if len(top_ghg)>1 else 0):,.0f} tCO₂e more than #2.")
    with c2:
        if all(c in df.columns for c in [CN, CPEN]):
            top_pen = df.nlargest(10, CPEN).sort_values(CPEN, ascending=True)
            fig = hbar(top_pen, CPEN, CN, "Top 10 Buildings by LL97 Fine Exposure", C_RED, [CGHG])
            st.plotly_chart(fig, width='stretch')
            st.caption("Highest estimated statutory fines under Local Law 97.")
            with st.expander("💡 Insights: Financial Risk"):
                hr = top_pen.iloc[-1]
                top10 = top_pen[CPEN].sum()
                st.warning(f"* **Max Liability:** {hr[CN]} — ${hr[CPEN]:,.0f}\n* **Top 10 Concentration:** ${top10:,.0f} ({(top10/kpi_penalty*100):.1f}% of portfolio)\n* **Action:** Retrofitting these 10 properties yields the highest penalty-avoidance ROI.")

    st.markdown(section_div(), unsafe_allow_html=True)

    # ── Regional & Type
    st.markdown(pill("🏢", "Portfolio Distribution"), unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if CTYP in df.columns and CGHG in df.columns:
            type_df = df.groupby(CTYP)[CGHG].sum().reset_index().nlargest(10, CGHG).sort_values(CGHG, ascending=True)
            st.plotly_chart(hbar(type_df, CGHG, CTYP, "Emissions by Building Type (tCO₂e)", C_CYAN), width='stretch')
            st.caption("Aggregated emissions by primary property use-case.")
    with c4:
        if CBOR in df.columns and CPEN in df.columns and CINT in df.columns:
            valid_boros = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
            boro_df = (
                df[df[CBOR].isin(valid_boros)]
                .groupby(CBOR)
                .agg({CPEN: "sum", CGHG: "sum", CINT: "mean"})
                .reset_index()
                .sort_values(CPEN, ascending=False)
            )
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Bar(
                    x=boro_df[CBOR],
                    y=boro_df[CPEN],
                    name="LL97 Fine Exposure ($)",
                    marker_color=C_CYAN,
                    opacity=0.88,
                    hovertemplate="<b>%{x}</b><br>Fine Liability: $%{y:,.0f}<extra></extra>",
                ),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(
                    x=boro_df[CBOR],
                    y=boro_df[CINT],
                    name="Avg Intensity (kgCO₂/ft²)",
                    mode="lines+markers",
                    marker=dict(color=C_AMBER, size=8),
                    line=dict(color=C_AMBER, width=2.5),
                    hovertemplate="Avg Intensity: %{y:.2f} kgCO₂/ft²<extra></extra>",
                ),
                secondary_y=True,
            )
            fig.update_layout(
                chart("NYC Borough Analysis: Fine Exposure vs Intensity", margin=dict(t=50, b=65, l=45, r=45)),
                legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5)
            )
            fig.update_yaxes(title_text="LL97 Penalty ($)", secondary_y=False, gridcolor="rgba(100,116,139,0.1)" if not IS_LIGHT else "#e5e7eb")
            fig.update_yaxes(title_text="Avg Intensity (kgCO₂/ft²)", secondary_y=True, showgrid=False)
            st.plotly_chart(fig, width='stretch')
            st.caption("Total statutory fine exposure (bars, left axis) vs average carbon intensity per sq ft (line, right axis).")

    st.markdown(section_div(), unsafe_allow_html=True)

    # ── Operational
    st.markdown(pill("⚡", "Operational Insights"), unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        if all(c in df.columns for c in [CAGE, CINT, CN]):
            try:
                fig = px.scatter(df, x=CAGE, y=CINT, opacity=0.55, hover_name=CN, hover_data=[CTYP, CGHG],
                                 trendline="ols", trendline_color_override=C_AMBER)
            except Exception:
                fig = px.scatter(df, x=CAGE, y=CINT, opacity=0.55, hover_name=CN)
            fig.update_traces(marker_color=C_CYAN, selector=dict(mode="markers"))
            fig.update_layout(chart("Building Age vs Emission Intensity"))
            st.plotly_chart(fig, width='stretch')
            st.caption("Relationship between infrastructure age and carbon efficiency.")
            with st.expander("💡 Insights: Infrastructure Age"):
                corr = df[CAGE].corr(df[CINT]) if len(df.dropna(subset=[CAGE, CINT])) > 2 else 0
                txt = "tend to be less efficient" if corr > 0 else "show no clear efficiency degradation vs newer builds"
                st.info(f"* **Trend:** Older buildings {txt} (r={corr:.2f})\n* **Oldest Asset:** {df.loc[df[CAGE].idxmax()][CN]} ({df[CAGE].max():.0f} yrs)\n* **Worst Intensity:** {df.loc[df[CINT].idxmax()][CN]}")
    with c6:
        energy_cols = [c for c in df.columns if "Use (kBtu)" in c]
        if energy_cols:
            esums = df[energy_cols].sum().sort_values(ascending=True)
            edf   = pd.DataFrame({"Source": esums.index.str.replace(" Use (kBtu)", "", regex=False), "kBtu": esums.values})
            st.plotly_chart(hbar(edf, "kBtu", "Source", "Portfolio Energy Source Breakdown", C_CYAN), width='stretch')
            st.caption("Aggregate consumption by fuel/utility type.")

    c7, c8 = st.columns(2)
    with c7:
        if all(c in df.columns for c in [CSCO, CINT, CN]):
            fig = px.scatter(df, x=CSCO, y=CINT, color=CSCO, hover_name=CN,
                             color_continuous_scale="RdYlGn", opacity=0.65)
            fig.update_layout(chart("ENERGY STAR Score vs Emission Intensity"))
            st.plotly_chart(fig, width='stretch')
            st.caption("Higher ENERGY STAR scores should correlate with lower carbon intensity.")
    with c8:
        if CALT in df.columns:
            aseries = df[CALT].dropna().astype(str).str.split(",").explode().str.strip()
            acnt    = aseries.value_counts().reset_index().head(10).sort_values("count", ascending=True)
            acnt.columns = ["Alert Type", "Frequency"]
            st.plotly_chart(hbar(acnt, "Frequency", "Alert Type", "Data Quality Alerts Detected", C_AMBER), width='stretch')
            st.caption("Most common utility reporting anomalies in the dataset.")


# ══════════════════════════════════════════════════════════════
# TAB 2 — MITIGATION SCENARIOS
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<img src="https://images.unsplash.com/photo-1466611653911-95081537e5b7?q=80&w=1400&auto=format&fit=crop" class="header-image" style="border-radius:16px;width:100%;height:180px;object-fit:cover;opacity:0.75;margin-bottom:1.25rem;border:1px solid rgba(255,255,255,0.06);">', unsafe_allow_html=True)

    st.markdown(pill("🛠️", "Configure Strategic Interventions"), unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    with sc1: eff_pct   = st.slider("💡 Energy Efficiency Upgrade (%)", 0, 40, 15) / 100
    with sc2: renew_pct = st.slider("☀️ Renewable Energy Adoption (%)", 0, 100, 30) / 100
    with sc3: retro_age = st.slider("🏗️ Deep Retrofit Target Age (years)", 20, 100, 50)

    base_em  = df[CGHG].sum() if CGHG in df.columns else 1
    base_pen = df[CPEN].sum() if CPEN in df.columns else 0
    s1_red   = base_em * eff_pct

    grid_col   = "Electricity Use - Grid Purchase (kBtu)"
    grid_ratio = df[grid_col].sum() / df[[c for c in df.columns if "Use (kBtu)" in c]].sum().sum() \
                 if grid_col in df.columns else 0.4
    s2_red   = base_em * grid_ratio * renew_pct
    s2_bldgs = len(df[df[grid_col] > 0]) if grid_col in df.columns else len(df)

    if CAGE in df.columns:
        tgt = df[df[CAGE] >= retro_age]
        s3_red, s3_bldgs = tgt[CGHG].sum() * 0.40, len(tgt)
    else:
        s3_red, s3_bldgs = 0, 0

    rem = base_em*(1-eff_pct) - s2_red*(1-eff_pct) - s3_red*(1-eff_pct)
    comb_red = base_em - rem
    def savings(r): return base_pen * (r / base_em) if base_em > 0 else 0

    st.markdown(section_div(), unsafe_allow_html=True)
    st.markdown(pill("🎯", "Combined Strategy Outcomes"), unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Residual Emissions (tCO₂e)", f"{rem:,.0f}", f"-{comb_red:,.0f} ({(comb_red/base_em*100):.1f}%)")
    m2.metric("Annual LL97 Fine Avoided",    f"${savings(comb_red):,.0f} / yr", "recurring annual savings")
    m3.metric("Buildings Impacted",          f"{len(df):,}", "portfolio wide")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=(comb_red/base_em)*100,
        title={"text": "Emissions Reduction %", "font": {"color": ("#4b5563" if IS_LIGHT else "#94a3b8"), "size": 13}},
        number={"suffix": "%", "font": {"color": C_GREEN, "size": 28}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": ("#d1d5db" if IS_LIGHT else "#475569")},
            "bar":  {"color": C_GREEN, "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0, 20],  "color": "rgba(255,75,110,0.15)"},
                {"range": [20, 50], "color": "rgba(255,184,0,0.12)"},
                {"range": [50,100], "color": "rgba(0,245,155,0.1)"},
            ],
            "borderwidth": 0,
        },
    ))
    fig_gauge.update_layout(chart("", height=220, margin=dict(t=30, b=0, l=10, r=10)))
    with m4:
        st.plotly_chart(fig_gauge, width='stretch')

    with st.expander("💡 Strategy Analysis"):
        scenarios_tbl = pd.DataFrame({
            "Scenario": ["S1: Efficiency","S2: Renewables","S3: Retrofit"],
            "Reduction %": [(s1_red/base_em)*100,(s2_red/base_em)*100,(s3_red/base_em)*100],
        })
        best = scenarios_tbl.loc[scenarios_tbl["Reduction %"].idxmax()]
        st.success(f"* **Best single measure:** {best['Scenario']} ({best['Reduction %']:.1f}% reduction)\n"
                   f"* **Combined removes:** {comb_red:,.0f} tCO₂e saving ${savings(comb_red):,.0f}/yr\n"
                   f"* **Residual liability:** {rem:,.0f} tCO₂e still requires offsets or deeper CAPEX")

    st.markdown(section_div(), unsafe_allow_html=True)
    st.markdown(pill("📉", "Impact Breakdown"), unsafe_allow_html=True)

    bc1, bc2 = st.columns(2)
    with bc1:
        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=["absolute","relative","relative","relative","total"],
            x=["Baseline","Efficiency","Renewables","Retrofits","Residual"],
            y=[base_em,-s1_red,-s2_red,-s3_red, rem],
            text=[f"{v/1e3:.1f}k" for v in [base_em,-s1_red,-s2_red,-s3_red,rem]],
            textposition="outside",
            decreasing={"marker": {"color": C_GREEN}},
            increasing={"marker": {"color": C_RED}},
            totals={"marker": {"color": C_CYAN}},
        ))
        fig_wf.update_layout(chart("Emissions Reduction Waterfall (tCO₂e)"))
        st.plotly_chart(fig_wf, width='stretch')
        st.caption("Step-by-step impact from baseline to final residual footprint.")
    with bc2:
        cats = ["CO₂ Reduction %","Penalty Savings %","Portfolio Coverage %"]
        fig_radar = go.Figure()
        def radarTrace(name, r_pct, bldgs, color):
            fig_radar.add_trace(go.Scatterpolar(
                r=[r_pct, r_pct, (bldgs/len(df)*100 if len(df)>0 else 0)],
                theta=cats, fill="toself", name=name, marker_color=color, opacity=0.8
            ))
        radarTrace("S1: Efficiency", (s1_red/base_em)*100, len(df), C_CYAN)
        radarTrace("S2: Renewables", (s2_red/base_em)*100, s2_bldgs,  C_AMBER)
        radarTrace("S3: Retrofit",   (s3_red/base_em)*100, s3_bldgs,  C_GREEN)
        fig_radar.update_layout(
            chart("Scenario Effectiveness Comparison"),
            polar=dict(radialaxis=dict(visible=True, range=[0,100], gridcolor="rgba(100,116,139,0.15)" if not IS_LIGHT else "#e5e7eb")),
        )
        st.plotly_chart(fig_radar, width='stretch')
        st.caption("Holistic impact comparison across the three independent strategies.")

    bc3, bc4 = st.columns(2)
    with bc3:
        scenario_df = pd.DataFrame({
            "Scenario": ["Efficiency","Renewables","Retrofit"],
            "CO₂ Reduction (tCO₂e)": [s1_red, s2_red, s3_red],
            "LL97 Savings ($)": [savings(s1_red), savings(s2_red), savings(s3_red)],
        })
        plot_long = scenario_df.melt(id_vars="Scenario", value_vars=["CO₂ Reduction (tCO₂e)","LL97 Savings ($)"])
        fig_comp = px.bar(plot_long, x="Scenario", y="value", color="variable", barmode="group",
                          color_discrete_sequence=[C_GREEN, C_CYAN])
        fig_comp.update_traces(marker_line_width=0, opacity=0.88)
        fig_comp.update_layout(chart("Scenario Return vs Impact"), yaxis_title="")
        st.plotly_chart(fig_comp, width='stretch')
        st.caption("Hover for exact physical and financial yield per scenario.")
    with bc4:
        df_road = pd.DataFrame([
            dict(Task="Phase 1: Audits & Efficiency", Start="2024-01-01", Finish="2024-12-31", Phase="Short-term"),
            dict(Task="Phase 2: Power Purchase Agreements", Start="2024-06-01", Finish="2025-06-30", Phase="Mid-term"),
            dict(Task="Phase 3: Deep Envelope Retrofits", Start="2025-01-01", Finish="2026-12-31", Phase="Long-term"),
        ])
        fig_tl = px.timeline(df_road, x_start="Start", x_end="Finish", y="Task", color="Phase",
                             color_discrete_sequence=[C_CYAN, C_AMBER, C_GREEN])
        fig_tl.update_layout(chart("Strategic Implementation Roadmap"))
        st.plotly_chart(fig_tl, width='stretch')
        st.caption("Proposed multi-phase execution timeline across 2024–2026.")

    st.markdown(f"""
    <div class="glass-panel amber" style="margin-top:1rem;">
        <div class="section-pill">
            💡 C-Suite Integration
        </div>
        <p>For detailed <b>Regulatory & Grid Shock Sensitivity Analysis</b> ($/ft²) or <b>Decade-Built WET Decarbonization Payback Modeling</b>,
        navigate to the <b>Financial Modeling</b> tab above.</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 3 — ML PREDICTOR
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown(pill("🤖", "AI-Powered Emissions & LL97 Liability Predictor"), unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;font-size:0.88rem;margin-top:-0.25rem;'>Enter a building's characteristics to forecast GHG emissions and estimate Local Law 97 penalty exposure using the trained Random Forest model.</p>", unsafe_allow_html=True)

    ml_model, ml_encoders = load_ml_assets()

    if ml_model is None or ml_encoders is None:
        st.error("⚠️ ML model assets not found. Ensure 'll97_model.joblib' and 'll97_encoders.joblib' are in the 'models/' directory.")
    elif not isinstance(ml_encoders, dict) or "bor" not in ml_encoders or "typ" not in ml_encoders:
        st.error("⚠️ Encoder file is malformed. Expected keys 'bor' and 'typ' not found.")
    else:
        boro_classes = list(ml_encoders["bor"].classes_)
        type_classes = list(ml_encoders["typ"].classes_)
        type_avg, global_avg = compute_peer_benchmarks(raw_df, ml_encoders)

        st.markdown(section_div(), unsafe_allow_html=True)
        st.markdown(pill("🏗️", "Building Profile Input"), unsafe_allow_html=True)

        with st.form("ml_form"):
            f1, f2, f3 = st.columns(3)
            with f1:
                yr   = st.number_input("Year Built",             1800, 2026, 1990, step=1)
                gfa  = st.number_input("Gross Floor Area (ft²)", 1.0, value=100000.0, step=1000.0)
            with f2:
                score   = st.number_input("ENERGY STAR Score", 0, 100, 50, step=1)
                borough = st.selectbox("Borough", boro_classes)
            with f3:
                prop_type = st.selectbox("Primary Property Type", type_classes)
                st.markdown("<div style='height:1.9rem'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("⚡ Generate Prediction", width='stretch')

        if submitted:
            errs = validate_ml_inputs(yr, gfa, score)
            if errs:
                for e in errs: st.error(e)
            else:
                try:
                    bc  = ml_encoders["bor"].transform([borough])[0]
                    tc  = ml_encoders["typ"].transform([prop_type])[0]
                    inp = pd.DataFrame([[yr, gfa, score, bc, tc]], columns=[
                        "Year Built", "Property GFA - Calculated (Buildings and Parking) (ft²)",
                        "ENERGY STAR Score", "Borough_Enc", "Type_Enc"
                    ])
                    pred_em  = float(ml_model.predict(inp)[0])
                    pred_pen = pred_em * 268
                    psf      = pred_pen / gfa
                    intens   = pred_em / gfa
                    limit    = CURRENT_LIMITS.get(prop_type, CURRENT_LIMITS.get("Default", 0.00750))
                    compliant = intens <= limit
                    diag, recs, gap = get_data_driven_insights(yr, score, pred_em, gfa, prop_type, type_avg, global_avg)

                    st.markdown(section_div(), unsafe_allow_html=True)
                    st.markdown(pill("📋", "Prediction Results"), unsafe_allow_html=True)

                    g_cls = "red" if gap > 0 else "green"
                    c_cls = "green" if compliant else "red"

                    st.markdown(kpi_row(
                        kpi("Predicted GHG",        f"{pred_em:,.1f}",     sub="tCO₂e per year",    cls="red"),
                        kpi("Estimated LL97 Fine",  f"${pred_pen:,.0f}",   sub="per year",          cls="red"),
                        kpi("Liability per ft²",    f"${psf:.3f}",         sub="$/ft²"),
                        kpi("Peer Comparison",      f"{gap:+.1f}%",        sub="vs building type",  cls=g_cls),
                        kpi("LL97 Compliance",      "✅ Compliant" if compliant else "🚫 Non-Compliant",
                            sub=f"limit: {limit:.5f}", cls=c_cls),
                        kpi("Emission Intensity",   f"{intens:.5f}",       sub="tCO₂e/ft²"),
                    ), unsafe_allow_html=True)

                    dc1, dc2 = st.columns(2)
                    with dc1:
                        with st.expander("🔍 AI Diagnosis", expanded=True):
                            for d in diag: st.info(d)
                    with dc2:
                        with st.expander("🛠️ Recommended Actions", expanded=True):
                            for r in recs: st.success(r)

                    if not ML_INSIGHTS_AVAILABLE:
                        st.warning("Insights running in fallback mode — 'll97_playground.py' could not be imported.")
                except Exception as exc:
                    st.error(f"⚠️ Prediction failed: {exc}")

        st.markdown(section_div(), unsafe_allow_html=True)
        st.markdown(pill("📈", "Model Intelligence"), unsafe_allow_html=True)

        if hasattr(ml_model, "feature_importances_"):
            imp_df = pd.DataFrame({
                "Feature":    ["Year Built","Floor Area (GFA)","ENERGY STAR Score","Borough","Property Type"],
                "Importance": ml_model.feature_importances_,
            }).sort_values("Importance", ascending=True)
            st.plotly_chart(hbar(imp_df, "Importance", "Feature", "Random Forest Feature Importance", C_CYAN),
                            width='stretch')
            st.caption("Relative influence of each input on the model's GHG emissions predictions.")
        else:
            st.info("Feature importance unavailable for this model type.")


# ══════════════════════════════════════════════════════════════
# TAB 4 — FINANCIAL MODELING
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown(pill("💼", "C-Suite Financial Modeling"), unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;font-size:0.88rem;margin-top:-0.25rem;'>Integrates Executive financial engineering models from the Excel project (Sensitivity & Scenario sheets) — regulatory shocks, CAPEX co-funding, and WET payback analysis.</p>", unsafe_allow_html=True)

    # ── Section 1: Sensitivity Simulator
    st.markdown(section_div(), unsafe_allow_html=True)
    st.markdown(pill("⚖️", "Regulatory & Grid Shock Sensitivity Simulator"), unsafe_allow_html=True)

    sma, smb = st.columns(2)
    with sma:
        sim_rate = st.slider("Fine Rate ($ / Metric Ton CO₂e)", 268, 400, 268, step=16,
                             help="Local Law 97 statutory fine rate — baseline is $268/MT.")
    with smb:
        sim_shock = st.slider("Emissions Shock (%)", 0, 25, 0, step=5,
                              help="Grid carbon intensity spike or extreme weather heating demand surge.")

    base_ghg_port = df[CGHG].sum() if CGHG in df.columns else 10_560_815.4
    port_gfa      = 2_014_727_607.4
    sim_ghg_v     = base_ghg_port * (1 + sim_shock / 100)
    sim_pen_v     = sim_ghg_v * sim_rate
    sim_psf       = sim_pen_v / port_gfa
    baseline_psf  = 1.4048
    variance      = (sim_psf - baseline_psf) / baseline_psf * 100
    v_cls = "red" if variance > 0 else "green"

    st.markdown(kpi_row(
        kpi("Simulated Portfolio Fine", f"${sim_pen_v/1e9:.3f}B",     sub="per year",             cls="red"),
        kpi("Penalty Intensity ($/ft²)",f"${sim_psf:.4f}",            sub="per sq ft",            cls=v_cls),
        kpi("Variance vs Baseline",     f"{variance:+.1f}%",          sub="vs $1.405/ft² base",   cls=v_cls),
        kpi("Simulated Emissions",      f"{sim_ghg_v/1e6:.2f}M tCO₂e", sub="portfolio total"),
    ), unsafe_allow_html=True)

    z = [[1.405,1.475,1.545,1.616],[1.573,1.651,1.730,1.808],[1.835,1.926,2.018,2.110]]
    fig_hm = go.Figure(go.Heatmap(
        z=z,
        x=["+0%","+5%","+10%","+15%"],
        y=["$268/MT (Base)","$300/MT (Moderate)","$350/MT (Severe)"],
        colorscale=[[0, ("#ffffff" if IS_LIGHT else "#0d1526")], [0.25,C_CYAN],[0.5,C_PURPLE],[0.75,C_AMBER],[1,C_RED]],
        texttemplate="<b>$%{z:.3f}</b>",
        textfont={"size": 15, "color": ("#111827" if IS_LIGHT else "white"), "family": "Inter"},
        hovertemplate="Rate: %{y}<br>Shock: %{x}<br>Liability: <b>$%{z:.3f}/ft²</b><extra></extra>",
    ))
    fig_hm.update_layout(
        chart("Portfolio Liability Intensity Matrix ($/ft²)", height=280, margin=dict(t=48, b=28, l=150, r=28))
    )
    st.plotly_chart(fig_hm, width='stretch')

    # ── Section 2: Playbooks
    st.markdown(section_div(), unsafe_allow_html=True)
    st.markdown(pill("🎯", "The 5 Strategic Decarbonization Playbooks"), unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;font-size:0.88rem;margin-top:-0.25rem;'>The 5 core engineering playbooks from the Excel Scenario sheet — from OPEX quick-wins to full electrification.</p>", unsafe_allow_html=True)

    PLAYBOOKS = [
        {"name":"Surgical Strike",      "short":"Surgical Strike",
         "target":"Top 10 worst offenders (0.07% portfolio area)",
         "capex":500_000,        "opex":45_000,      "savings":20_594_117,  "net_savings":20_549_117,  "payback":0.024,
         "base_pen":51_485_292,  "post_pen":30_891_175,
         "desc":"Dispatch engineering task force for Level 2 Energy Audits on the 10 worst properties. Execute low-cost OPEX repairs: fix leaks, recalibrate sensors, correct BMS scheduling. Annual OPEX ($45K/yr) covers quarterly sensor calibrations and ongoing BMS software fees."},
        {"name":"Retro-commissioning",  "short":"Retro-commissioning",
         "target":"Buildings with ENERGY STAR Score < 50",
         "capex":802_166_574,    "opex":3_250_000,   "savings":243_615_631, "net_savings":240_365_631, "payback":3.29,
         "base_pen":974_462_526, "post_pen":730_846_894,
         "desc":"Implement RCx and BMS optimization at $1.50/ft² to bring properties up to ENERGY STAR 75. Achieves 25% drop in energy consumption and LL97 penalties. Annual OPEX ($3.25M/yr) covers automated FDD monitoring and semi-annual VAV tuning."},
        {"name":"1960s Smart Scale",    "short":"1960s Smart Scale",
         "target":"1960s-built properties ($2.50/ft² package)",
         "capex":785_244_162,    "opex":2_800_000,   "savings":88_033_696,  "net_savings":85_233_696,  "payback":8.92,
         "base_pen":440_168_480, "post_pen":352_134_784,
         "desc":"Deploy $2.50/ft² package: networked LED + daylight sensors, VFD HVAC motors, CO₂-sensor Demand Control Ventilation, steam trap repairs, and boiler control upgrades. Annual OPEX ($2.80M/yr) covers preventative VFD maintenance and sensor checks."},
        {"name":"1930s WET Systems",    "short":"1930s WET Systems",
         "target":"1930s historic pre-war properties",
         "capex":1_499_764_152,  "opex":4_500_000,   "savings":122_390_647, "net_savings":117_890_647, "payback":12.25,
         "base_pen":305_976_618, "post_pen":183_585_971,
         "desc":"Public-Private Partnership (50% government grant = $749M). Install basement wastewater heat exchangers and high-efficiency water-to-water heat pumps to eliminate fossil combustion. Annual OPEX ($4.50M/yr) covers anti-fouling flush protocols and pump servicing."},
        {"name":"Electrification Push", "short":"Electrification Push",
         "target":"Properties using high-risk Fuel Oil #4",
         "capex":1_889_125_740,  "opex":5_100_000,   "savings":181_993_196, "net_savings":176_893_196, "payback":10.38,
         "base_pen":134_362_550, "post_pen":94_053_785,
         "desc":"Replace Fuel Oil #4 boilers with Electric Heat Pumps at $20/ft². Combines 30% penalty reduction + $1.50/ft² utility savings for a ~10-year payback. Annual OPEX ($5.10M/yr) covers OEM service contracts and thermographic inspections."},
    ]
    pb_df = pd.DataFrame(PLAYBOOKS)

    sel_pb = st.selectbox(
        "Select Playbook to Analyze",
        [p["name"] for p in PLAYBOOKS],
        format_func=lambda x: f"▸ {x}",
    )
    sp = next(p for p in PLAYBOOKS if p["name"] == sel_pb)

    pen_saved = sp["base_pen"] - sp["post_pen"]
    st.markdown(kpi_row(
        kpi("Required CAPEX",            f"${sp['capex']/1e6:.1f}M",          sub="gross investment"),
        kpi("Annual OPEX",               f"${sp['opex']/1e6:.2f}M / yr",      sub="recurring maintenance", cls="blue"),
        kpi("Gross Annual Savings",      f"${sp['savings']/1e6:.1f}M / yr",   sub="recurring / yr", cls="green"),
        kpi("Net Annual Benefit",        f"${sp['net_savings']/1e6:.1f}M / yr", sub="net cash flow / yr", cls="green"),
        kpi("Payback Period",            f"{sp['payback']:.2f} yrs",          sub="corporate payback", cls="green"),
        kpi("Annual Penalty Eliminated", f"${pen_saved/1e6:.1f}M / yr",       sub="statutory fine saved", cls="green"),
    ), unsafe_allow_html=True)

    pc1, pc2 = st.columns([1.2, 1.0])
    with pc1:
        sorted_pb = pb_df.sort_values("payback", ascending=True)
        fig_pb = px.bar(
            sorted_pb, y="short", x="payback", orientation="h",
            color="savings",
            color_continuous_scale=[[0,C_CYAN],[0.5,C_PURPLE],[1,C_GREEN]],
            text=sorted_pb["payback"].apply(lambda v: f"{v:.2f} yrs"),
            labels={"payback":"Payback Period (Years)","short":""},
        )
        fig_pb.update_traces(marker_line_width=0, opacity=0.88, textposition="outside",
                             textfont=dict(color=("#111827" if IS_LIGHT else "#ffffff"), size=12))
        fig_pb.update_layout(
            chart("Payback Period — 5 Strategic Playbooks", height=360, margin=dict(t=48, b=28, l=10, r=55)),
            yaxis=dict(gridcolor="rgba(100,116,139,0.1)" if not IS_LIGHT else "#e5e7eb", automargin=True),
            xaxis_title="",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_pb, width='stretch')

    with pc2:
        st.markdown(f"""
        <div class="glass-panel green" style="min-height:360px; height:auto;">
            <div class="section-pill">
                ⚙️ Engineering Blueprint
            </div>
            <p style="margin-bottom:0.6rem;">
                <span style="color:{C_CYAN if not IS_LIGHT else '#3b82f6'};font-weight:700;">Target:</span>
                <span style="color:{'#e2e8f0' if not IS_LIGHT else '#111827'};"> {sp['target']}</span>
            </p>
            <p style="margin-bottom:1rem;">
                <span style="color:{C_CYAN if not IS_LIGHT else '#3b82f6'};font-weight:700;">Strategy:</span>
                <span style="color:{'#cbd5e1' if not IS_LIGHT else '#4b5563'};"> {sp['desc']}</span>
            </p>
            <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,245,155,0.2),transparent);margin:0.75rem 0;"></div>
            <p style="font-size:0.85rem;color:#64748b;margin-bottom:0;">
                💡 <span style="color:{C_GREEN if not IS_LIGHT else '#10b981'};font-weight:600;">Self-Funding Model:</span>
                <span style="color:#94a3b8;"> Phase 1 (Surgical Strike — </span>
                <span style="color:{'#ffffff' if not IS_LIGHT else '#111827'};font-weight:600;">0.02 yr payback</span>
                <span style="color:#94a3b8;">) generates immediate cash flow to fund Phases 2 & 3.</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # CAPEX waterfall across all playbooks
    st.markdown(section_div(), unsafe_allow_html=True)
    st.markdown(pill("📊", "Portfolio-Wide Investment Overview"), unsafe_allow_html=True)

    tc1, tc2 = st.columns(2)
    with tc1:
        fig_capex = px.bar(
            pb_df.sort_values("capex"),
            y="short", x="capex", orientation="h",
            color="payback",
            color_continuous_scale=[[0,C_GREEN],[0.5,C_AMBER],[1,C_RED]],
            labels={"capex":"CAPEX ($)","short":""},
            text=pb_df.sort_values("capex")["capex"].apply(lambda v: f"${v/1e6:.0f}M"),
        )
        fig_capex.update_traces(marker_line_width=0, opacity=0.88, textposition="outside",
                                textfont=dict(color=("#111827" if IS_LIGHT else "#ffffff"), size=11))
        fig_capex.update_layout(
            chart("Required CAPEX by Playbook ($)", height=300, margin=dict(t=48, b=28, l=10, r=65)),
            yaxis=dict(automargin=True), xaxis_title="",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_capex, width='stretch')

    with tc2:
        total_capex   = pb_df["capex"].sum()
        total_opex    = pb_df["opex"].sum()
        total_savings = pb_df["savings"].sum()
        total_net     = pb_df["net_savings"].sum()
        avg_payback   = pb_df["payback"].mean()

        st.markdown(f"""
        <div class="glass-panel" style="min-height:300px; height:auto;">
            <div class="section-pill">🌍 Portfolio Investment Summary</div>
            {kpi_row(
                kpi("Total CAPEX (5 Playbooks)",  f"${total_capex/1e9:.2f}B",      sub="gross investment"),
                kpi("Total Annual OPEX",          f"${total_opex/1e6:.2f}M / yr",  sub="portfolio maintenance", cls="blue"),
            )}
            {kpi_row(
                kpi("Gross Annual Savings",       f"${total_savings/1e6:.1f}M / yr", sub="recurring savings", cls="green"),
                kpi("Net Annual Cash Flow",       f"${total_net/1e6:.1f}M / yr",     sub="net benefit / yr", cls="green"),
            )}
            {kpi_row(
                kpi("Blended Portfolio Payback",  "7.58 yrs",                      sub="blended capital return", cls="green"),
                kpi("Self-Fund Strategy",         "Phase 1 → 3",                   sub="0.02 yr → 12.25 yr"),
            )}
            <p style="font-size:0.82rem;color:#475569;margin-top:0.5rem;">
                💡 The <span style="color:{C_GREEN if not IS_LIGHT else '#10b981'};font-weight:600;">Self-Funding Model</span> means you don't need
                the full ${total_capex/1e9:.1f}B upfront — Phase 1 quick-wins generate liquidity to de-risk
                and fund deeper Phase 2 & 3 investments.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 5 — AI C-SUITE CO-PILOT & CHART BOT
# ══════════════════════════════════════════════════════════════
with tab5:
    st.markdown(section_div(), unsafe_allow_html=True)
    st.markdown(pill("🤖", "LL97 C-Suite AI Co-Pilot & Strategic Chart Scientist"), unsafe_allow_html=True)
    
    sub_color = "#374151" if IS_LIGHT else "#94a3b8"
    st.markdown(f"<p style='color:{sub_color};font-size:0.9rem;margin-top:-0.2rem;line-height:1.6;'>Executive AI Assistant trained on all <b>11,639 NYC properties</b>, statutory Local Law 97 formulas (<b>&dollar;268/MT CO₂e</b>), and the Executive <b>5 Decarbonization Playbooks</b>. Click any strategic button below for instant adaptive visualizations & executive intelligence.</p>", unsafe_allow_html=True)

    # Optional Live Generative AI Gemini configuration
    with st.expander("✨ Live Generative AI Mode (Google Gemini Integration - Optional)", expanded=False):
        st.markdown("<p style='font-size:0.85rem;color:#64748b;'>Connect your Google Gemini API Key to enable true generative AI reasoning, dynamic multi-lingual conversation (Arabic/English), and live C-Suite scenario analysis across the Local Law 97 database.</p>", unsafe_allow_html=True)
        key_col, _ = st.columns([2, 1])
        with key_col:
            user_gemini_key = st.text_input("🔑 Enter Gemini API Key (or set GEMINI_API_KEY in Streamlit Secrets):", type="password", key="gemini_key_input")

    # Determine active Gemini Key (user input or Streamlit Secrets)
    active_gemini_key = user_gemini_key.strip() if user_gemini_key else None
    if not active_gemini_key:
        try:
            active_gemini_key = st.secrets.get("GEMINI_API_KEY", None)
        except Exception:
            pass
        if not active_gemini_key:
            active_gemini_key = os.environ.get("GEMINI_API_KEY", None)

    if active_gemini_key:
        st.markdown("<div style='background:#ecfdf5;border:1px solid #10b981;color:#047857;padding:0.55rem 0.9rem;border-radius:10px;font-size:0.85rem;margin:0.4rem 0;'><b>✅ Live Google Gemini AI Connected!</b> Active Model: <code>gemini-2.5-flash</code>. Ask any natural language question below for live generative reasoning.</div>", unsafe_allow_html=True)

    # High-impact Executive Quick Prompt Buttons
    st.markdown("<div style='font-size:0.75rem;font-weight:700;color:#0ea5e9;text-transform:uppercase;letter-spacing:0.08em;margin:0.6rem 0;'>⚡ Strategic C-Suite Intelligence & Dynamic Visualizations</div>", unsafe_allow_html=True)
    qp1, qp2, qp3, qp4 = st.columns(4)
    quick_query = None
    with qp1:
        if st.button("🗺️ Plot 5-Phase Execution Roadmap", use_container_width=True):
            quick_query = "Plot the 5-Phase Strategic Decarbonization Execution Roadmap across timelines and milestones"
    with qp2:
        if st.button("📉 Plot 15-Year Net Cash Trajectory", use_container_width=True):
            quick_query = "Plot the cumulative Net Cash Flow and ROI trajectory over a 15-year horizon"
    with qp3:
        if st.button("⚖️ Plot Fine Reduction Waterfall", use_container_width=True):
            quick_query = "Plot the statutory LL97 Fine Reduction Waterfall across all 5 Playbooks starting from &dollar;2.83B baseline"
    with qp4:
        if st.button("📊 Compare CAPEX vs Net Benefit", use_container_width=True):
            quick_query = "Compare upfront CAPEX versus Net Annual Benefit across all 5 Decarbonization Playbooks"

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "assistant", "content": "Welcome to the **NYC Carbon Heist Mitigation AI C-Suite Co-Pilot**! 👋<br><br>I am your dedicated executive AI specialist. Ask me anything about our **11,639 audited properties**, **&dollar;4.98B CAPEX deployment**, **7.58-Year Payback**, or click any **Strategic Button above** to render interactive **Execution Roadmaps**, **15-Year Cash Flow Trajectories**, **Fine Reduction Waterfalls**, or **CAPEX vs Net Benefit Comparisons**."}
        ]

    # Handle quick query or input
    user_input = st.chat_input("Ask any executive question (e.g., hello, explain payback, show CAPEX breakdown)...")
    query_to_process = quick_query if quick_query else user_input

    if query_to_process and query_to_process.strip():
        st.session_state["chat_history"].append({"role": "user", "content": query_to_process})

        q_lower = query_to_process.lower().strip()
        response_text = ""
        chart_type = None

        # Check if button chart query
        if any(w in q_lower for w in ["roadmap", "timeline", "gantt", "execution", "schedule", "milestone", "5-phase"]):
            chart_type = "roadmap_gantt"
            response_text = """### 🗺️ Strategic 5-Phase Decarbonization Execution Roadmap

The interactive Gantt schedule below details the phased deployment across our **11,639 properties**. By sequencing interventions according to capital velocity, early quick-wins generate immediate liquidity to fund deeper Phase 3–5 structural retrofits:

* **Phase 1 · Surgical Strike (Y0.0 – Y0.5):** Rapid Level 2 audits and BMS setback scheduling across Top 10 offenders — **8-Day Payback &rarr; &dollar;20.55M/yr Net Cash Flow**
* **Phase 2 · Retro-commissioning (Y0.5 – Y2.0):** Comprehensive RCx & DDC upgrades on low-score assets — **&dollar;1.50/ft² &rarr; &dollar;240.37M/yr Net Cash Flow**
* **Phase 3 · 1960s Smart Scale (Y1.5 – Y4.0):** Networked LED lighting & VFD motor retrofits — **&dollar;2.50/ft² &rarr; &dollar;85.23M/yr Net Cash Flow**
* **Phase 4 · 1930s WET Systems (Y3.0 – Y6.0):** Historic sewer wastewater heat recovery leveraging **50% PPP Grants (&dollar;749M)** — **12.25 Yr Payback &rarr; &dollar;117.89M/yr Net Cash Flow**
* **Phase 5 · Electrification Push (Y5.0 – Y8.0):** Complete replacement of Fuel Oil #4 boilers with Electric Heat Pumps — **10.38 Yr Payback &rarr; &dollar;176.89M/yr Net Cash Flow**
"""
        elif any(w in q_lower for w in ["trajectory", "15-year", "cumulative", "cash flow", "horizon"]):
            chart_type = "cash_trajectory"
            response_text = """### 📉 15-Year Cumulative Net Cash Flow & ROI Trajectory

The adaptive area chart below illustrates the self-funding financial cascade over a 15-year horizon. After achieving full blended capital recovery at **Year 7.58**, the portfolio generates exponential positive net operational surpluses, accumulating over **&dollar;4.63 Billion in cumulative net savings** by Year 15.
"""
        elif any(w in q_lower for w in ["waterfall", "reduction", "eliminated", "liability cascade", "starting from"]):
            chart_type = "fine_waterfall"
            response_text = """### ⚖️ LL97 Statutory Fine Reduction Waterfall

The step-down waterfall chart below starts at our unmitigated baseline liability (**&dollar;2.83 Billion/year** evaluated at **&dollar;268/MT CO₂e**) and demonstrates how each individual decarbonization playbook systematically strips away statutory penalties, generating **&dollar;656.63 Million/yr** in gross annual reductions.
"""
        elif any(w in q_lower for w in ["compare capex", "capex vs", "net benefit", "comparison", "playbooks"]):
            chart_type = "playbooks_comp"
            response_text = """### 📊 Strategic Comparison: Initial CAPEX vs. Net Annual Benefit

The grouped comparison chart below benchmarks upfront capital expenditure against recurring annual net cash flow across each of the 5 Strategic Playbooks:
* **Playbook 01 (Surgical Strike):** Minimal **&dollar;500K CAPEX** unlocks **&dollar;20.55M/yr** recurring net benefit (**0.02 Yr Payback**).
* **Playbook 02 (Retro-commissioning):** **&dollar;802.17M CAPEX** yields **&dollar;240.37M/yr** recurring net benefit (**3.29 Yr Payback**).
* **Total Portfolio Performance:** **&dollar;4.98B CAPEX** yields **&dollar;640.93M/yr Net Recurring Cash Flow** (**7.58 Yr Blended Payback**).
"""
        elif any(w in q_lower for w in ["borough", "manhattan", "brooklyn", "queens", "bronx", "staten", "emissions per", "boroughs"]):
            chart_type = "borough_emissions"
            response_text = """### 🏙️ NYC Borough Carbon Emissions & LL97 Liability Breakdown

Across our audited **11,639 properties**, annual carbon emissions (**10.56M MT CO₂e/yr**) and statutory fine liability (**&dollar;2.83 Billion/yr**) are distributed across the 5 boroughs as shown in the interactive chart below:
* **Manhattan:** 4,821 properties (41.4%) &rarr; **4.96M MT CO₂e/yr** (&dollar;1.33B/yr penalty)
* **Brooklyn:** 3,142 properties (27.0%) &rarr; **2.43M MT CO₂e/yr** (&dollar;650.9M/yr penalty)
* **Queens:** 2,211 properties (19.0%) &rarr; **1.90M MT CO₂e/yr** (&dollar;509.4M/yr penalty)
* **Bronx:** 1,164 properties (10.0%) &rarr; **0.95M MT CO₂e/yr** (&dollar;254.7M/yr penalty)
* **Staten Island:** 301 properties (2.6%) &rarr; **0.32M MT CO₂e/yr** (&dollar;84.9M/yr penalty)
"""
        elif any(w in q_lower for w in ["capex breakdown", "capex allocation", "playbook cost", "itemized capex"]):
            chart_type = "capex_breakdown"
            response_text = """### 💰 Itemized Portfolio CAPEX Allocation (&dollar;4.98 Billion)

The interactive visualization below illustrates the distribution of capital expenditure across our 5 Decarbonization Playbooks:
* **Playbook 01 (Surgical Strike):** &dollar;500,000 (0.01%)
* **Playbook 02 (Retro-commissioning):** &dollar;802.17 Million (16.1%)
* **Playbook 03 (1960s Smart Scale):** &dollar;785.24 Million (15.8%)
* **Playbook 04 (1930s WET Systems):** &dollar;1.50 Billion Net CAPEX (30.1%)
* **Playbook 05 (Electrification Push):** &dollar;1.89 Billion (38.0%)
"""
        else:
            # If Gemini AI key is available, invoke true Generative AI reasoning via direct REST API
            gemini_succeeded = False
            if active_gemini_key:
                try:
                    with st.spinner("🧠 Gemini 2.5 Flash is thinking..."):
                        ai_reply = call_gemini_ai(query_to_process, active_gemini_key, GEMINI_SYSTEM_PROMPT)
                    response_text = ai_reply + "<br><br><span style='font-size:0.75rem;color:#0ea5e9;font-weight:600;'>✨ Generated live by Google Gemini 2.5 Flash</span>"
                    gemini_succeeded = True
                    # Dynamically attach adaptive chart if query implies a graph or specific dimension
                    if any(w in q_lower for w in ["borough", "manhattan", "brooklyn", "queens", "bronx", "staten"]):
                        chart_type = "borough_emissions"
                    elif any(w in q_lower for w in ["capex", "cost breakdown", "allocation"]):
                        chart_type = "capex_breakdown"
                    elif any(w in q_lower for w in ["payback", "roi", "compare"]):
                        chart_type = "playbooks_comp"
                    elif any(w in q_lower for w in ["waterfall", "fine", "penalty"]):
                        chart_type = "fine_waterfall"
                    elif any(w in q_lower for w in ["roadmap", "timeline", "gantt"]):
                        chart_type = "roadmap_gantt"
                    elif any(w in q_lower for w in ["graph", "chart", "plot", "visualize", "رسم", "مخطط"]):
                        chart_type = "borough_emissions"
                except Exception as e:
                    error_banner = f"<div style='background:#fef2f2;border:1px solid #ef4444;color:#991b1b;padding:0.6rem;border-radius:8px;font-size:0.82rem;margin-bottom:0.6rem;'><b>⚠️ Gemini API Error:</b> {str(e)}<br><i>Showing Executive Quantitative Database fallback below:</i></div>"
            
            # Fallback high-precision analytical responses if no API key or Gemini failed
            if not gemini_succeeded:
                prefix = error_banner if active_gemini_key and "error_banner" in locals() else ""
                if q_lower in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "howdy", "hola", "hi there", "hello there", "مرحبا", "اهلا", "سلام"]:
                    response_text = """### 👋 Hello! Welcome to the Executive C-Suite Co-Pilot

I am your dedicated AI Decarbonization Specialist trained on NYC's **11,639 audited properties** and Local Law 97 statutory frameworks.

**How can I assist your executive team today?**
* 💡 Ask me to explain our **Self-Funding Strategy** or **7.58-Year Blended Payback**.
* 📊 Ask about our **&dollar;4.98B CAPEX** or **&dollar;640.93M/yr Net Annual Cash Flow**.
* 🗺️ Or click any of the **4 Strategic Buttons above** to dynamically render our Gantt Execution Roadmap, 15-Year Cash Trajectory, Fine Reduction Waterfall, or CAPEX Comparison chart!
"""
                elif any(w in q_lower for w in ["payback", "roi", "return", "breakeven", "self-funding"]):
                    response_text = """### ⏱️ Portfolio Payback Period & Self-Funding Financial Structure

Our executive master plan delivers a **Blended Portfolio Payback Period of exactly 7.58 Years**.

**How the Self-Funding Cascade Works:**
* **Phase 1 (Surgical Strike):** Recovers capital in just **8 Days (0.02 Years)**, instantly injecting **&dollar;20.55M/yr** in liquid net cash flow.
* **Phase 2 (Retro-commissioning):** Recovers capital in **3.29 Years**, adding **&dollar;240.37M/yr** in net recurring operational surpluses.
* This early liquidity directly underwrites and de-risks the heavier structural retrofits in Phases 3, 4, and 5.
"""
                elif any(w in q_lower for w in ["capex", "cost", "investment", "upfront", "capital"]):
                    response_text = """### 💰 Itemized Portfolio CAPEX Breakdown

The total required capital investment across all **11,639 properties** is **&dollar;4.98 Billion**, structured across 5 targeted deployment playbooks:
1. **01 · Surgical Strike:** &dollar;500,000 CAPEX
2. **02 · Retro-commissioning:** &dollar;802.17 Million CAPEX
3. **03 · 1960s Smart Scale:** &dollar;785.24 Million CAPEX
4. **04 · 1930s WET Systems:** &dollar;1.50 Billion Net CAPEX (after 50% PPP Grants)
5. **05 · Electrification Push:** &dollar;1.89 Billion CAPEX
"""
                elif any(w in q_lower for w in ["opex", "maintenance", "net benefit", "net savings", "recurring"]):
                    response_text = """### 📈 Itemized Annual OPEX & Net Annual Cash Flow

Every playbook accounts for annual operational and maintenance costs (OPEX) to ensure true executive net metrics:
* **Gross Annual Financial & Utility Savings:** &dollar;656.63 Million / yr
* **Total Annual OPEX & Maintenance:** &dollar;15.70 Million / yr
* **Net Annual Cash Flow (Net Benefit):** **&dollar;640.93 Million / yr**
"""
                elif any(w in q_lower for w in ["fines", "penalty", "penalties", "law", "ll97", "statutory"]):
                    response_text = """### ⚖️ Local Law 97 Statutory Liability & Mitigation

Under NYC Local Law 97, buildings exceeding carbon emissions thresholds face strict statutory penalties evaluated at **&dollar;268 per Metric Ton of CO₂ equivalent (&dollar;268/MT CO₂e)**.
* **Unmitigated Baseline Portfolio Fine Exposure:** **&dollar;2.83 Billion / year**
* **Total Fines Eliminated via 5 Playbooks:** **&dollar;656.63 Million / year** recurring savings
"""
                else:
                    response_text = f"""### 🤖 Executive C-Suite Analysis: `{query_to_process}`

Based on your query, here is our quantitative portfolio assessment across our verified Local Law 97 database:
* **Portfolio Assets:** 11,639 audited properties across NYC's 5 boroughs.
* **Baseline Statutory Liability:** **&dollar;2.83 Billion/year** (evaluated at **&dollar;268/MT CO₂e**).
* **Blended Strategy Execution:** Combined CAPEX of **&dollar;4.98 Billion** generates **&dollar;656.63 Million/yr** in gross savings and **&dollar;640.93 Million/yr in Net Annual Cash Flow** after itemized OPEX (**&dollar;15.70M/yr**).
* **Blended Portfolio Payback:** **7.58 Years** across all 5 Decarbonization Playbooks.

💡 *Tip: Connect a Google Gemini API key above for live Generative AI reasoning, or click any prompt button to render interactive charts.*
"""

        if not gemini_succeeded and "error_banner" in locals():
            response_text = error_banner + response_text

        st.session_state["chat_history"].append({"role": "assistant", "content": response_text, "chart": chart_type})

    # Adaptive Theme Backgrounds
    bg_paper = "rgba(255, 255, 255, 0.85)" if IS_LIGHT else "rgba(15, 23, 42, 0.75)"
    bg_plot  = "rgba(248, 250, 252, 0.6)"  if IS_LIGHT else "rgba(15, 23, 42, 0.4)"

    # Display newest responses directly under the prompt/input box always
    for idx, msg in enumerate(reversed(st.session_state["chat_history"])):
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            content_text = msg["content"]
            
            # Check if Gemini generated a universal dynamic plotly_json chart block
            gemini_custom_chart = None
            if "```plotly_json" in content_text:
                try:
                    parts = content_text.split("```plotly_json")
                    display_text = parts[0]
                    json_raw = parts[1].split("```")[0].strip()
                    gemini_custom_chart = json.loads(json_raw)
                    st.markdown(display_text, unsafe_allow_html=True)
                except Exception:
                    st.markdown(content_text, unsafe_allow_html=True)
            else:
                st.markdown(content_text, unsafe_allow_html=True)

            # Render custom Gemini AI generated chart if present
            if gemini_custom_chart and isinstance(gemini_custom_chart, dict):
                try:
                    c_title = gemini_custom_chart.get("title", "AI Dynamic Executive Chart")
                    c_type = gemini_custom_chart.get("chart_type", "bar")
                    x_vals = gemini_custom_chart.get("x", [])
                    y_vals = gemini_custom_chart.get("y", [])
                    x_lbl = gemini_custom_chart.get("x_label", "Category")
                    y_lbl = gemini_custom_chart.get("y_label", "Value")
                    
                    if x_vals and y_vals and len(x_vals) == len(y_vals):
                        df_custom = pd.DataFrame({x_lbl: x_vals, y_lbl: y_vals})
                        if c_type == "pie":
                            fig_ai = px.pie(df_custom, names=x_lbl, values=y_lbl, hole=0.5, color_discrete_sequence=[C_CYAN, C_GREEN, C_BLUE, C_PURPLE, C_AMBER])
                            fig_ai.update_traces(textposition="inside", textinfo="percent+label")
                        elif c_type == "hbar":
                            fig_ai = px.bar(df_custom, x=y_lbl, y=x_lbl, orientation="h", color=x_lbl, color_discrete_sequence=[C_CYAN, C_GREEN, C_BLUE, C_PURPLE, C_AMBER])
                        elif c_type == "line":
                            fig_ai = px.line(df_custom, x=x_lbl, y=y_lbl, markers=True, color_discrete_sequence=[C_CYAN])
                        else:
                            fig_ai = px.bar(df_custom, x=x_lbl, y=y_lbl, color=x_lbl, color_discrete_sequence=[C_CYAN, C_GREEN, C_BLUE, C_PURPLE, C_AMBER])
                        
                        fig_ai.update_layout(
                            chart(c_title, height=380),
                            paper_bgcolor=bg_paper,
                            plot_bgcolor=bg_plot,
                            showlegend=False
                        )
                        st.plotly_chart(fig_ai, width='stretch', theme=None, key=f"chat_chart_{idx}_custom_ai")
                except Exception:
                    pass
            
            chart_t = msg.get("chart")
            if chart_t == "roadmap_gantt":
                roadmap_df = pd.DataFrame([
                    {"Playbook": "01 · Surgical Strike",      "Start": "2026-01-01", "End": "2026-07-01", "CAPEX": "$500 K",    "Net_Savings": "$20.55M/yr", "Payback": "8 Days"},
                    {"Playbook": "02 · Retro-commissioning",  "Start": "2026-07-01", "End": "2028-01-01", "CAPEX": "$802.17M",  "Net_Savings": "$240.37M/yr","Payback": "3.29 Yrs"},
                    {"Playbook": "03 · 1960s Smart Scale",    "Start": "2027-06-01", "End": "2030-01-01", "CAPEX": "$785.24M",  "Net_Savings": "$85.23M/yr", "Payback": "8.92 Yrs"},
                    {"Playbook": "04 · 1930s WET Systems",    "Start": "2029-01-01", "End": "2032-01-01", "CAPEX": "$1.50B Net","Net_Savings": "$117.89M/yr","Payback": "12.25 Yrs"},
                    {"Playbook": "05 · Electrification Push", "Start": "2031-01-01", "End": "2034-01-01", "CAPEX": "$1.89B",    "Net_Savings": "$176.89M/yr","Payback": "10.38 Yrs"}
                ])
                fig_r = px.timeline(
                    roadmap_df, x_start="Start", x_end="End", y="Playbook",
                    color="Playbook",
                    color_discrete_sequence=[C_GREEN, C_CYAN, C_AMBER, C_PURPLE, C_RED],
                    hover_data=["CAPEX", "Net_Savings", "Payback"]
                )
                fig_r.update_yaxes(autorange="reversed")
                fig_r.update_layout(
                    chart("NYC Portfolio 8-Year Master Execution Roadmap (Gantt Schedule)", height=380),
                    paper_bgcolor=bg_paper,
                    plot_bgcolor=bg_plot,
                    showlegend=False
                )
                st.plotly_chart(fig_r, width='stretch', theme=None, key=f"chat_chart_{idx}_roadmap")

            elif chart_t == "cash_trajectory":
                years = list(range(0, 16))
                cum_net = []
                net_savings_yr = 640_932_287
                for y in years:
                    if y == 0:
                        cum_net.append(-4_976_800_628)
                    else:
                        cum_net.append(cum_net[-1] + net_savings_yr)
                traj_df = pd.DataFrame({"Year": [f"Year {y}" for y in years], "Cumulative Net Cash Flow ($)": cum_net})
                fig_t = px.area(
                    traj_df, x="Year", y="Cumulative Net Cash Flow ($)",
                    color_discrete_sequence=[C_GREEN]
                )
                fig_t.add_hline(y=0, line_dash="dash", line_color="#ef4444", annotation_text="Breakeven Threshold (Year 7.58)")
                fig_t.update_layout(
                    chart("15-Year Cumulative Net Cash Flow Trajectory (Breakeven at Year 7.58)", height=380),
                    paper_bgcolor=bg_paper,
                    plot_bgcolor=bg_plot
                )
                st.plotly_chart(fig_t, width='stretch', theme=None, key=f"chat_chart_{idx}_traj")

            elif chart_t == "fine_waterfall":
                fig_w = go.Figure(go.Waterfall(
                    name="LL97 Penalty Reduction",
                    orientation="v",
                    measure=["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
                    x=[
                        "Baseline Fine ($2.83B)",
                        "01 · Surgical Strike",
                        "02 · Retro-commissioning",
                        "03 · 1960s Smart Scale",
                        "04 · 1930s WET Systems",
                        "05 · Electrification Push",
                        "Gross Annual Savings"
                    ],
                    textposition="outside",
                    text=["$2.83B Baseline", "-$20.6M", "-$243.6M", "-$88.0M", "-$122.4M", "-$182.0M", "$656.6M Total Saved"],
                    y=[2830683648, -20594117, -243615631, -88033696, -122390647, -181993196, 656626287],
                    connector={"line": {"color": "rgba(148, 163, 184, 0.35)", "width": 1.5, "dash": "dot"}},
                    decreasing={"marker": {"color": "#10b981"}},
                    increasing={"marker": {"color": "#ef4444"}},
                    totals={"marker": {"color": "#0ea5e9"}}
                ))
                fig_w.update_layout(
                    chart("LL97 Statutory Fine Reduction Waterfall: Baseline Liability vs Playbook Savings", height=400),
                    paper_bgcolor=bg_paper,
                    plot_bgcolor=bg_plot,
                    showlegend=False
                )
                st.plotly_chart(fig_w, width='stretch', theme=None, key=f"chat_chart_{idx}_wf")

            elif chart_t == "playbooks_comp":
                pb_comp_df = pd.DataFrame(PLAYBOOKS)
                fig_c = px.bar(
                    pb_comp_df, x="short", y=["capex", "net_savings"],
                    barmode="group",
                    labels={"value": "USD ($)", "short": "Decarbonization Playbook", "variable": "Metric"},
                    color_discrete_map={"capex": C_CYAN, "net_savings": C_GREEN}
                )
                fig_c.update_layout(
                    chart("Strategic Comparison: Initial CAPEX vs Net Annual Benefit ($/yr)", height=380),
                    paper_bgcolor=bg_paper,
                    plot_bgcolor=bg_plot,
                    legend_title_text=""
                )
                st.plotly_chart(fig_c, width='stretch', theme=None, key=f"chat_chart_{idx}_comp")

            elif chart_t == "borough_emissions":
                borough_data = pd.DataFrame([
                    {"Borough": "Manhattan",     "Properties": 4821, "Emissions_MT": 4963059, "Annual_Fine_USD": 1330099812},
                    {"Borough": "Brooklyn",      "Properties": 3142, "Emissions_MT": 2428731, "Annual_Fine_USD": 650899908},
                    {"Borough": "Queens",        "Properties": 2211, "Emissions_MT": 1900746, "Annual_Fine_USD": 509399928},
                    {"Borough": "Bronx",         "Properties": 1164, "Emissions_MT": 950373,  "Annual_Fine_USD": 254699964},
                    {"Borough": "Staten Island", "Properties": 301,  "Emissions_MT": 316791,  "Annual_Fine_USD": 84900388}
                ])
                fig_b = px.bar(
                    borough_data, x="Emissions_MT", y="Borough", orientation="h",
                    color="Borough",
                    text_auto=".2s",
                    labels={"Emissions_MT": "Annual Carbon Emissions (MT CO₂e/yr)", "Borough": "NYC Borough"},
                    color_discrete_sequence=[C_CYAN, C_BLUE, C_PURPLE, C_AMBER, C_GREEN]
                )
                fig_b.update_layout(
                    chart("NYC Borough Carbon Emissions & Statutory Fine Exposure ($2.83B Total)", height=370),
                    paper_bgcolor=bg_paper,
                    plot_bgcolor=bg_plot,
                    showlegend=False
                )
                st.plotly_chart(fig_b, width='stretch', theme=None, key=f"chat_chart_{idx}_boro")

            elif chart_t == "capex_breakdown":
                capex_df = pd.DataFrame(PLAYBOOKS)
                fig_cx = px.pie(
                    capex_df, names="short", values="capex", hole=0.55,
                    color_discrete_sequence=[C_GREEN, C_CYAN, C_BLUE, C_PURPLE, C_AMBER]
                )
                fig_cx.update_traces(textposition="inside", textinfo="percent+label")
                fig_cx.update_layout(
                    chart("Itemized Portfolio CAPEX Allocation ($4.98 Billion Total)", height=380),
                    paper_bgcolor=bg_paper,
                    plot_bgcolor=bg_plot
                )
                st.plotly_chart(fig_cx, width='stretch', theme=None, key=f"chat_chart_{idx}_cx")
