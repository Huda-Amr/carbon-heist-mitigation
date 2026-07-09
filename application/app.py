import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import sys
from pathlib import Path

# ==========================================
# PAGE CONFIGURATION Using CSS
# ==========================================
st.set_page_config(
    page_title="ESG & Carbon Mitigation Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded" 
)

COLOR_GREEN = "#00F59B"  
COLOR_RED = "#FF4B6E"    
COLOR_ORANGE = "#FFB800" 
COLOR_BLUE = "#00D2FF"   
COLOR_PURPLE = "#A855F7"
COLOR_BG = "#060b18"     
COLOR_CARD = "#0f1729"   

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ===== GLOBAL CANVAS ===== */
    .stApp {{
        background: linear-gradient(135deg, #060b18 0%, #0c1225 30%, #0a0f1f 60%, #060b18 100%);
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Subtle animated mesh overlay */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: 
            radial-gradient(ellipse at 20% 50%, rgba(0, 210, 255, 0.04) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(168, 85, 247, 0.04) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 80%, rgba(0, 245, 155, 0.03) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }}

    /* ===== TYPOGRAPHY ===== */
    h1 {{
        background: linear-gradient(135deg, #00D2FF 0%, #A855F7 50%, #00F59B 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-weight: 800 !important;
        font-size: 2.4rem !important;
        letter-spacing: -0.03em;
    }}
    h2, h3 {{
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }}
    h4 {{
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }}
    
    /* ===== KPI CARDS - PREMIUM GLASS ===== */
    .kpi-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 2rem;
    }}
    .kpi-card {{
        background: linear-gradient(145deg, rgba(15, 23, 41, 0.85), rgba(15, 23, 41, 0.6));
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 1.4rem 1.5rem;
        flex: 1;
        min-width: 165px;
        box-shadow: 
            0 4px 30px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border-top: 3px solid {COLOR_BLUE};
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    .kpi-card::after {{
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 200%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent);
        transition: left 0.6s ease;
    }}
    .kpi-card:hover::after {{
        left: 100%;
    }}
    .kpi-card:hover {{
        transform: translateY(-6px) scale(1.01);
        box-shadow: 
            0 20px 40px rgba(0, 210, 255, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
        border-color: rgba(0, 210, 255, 0.2);
    }}
    .kpi-card.risk {{ border-top-color: {COLOR_RED}; }}
    .kpi-card.risk:hover {{ box-shadow: 0 20px 40px rgba(255, 75, 110, 0.15), inset 0 1px 0 rgba(255,255,255,0.08); }}
    .kpi-card.good {{ border-top-color: {COLOR_GREEN}; }}
    .kpi-card.good:hover {{ box-shadow: 0 20px 40px rgba(0, 245, 155, 0.15), inset 0 1px 0 rgba(255,255,255,0.08); }}
    
    .kpi-title {{
        font-size: 0.72rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    .kpi-value {{
        font-size: 1.65rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}
    
    /* ===== TAB BAR ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        background: linear-gradient(135deg, rgba(15, 23, 41, 0.7), rgba(15, 23, 41, 0.5));
        backdrop-filter: blur(12px);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 12px;
        padding: 10px 18px;
        color: #64748b;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: #94a3b8;
        background-color: rgba(255, 255, 255, 0.03);
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, rgba(0, 210, 255, 0.15), rgba(168, 85, 247, 0.1)) !important;
        color: #00D2FF !important;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.1);
    }}
    
    /* ===== EXECUTIVE PANELS ===== */
    .exec-panel {{
        background: linear-gradient(145deg, rgba(15, 23, 41, 0.85), rgba(15, 23, 41, 0.55));
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 1.8rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        border-left: 3px solid {COLOR_BLUE};
    }}
    .exec-panel h3, .exec-panel h4 {{
        background: linear-gradient(135deg, #00D2FF, #A855F7) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 0.8rem;
    }}
    .exec-panel p {{
        color: #cbd5e1;
        line-height: 1.7;
        font-size: 0.95rem;
    }}
    .exec-panel b {{
        color: #ffffff;
    }}
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0c1225 0%, #080e1c 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }}
    [data-testid="stSidebar"] .stMarkdown h3 {{
        font-size: 0.9rem;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    
    /* ===== WIDGETS ===== */
    .stSlider > div > div > div > div {{
        background: linear-gradient(90deg, {COLOR_BLUE}, {COLOR_PURPLE}) !important;
    }}
    /* Slider thumb */
    .stSlider [role="slider"] {{
        background-color: #ffffff !important;
        border-color: #ffffff !important;
        box-shadow: 0 0 8px rgba(0, 210, 255, 0.4) !important;
    }}
    /* Slider thumb value tooltip */
    .stSlider [data-testid="stThumbValue"],
    .stSlider [role="slider"] > div {{
        background-color: {COLOR_CARD} !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }}
    /* Kill the default Streamlit blue on ALL focused/active inputs */
    .stSlider > div > div > div > div > div {{
        background-color: transparent !important;
    }}
    input:focus, textarea:focus, [data-baseweb] *:focus {{
        border-color: rgba(0, 210, 255, 0.4) !important;
        box-shadow: 0 0 0 1px rgba(0, 210, 255, 0.2) !important;
    }}
    /* Number input and text input */
    .stNumberInput input, .stTextInput input {{
        background-color: rgba(15, 23, 41, 0.8) !important;
        border-color: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }}
    /* Selectbox and Multiselect */
    .stSelectbox > div > div, .stMultiSelect > div > div {{
        background-color: rgba(15, 23, 41, 0.8) !important;
        border-color: rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
    }}
    /* Dropdown menus */
    [data-baseweb="popover"] {{
        background-color: {COLOR_CARD} !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
    }}
    [data-baseweb="popover"] li:hover {{
        background-color: rgba(0, 210, 255, 0.1) !important;
    }}
    /* Override BaseWeb primary color (the ugly blue) */
    [data-baseweb] {{
        --primary: {COLOR_BLUE} !important;
        --primary400: {COLOR_BLUE} !important;
    }}
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {{
        color: #94a3b8 !important;
        font-weight: 600;
        font-size: 0.9rem;
    }}
    .streamlit-expanderContent {{
        background: rgba(15, 23, 41, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 0 0 14px 14px;
    }}
    
    /* ===== METRICS DELTA ===== */
    [data-testid="stMetricDelta"] {{
        font-weight: 600;
    }}
    
    /* ===== DIVIDERS ===== */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 210, 255, 0.2), rgba(168, 85, 247, 0.2), transparent);
        margin: 2rem 0;
    }}
    
    /* ===== IMAGE HEADERS ===== */
    .header-image {{
        border-radius: 18px;
        margin-bottom: 1.5rem;
        object-fit: cover;
        width: 100%;
        height: 200px;
        opacity: 0.8;
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }}
    
    /* ===== FORMS ===== */
    [data-testid="stForm"] {{
        background: rgba(15, 23, 41, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 1.5rem;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, {COLOR_BLUE}, {COLOR_PURPLE}) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.25) !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 210, 255, 0.35) !important;
    }}
    
    /* ===== BOLD TEXT VISIBILITY ===== */
    b, strong {{
        color: #ffffff !important;
        font-weight: 700;
    }}
    .exec-panel b, .exec-panel strong {{
        color: #00D2FF !important;
    }}
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(100, 116, 139, 0.3); border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(100, 116, 139, 0.5); }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# ML MODEL SETUP
# ==========================================
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
        fallback_diagnosis = ["Diagnostic engine unavailable: could not import 'models/ll97_playground.py'."]
        fallback_recommendations = ["Verify that 'models/ll97_playground.py' exists and is importable."]
        return fallback_diagnosis, fallback_recommendations, 0.0

# ==========================================
# DATA HANDLING 
# ==========================================
@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "results.csv"
    
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'results.csv' is in the directory.")
        st.stop()

    numeric_targets = [
        "Total GHG Emissions (Metric Tons CO2e)", "Net Emissions (Metric Tons CO2e)",
        "Base LL97 Penalty", "ENERGY STAR Score", "Building Age", "Year Built",
        "Total GHG Emissions Intensity (kgCO2e/ft²)", 
        "Avoided Emissions - Onsite and Offsite Green Power (Metric Tons CO2e)",
        "Electricity Use - Grid Purchase (kBtu)", "Natural Gas Use (kBtu)",
        "District Steam Use (kBtu)", "Fuel Oil #2 Use (kBtu)", "Diesel #2 Use (kBtu)"
    ]
    
    for col in numeric_targets:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Recalculate LL97 Penalty on Total GHG (not just excess)
    if "Total GHG Emissions (Metric Tons CO2e)" in df.columns:
        df["Base LL97 Penalty"] = df["Total GHG Emissions (Metric Tons CO2e)"] * 268

    if "Year Built" in df.columns and "Building Age" not in df.columns:
        df["Building Age"] = 2026 - df["Year Built"]
        
    if "Year Built" in df.columns:
        df["Decade Built"] = (df["Year Built"] // 10) * 10
        
    return df

raw_df = load_data()

C_NAME = "Property Name"
C_GHG = "Total GHG Emissions (Metric Tons CO2e)"
C_NET = "Net Emissions (Metric Tons CO2e)"
C_PENALTY = "Base LL97 Penalty"
C_SCORE = "ENERGY STAR Score"
C_INTENSITY = "Total GHG Emissions Intensity (kgCO2e/ft²)"
C_AVOIDED = "Avoided Emissions - Onsite and Offsite Green Power (Metric Tons CO2e)" # <--- ADD THIS LINE
C_TYPE = "Primary Property Type - Portfolio Manager-Calculated"
C_BORO = "Borough"
C_CITY = "City"
C_AGE = "Building Age"
C_DECADE = "Decade Built"
C_ALERTS = "Alerts"
C_OCCUPANCY = "Occupancy"
C_CONSTRUCTION = "Construction Status"

# ==========================================
# SIDEBAR & ADVANCED FILTERS
# ==========================================
st.sidebar.image("https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?q=80&w=600&auto=format&fit=crop", caption="ESG Data Hub")
st.sidebar.title("🌍 Global Filters")


with st.sidebar.expander("📍 Location Filters", expanded=False):
    sel_cities = st.multiselect("City", raw_df[C_CITY].dropna().unique() if C_CITY in raw_df.columns else [])
    sel_boros = st.multiselect("Borough", raw_df[C_BORO].dropna().unique() if C_BORO in raw_df.columns else [])

with st.sidebar.expander("🏢 Property Details", expanded=False):
    sel_types = st.multiselect("Primary Property Type", raw_df[C_TYPE].dropna().unique() if C_TYPE in raw_df.columns else [])
    sel_decades = st.multiselect("Decade Built", sorted(raw_df[C_DECADE].dropna().unique()) if C_DECADE in raw_df.columns else [])
    sel_occ = st.multiselect("Occupancy Status", raw_df[C_OCCUPANCY].dropna().unique() if C_OCCUPANCY in raw_df.columns else [])
    sel_const = st.multiselect("Construction Status", raw_df[C_CONSTRUCTION].dropna().unique() if C_CONSTRUCTION in raw_df.columns else [])
    
    if C_AGE in raw_df.columns:
        age_min, age_max = int(raw_df[C_AGE].min()), int(raw_df[C_AGE].max())
    else:
        age_min, age_max = 0, 100
    sel_age = st.slider("Building Age Range", age_min, age_max, (age_min, age_max))

with st.sidebar.expander("📈 Performance & Risk", expanded=False):
    score_min, score_max = 0, 100
    sel_score = st.slider("ENERGY STAR Score", score_min, score_max, (score_min, score_max))
    
    if C_GHG in raw_df.columns:
        ghg_min, ghg_max = float(raw_df[C_GHG].min()), float(raw_df[C_GHG].max())
    else:
        ghg_min, ghg_max = 0.0, 1000.0
    sel_ghg = st.slider("GHG Emissions (tCO₂e)", ghg_min, ghg_max, (ghg_min, ghg_max))
    
    if C_PENALTY in raw_df.columns:
        pen_min, pen_max = float(raw_df[C_PENALTY].min()), float(raw_df[C_PENALTY].max())
    else:
        pen_min, pen_max = 0.0, 1000000.0
    sel_pen = st.slider("LL97 Penalty ($)", pen_min, pen_max, (pen_min, pen_max))

with st.sidebar.expander("⚠️ Data Quality", expanded=False):
    exc_alerts = st.multiselect("Exclude Properties with Alerts", 
                                ['Energy Meter Gaps', 'Missing Energy Meters', 'Less than 12 Months of Data'])

search_term = st.sidebar.text_input("🔍 Search Property Name", "")

# --- Apply Filters ---
df = raw_df.copy()

if search_term and C_NAME in df.columns:
    df = df[df[C_NAME].str.contains(search_term, case=False, na=False)]
if sel_cities and C_CITY in df.columns:
    df = df[df[C_CITY].isin(sel_cities)]
if sel_boros and C_BORO in df.columns:
    df = df[df[C_BORO].isin(sel_boros)]
if sel_types and C_TYPE in df.columns:
    df = df[df[C_TYPE].isin(sel_types)]
if sel_decades and C_DECADE in df.columns:
    df = df[df[C_DECADE].isin(sel_decades)]
if sel_occ and C_OCCUPANCY in df.columns:
    df = df[df[C_OCCUPANCY].isin(sel_occ)]
if sel_const and C_CONSTRUCTION in df.columns:
    df = df[df[C_CONSTRUCTION].isin(sel_const)]
if C_AGE in df.columns:
    df = df[df[C_AGE].between(sel_age[0], sel_age[1])]
if C_SCORE in df.columns:
    df = df[df[C_SCORE].fillna(0).between(sel_score[0], sel_score[1])]
if C_GHG in df.columns:
    df = df[df[C_GHG].between(sel_ghg[0], sel_ghg[1])]
if C_PENALTY in df.columns:
    df = df[df[C_PENALTY].between(sel_pen[0], sel_pen[1])]
if exc_alerts and C_ALERTS in df.columns:
    df = df[~df[C_ALERTS].isin(exc_alerts)]


# ==========================================
# HELPER FUNCTIONS 
# ==========================================
def get_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(size=15, color="#ffffff", family="Inter")),
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=30, l=30, r=30),
        font=dict(color="#94a3b8", family="Inter"),
        xaxis=dict(gridcolor="rgba(100,116,139,0.1)", zerolinecolor="rgba(100,116,139,0.15)"),
        yaxis=dict(gridcolor="rgba(100,116,139,0.1)", zerolinecolor="rgba(100,116,139,0.15)")
    )

def plot_horizontal_bar(data, x, y, title, color_hex, hover_cols=None):
    fig = px.bar(data, x=x, y=y, orientation='h', hover_data=hover_cols)
    fig.update_traces(
        marker_color=color_hex,
        marker_line_width=0,
        opacity=0.9
    )
    fig.update_layout(get_layout(title), yaxis={'categoryorder':'total ascending'})
    return fig


@st.cache_resource
def load_ml_assets():
    """Loads the pre-trained LL97 model and its encoders without retraining."""
    model_path = MODELS_DIR / "ll97_model.joblib"
    encoders_path = MODELS_DIR / "ll97_encoders.joblib"
    try:
        if not model_path.exists() or not encoders_path.exists():
            return None, None
        model = joblib.load(model_path)
        encoders = joblib.load(encoders_path)
        return model, encoders
    except Exception:
        return None, None


def compute_peer_benchmarks(dataset, encoders):
    """
    Returns (type_avg_per_sqft, global_avg_per_sqft) for peer comparison.
    Uses the values saved alongside the model if present; otherwise reconstructs
    per-sqft emissions from the dashboard dataset by back-solving GFA from the
    existing emissions intensity column.
    """
    if isinstance(encoders, dict) and "type_avg" in encoders and "global_avg" in encoders:
        return encoders["type_avg"], encoders["global_avg"]

    if C_GHG not in dataset.columns or C_TYPE not in dataset.columns:
        return {}, 1.0

    working = dataset.dropna(subset=[C_GHG, C_TYPE]).copy()

    if C_INTENSITY in working.columns:
        working["Estimated GFA"] = np.where(
            working[C_INTENSITY] > 0,
            (working[C_GHG] * 1000) / working[C_INTENSITY],
            np.nan
        )
        working = working.dropna(subset=["Estimated GFA"])
        if len(working) > 0:
            type_groups = working.groupby(C_TYPE)
            type_avg = (type_groups[C_GHG].sum() / type_groups["Estimated GFA"].sum()).to_dict()
            global_avg = working[C_GHG].sum() / working["Estimated GFA"].sum()
            return type_avg, global_avg

    type_avg = working.groupby(C_TYPE)[C_GHG].mean().to_dict()
    global_avg = working[C_GHG].mean() if len(working) > 0 else 1.0
    return type_avg, global_avg


def validate_ml_inputs(year_built, gfa, score):
    """Validates ML prediction inputs and returns a list of error messages."""
    errors = []
    current_year = 2026

    if year_built is None or year_built < 1800 or year_built > current_year:
        errors.append(f"⚠️ Year Built must be between 1800 and {current_year}.")
    if gfa is None or gfa <= 0:
        errors.append("⚠️ Gross Floor Area must be a positive number.")
    if score is None or not (0 <= score <= 100):
        errors.append("⚠️ ENERGY STAR Score must be between 0 and 100.")

    return errors


# ==========================================
# MAIN DASHBOARD LAYOUT
# ==========================================
st.title("🌍 ESG & Carbon Mitigation Dashboard")

tab1, tab2, tab3, tab4 = st.tabs([
    "Section 1: Problem Analysis",
    "Section 2: Mitigation Scenarios",
    "Section 3: ML Prediction Engine",
    "Section 4: Financial Sensitivity & CAPEX Scenarios"
])

# ---------------------------------------------------------
# TAB 1: PROBLEM ANALYSIS
# ---------------------------------------------------------
with tab1:
    #st.markdown('<img src="https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?q=80&w=1200&auto=format&fit=crop" class="header-image">', unsafe_allow_html=True)
    
    kpi_ghg = df[C_GHG].sum() if C_GHG in df.columns else 0
    kpi_net = df[C_NET].sum() if C_NET in df.columns else 0
    kpi_penalty = df[C_PENALTY].sum() if C_PENALTY in df.columns else 0
    kpi_score = df[C_SCORE].mean() if C_SCORE in df.columns else 0
    kpi_intensity = df[C_INTENSITY].mean() if C_INTENSITY in df.columns else 0
    kpi_avoided = df[C_AVOIDED].sum() if C_AVOIDED in df.columns else 0
    high_risk_count = len(df[df[C_PENALTY] > df[C_PENALTY].quantile(0.75)]) if C_PENALTY in df.columns else 0
    bldg_count = len(df)
    
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card"><div class="kpi-title">Total Properties</div><div class="kpi-value">🏢 {bldg_count:,}</div></div>
            <div class="kpi-card risk"><div class="kpi-title">Total GHG (tCO₂e)</div><div class="kpi-value">🏭 {kpi_ghg:,.0f}</div></div>
            <div class="kpi-card risk"><div class="kpi-title">Total LL97 Penalty</div><div class="kpi-value">💵 ${kpi_penalty:,.0f}</div></div>
            <div class="kpi-card good"><div class="kpi-title">Avg ENERGY STAR</div><div class="kpi-value">⭐ {kpi_score:.1f}/100</div></div>
        </div>
        <div class="kpi-container">
            <div class="kpi-card good"><div class="kpi-title">Avoided Emissions</div><div class="kpi-value">🌿 {kpi_avoided:,.0f} <span class="kpi-badge badge-green">tCO₂e</span></div></div>
            <div class="kpi-card risk"><div class="kpi-title">Avg Intensity</div><div class="kpi-value">📊 {kpi_intensity:.2f} <span class="kpi-badge badge-red">kgCO₂/ft²</span></div></div>
            <div class="kpi-card"><div class="kpi-title">Net Emissions</div><div class="kpi-value">📉 {kpi_net:,.0f}</div></div>
            <div class="kpi-card risk"><div class="kpi-title">High-Risk Assets</div><div class="kpi-value">⚠️ {high_risk_count}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Executive Summary Panel
    highest_emitter = df.loc[df[C_GHG].idxmax()][C_NAME] if C_GHG in df.columns and not df[C_GHG].isna().all() else "N/A"
    highest_penalty_bldg = df.loc[df[C_PENALTY].idxmax()][C_NAME] if C_PENALTY in df.columns and not df[C_PENALTY].isna().all() else "N/A"
    best_performer = df.loc[df[C_SCORE].idxmax()][C_NAME] if C_SCORE in df.columns and not df[C_SCORE].isna().all() else "N/A"
    
    st.markdown(f"""
        <div class="exec-panel">
            <h3>📑 Chief Sustainability Officer Summary</h3>
            <p>The current portfolio configuration carries an aggregate LL97 exposure of <b>${kpi_penalty:,.0f}</b> driven by <b>{kpi_ghg:,.0f} metric tons</b> of CO₂e. 
            The most severe environmental bottleneck is <b>{highest_emitter}</b>, while <b>{highest_penalty_bldg}</b> poses the most immediate financial threat. 
            Conversely, <b>{best_performer}</b> serves as the portfolio benchmark. Priority capital allocation should target the highest-risk assets to rapidly mitigate statutory fines.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🚨 High-Risk Identification")
    c1, c2 = st.columns(2)
    with c1:
        if all(c in df.columns for c in [C_NAME, C_GHG]):
            top_ghg = df.nlargest(10, C_GHG).sort_values(C_GHG, ascending=True)
            st.plotly_chart(plot_horizontal_bar(top_ghg, C_GHG, C_NAME, "Top 10 Polluting Buildings", COLOR_RED, hover_cols=[C_TYPE, C_BORO]), use_container_width=True)
            st.caption("Buildings contributing the highest gross metric tons of CO₂ equivalent.")
            
            with st.expander("🔍 Show Insights: Top Polluters"):
                if len(top_ghg) > 0:
                    highest_bldg = top_ghg.iloc[-1]
                    pct_total = (highest_bldg[C_GHG] / kpi_ghg * 100) if kpi_ghg > 0 else 0
                    diff = highest_bldg[C_GHG] - (top_ghg.iloc[-2][C_GHG] if len(top_ghg)>1 else 0)
                    st.info(f"""
                    * ✅ **Highest Emitter:** {highest_bldg[C_NAME]} with {highest_bldg[C_GHG]:,.0f} tCO₂e.
                    * ⚠️ **Concentration Risk:** This single building accounts for **{pct_total:.1f}%** of the currently filtered emissions.
                    * 📈 **Outlier Check:** It emits **{diff:,.0f} tCO₂e** more than the second-highest emitter.
                    """)
            
    with c2:
        if all(c in df.columns for c in [C_NAME, C_PENALTY]):
            top_pen = df.nlargest(10, C_PENALTY).sort_values(C_PENALTY, ascending=True)
            st.plotly_chart(plot_horizontal_bar(top_pen, C_PENALTY, C_NAME, "Highest Financial Risk (LL97 Penalties)", COLOR_RED, hover_cols=[C_GHG]), use_container_width=True)
            st.caption("Buildings facing the largest estimated statutory fines under Local Law 97.")
            
            with st.expander("💡 AI Insights: Financial Risk"):
                if len(top_pen) > 0:
                    highest_risk = top_pen.iloc[-1]
                    top10_pen_total = top_pen[C_PENALTY].sum()
                    pct_risk = (top10_pen_total / kpi_penalty * 100) if kpi_penalty > 0 else 0
                    st.warning(f"""
                    * 💰 **Maximum Liability:** {highest_risk[C_NAME]} is facing the highest potential penalty of **${highest_risk[C_PENALTY]:,.0f}**.
                    * ⚠️ **Risk Concentration:** The top 10 buildings shown represent **{pct_risk:.1f}%** (${top10_pen_total:,.0f}) of total portfolio penalties.
                    * 🌱 **Action Required:** Prioritizing retrofits on these specific properties will yield the highest ROI in penalty avoidance.
                    """)

    st.markdown("### 🏢 Structural & Regional Distribution")
    c3, c4 = st.columns(2)
    with c3:
        if C_TYPE in df.columns and C_GHG in df.columns:
            type_df = df.groupby(C_TYPE)[C_GHG].sum().reset_index().nlargest(10, C_GHG).sort_values(C_GHG, ascending=True)
            st.plotly_chart(plot_horizontal_bar(type_df, C_GHG, C_TYPE, "Emissions by Building Type", COLOR_BLUE), use_container_width=True)
            st.caption("Aggregated emissions footprint categorized by primary property use-case.")
            
            with st.expander("📊 Key Findings: Building Types"):
                if len(type_df) > 0:
                    top_type = type_df.iloc[-1]
                    avg_by_type = df.groupby(C_TYPE)[C_GHG].mean().loc[top_type[C_TYPE]]
                    st.info(f"""
                    * ✅ **Primary Contributor:** **{top_type[C_TYPE]}** properties generate the most aggregate emissions ({top_type[C_GHG]:,.0f} tCO₂e).
                    * 📈 **Averages:** On average, a {top_type[C_TYPE]} building emits **{avg_by_type:,.0f} tCO₂e**.
                    * 🌱 **Strategy Focus:** Targeted guidelines specific to {top_type[C_TYPE]} operations will have the largest systemic impact.
                    """)
            
    with c4:
        if C_BORO in df.columns and C_PENALTY in df.columns:
            boro_df = df.groupby(C_BORO)[[C_GHG, C_PENALTY]].sum().reset_index()
            fig_boro = px.bar(boro_df, x=C_BORO, y=[C_GHG, C_PENALTY], barmode='group', 
                              color_discrete_sequence=[COLOR_BLUE, COLOR_RED])
            fig_boro.update_layout(get_layout("Borough Analysis: Emissions & Penalties"))
            fig_boro.update_layout(legend_title_text='')
            st.plotly_chart(fig_boro, use_container_width=True)
            st.caption("Comparison of physical emissions vs. financial risk distributed geographically.")
            
            with st.expander("🔍 Show Insights: Geography"):
                if len(boro_df) > 0:
                    worst_boro = boro_df.loc[boro_df[C_GHG].idxmax()]
                    best_boro = boro_df.loc[boro_df[C_GHG].idxmin()]
                    st.info(f"""
                    * ✅ **Highest Emissions:** **{worst_boro[C_BORO]}** accounts for the most emissions ({worst_boro[C_GHG]:,.0f} tCO₂e).
                    * 💰 **Highest Penalties:** {boro_df.loc[boro_df[C_PENALTY].idxmax()][C_BORO]} faces the highest cumulative LL97 fines.
                    * 🌱 **Best Performer:** **{best_boro[C_BORO]}** shows the lowest aggregate footprint in the selected filters.
                    """)

    st.markdown("### ⚡ Operational Insights")
    c5, c6 = st.columns(2)
    with c5:
        if all(c in df.columns for c in [C_AGE, C_INTENSITY, C_NAME]):
            try:
                fig_age = px.scatter(df, x=C_AGE, y=C_INTENSITY, opacity=0.6, hover_name=C_NAME, hover_data=[C_TYPE, C_GHG],
                                     trendline="ols", trendline_color_override=COLOR_ORANGE)
            except Exception:
                fig_age = px.scatter(df, x=C_AGE, y=C_INTENSITY, opacity=0.6, hover_name=C_NAME, hover_data=[C_TYPE, C_GHG])
            fig_age.update_traces(marker_color=COLOR_BLUE)
            fig_age.update_layout(get_layout("Building Age vs. Emission Intensity"))
            st.plotly_chart(fig_age, use_container_width=True)
            st.caption("Visualizing the relationship between infrastructure age and carbon efficiency.")
            
            with st.expander("💡 AI Insights: Infrastructure Age"):
                if len(df.dropna(subset=[C_AGE, C_INTENSITY])) > 2:
                    corr = df[C_AGE].corr(df[C_INTENSITY])
                    trend_txt = "tend to be less efficient" if corr > 0 else "show minimal efficiency loss compared to newer builds"
                    st.info(f"""
                    * 📈 **Trend Analysis:** Older buildings in this portfolio {trend_txt} (Correlation: {corr:.2f}).
                    * ✅ **Oldest Asset:** {df.loc[df[C_AGE].idxmax()][C_NAME]} ({df[C_AGE].max():.0f} years old).
                    * ⚠️ **Highest Intensity:** {df.loc[df[C_INTENSITY].idxmax()][C_NAME]} is the least carbon-efficient property per square foot.
                    """)
            
    with c6:
        energy_cols = [c for c in df.columns if "Use (kBtu)" in c]
        if energy_cols:
            energy_sums = df[energy_cols].sum().sort_values(ascending=True)
            energy_df = pd.DataFrame({'Source': energy_sums.index.str.replace(' Use (kBtu)', '', regex=False), 'Total kBtu': energy_sums.values})
            st.plotly_chart(plot_horizontal_bar(energy_df, 'Total kBtu', 'Source', "Portfolio Energy Source Breakdown", COLOR_BLUE), use_container_width=True)
            st.caption("Aggregate energy consumption separated by utility and fuel type.")
            
            with st.expander("📊 Key Findings: Energy Use"):
                if len(energy_sums) > 0:
                    top_energy = energy_sums.index[-1]
                    total_energy = energy_sums.sum()
                    pct_energy = (energy_sums.iloc[-1] / total_energy * 100) if total_energy > 0 else 0
                    st.info(f"""
                    * ✅ **Dominant Source:** **{top_energy.replace(' Use (kBtu)', '')}** is the primary driver of consumption.
                    * 📈 **Distribution:** It accounts for **{pct_energy:.1f}%** of the total energy modeled.
                    * 🌱 **Opportunity:** Targeting {top_energy.replace(' Use (kBtu)', '')} efficiency systems (like HVAC electrification or grid PPAs) provides the fastest reduction pathway.
                    """)

    c7, c8 = st.columns(2)
    with c7:
        if all(c in df.columns for c in [C_SCORE, C_INTENSITY, C_NAME]):
            fig_bench = px.scatter(df, x=C_SCORE, y=C_INTENSITY, color=C_SCORE, hover_name=C_NAME,
                                   color_continuous_scale="RdYlGn", opacity=0.7)
            fig_bench.update_layout(get_layout("ENERGY STAR Score vs. Emission Intensity"))
            st.plotly_chart(fig_bench, use_container_width=True)
            st.caption("Benchmarking federal rating (higher is better) against actual carbon intensity.")
            
            with st.expander("🔍 Show Insights: ENERGY STAR Benchmark"):
                if len(df.dropna(subset=[C_SCORE, C_INTENSITY])) > 2:
                    avg_score = df[C_SCORE].mean()
                    low_score_bldgs = len(df[df[C_SCORE] < 50])
                    st.info(f"""
                    * 📈 **Average Benchmark:** The filtered portfolio averages a score of **{avg_score:.1f}/100**.
                    * ⚠️ **Underperformers:** **{low_score_bldgs} properties** score below the national median of 50.
                    * ✅ **Validation:** As expected, higher scores generally correlate tightly with lower emission intensities.
                    """)
            
    with c8:
        if C_ALERTS in df.columns:
            alerts_series = df[C_ALERTS].dropna().astype(str).str.split(',').explode().str.strip()
            alerts_count = alerts_series.value_counts().reset_index().head(10).sort_values('count', ascending=True)
            alerts_count.columns = ['Alert Type', 'Frequency']
            fig_alerts = plot_horizontal_bar(alerts_count, 'Frequency', 'Alert Type', "Data Quality Issues Detected", COLOR_ORANGE)
            st.plotly_chart(fig_alerts, use_container_width=True)
            st.caption("Identified gaps and anomalies in utility data reporting.")
            
            with st.expander("⚠️ Key Findings: Data Integrity"):
                if len(alerts_count) > 0:
                    top_alert = alerts_count.iloc[-1]
                    st.warning(f"""
                    * ⚠️ **Primary Issue:** **{top_alert['Alert Type']}** is the most common data gap, affecting {top_alert['Frequency']} reports.
                    * 📈 **Reporting Risk:** Poor data quality can lead to inaccurate LL97 penalty assessments and misallocated capital.
                    * 💰 **Action:** Immediate utility meter audits required for flagged properties to correct baseline reporting.
                    """)

# ---------------------------------------------------------
# TAB 2: MITIGATION SCENARIOS
# ---------------------------------------------------------
with tab2:
    st.markdown('<img src="https://images.unsplash.com/photo-1466611653911-95081537e5b7?q=80&w=1200&auto=format&fit=crop" class="header-image">', unsafe_allow_html=True)
    st.markdown("### 🛠️ Configure Strategic Interventions")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        eff_pct = st.slider("💡 Energy Efficiency Upgrade (%)", 0, 40, 15, help="Reduces overall baseline emissions portfolio-wide (e.g. LED retrofits, HVAC tuning).") / 100
    with col_s2:
        renew_pct = st.slider("☀️ Renewable Energy Adoption (%)", 0, 100, 30, help="Replaces Grid Electricity with clean, off-site power purchase agreements (PPAs).") / 100
    with col_s3:
        retro_age = st.slider("🏗️ Deep Retrofit Target Age (Years)", 20, 100, 50, help="Targets buildings older than this parameter for deep envelope and system upgrades.")
        retro_pct = 0.40 

    base_emissions = df[C_GHG].sum() if C_GHG in df.columns else 1 
    base_penalty = df[C_PENALTY].sum() if C_PENALTY in df.columns else 0
    
    s1_red_emissions = base_emissions * eff_pct
    s1_bldgs = len(df)
    
    grid_col = "Electricity Use - Grid Purchase (kBtu)"
    grid_ratio = df[grid_col].sum() / df[[c for c in df.columns if "Use (kBtu)" in c]].sum().sum() if grid_col in df.columns else 0.4
    s2_red_emissions = (base_emissions * grid_ratio) * renew_pct
    s2_bldgs = len(df[df[grid_col] > 0]) if grid_col in df.columns else len(df)
    
    if C_AGE in df.columns:
        target_bldgs = df[df[C_AGE] >= retro_age]
        s3_red_emissions = target_bldgs[C_GHG].sum() * retro_pct
        s3_bldgs = len(target_bldgs)
    else:
        s3_red_emissions, s3_bldgs = 0, 0

    comb_remain = base_emissions * (1 - eff_pct)
    comb_remain = comb_remain - (s2_red_emissions * (1 - eff_pct)) 
    comb_remain = comb_remain - (s3_red_emissions * (1 - eff_pct)) 
    comb_red_emissions = base_emissions - comb_remain

    def calc_savings(reduction): return base_penalty * (reduction / base_emissions)

    scenarios = pd.DataFrame({
        "Scenario": ["Baseline", "S1: Efficiency", "S2: Renewables", "S3: Retrofit", "Combined Strategy"],
        "Emissions (tCO₂e)": [base_emissions, base_emissions-s1_red_emissions, base_emissions-s2_red_emissions, base_emissions-s3_red_emissions, comb_remain],
        "Reduction (tCO₂e)": [0, s1_red_emissions, s2_red_emissions, s3_red_emissions, comb_red_emissions],
        "Reduction %": [0, (s1_red_emissions/base_emissions)*100, (s2_red_emissions/base_emissions)*100, (s3_red_emissions/base_emissions)*100, (comb_red_emissions/base_emissions)*100],
        "$ Saved (LL97)": [0, calc_savings(s1_red_emissions), calc_savings(s2_red_emissions), calc_savings(s3_red_emissions), calc_savings(comb_red_emissions)],
        "Bldgs Impacted": [0, s1_bldgs, s2_bldgs, s3_bldgs, bldg_count]
    })

    st.markdown("---")
    
    st.subheader("🎯 Combined Strategy Outcomes", help="Shows the compounded result of applying all three scenarios sequentially to avoid double-counting emissions.")
    co1, co2, co3, co4 = st.columns(4)
    co1.metric("Final Emissions (tCO₂e)", f"{comb_remain:,.0f}", f"-{comb_red_emissions:,.0f} (-{(comb_red_emissions/base_emissions)*100:.1f}%)")
    co2.metric("Total LL97 Penalty Saved", f"${calc_savings(comb_red_emissions):,.0f}", "Projected Annual Savings")
    co3.metric("Buildings Impacted", f"{bldg_count}", "Portfolio Wide")
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = (comb_red_emissions/base_emissions)*100,
        title = {'text': "% Portfolio Emissions Reduced", 'font': {'color': '#f8fafc'}},
        number = {'suffix': "%", 'font': {'color': COLOR_GREEN}},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': COLOR_GREEN},
            'bgcolor': COLOR_CARD,
            'steps': [
                {'range': [0, 20], 'color': COLOR_RED},
                {'range': [20, 50], 'color': COLOR_ORANGE},
                {'range': [50, 100], 'color': "#064e3b"}
            ]}
    ))
    fig_gauge.update_layout(get_layout(), height=250, margin=dict(t=40, b=0, l=20, r=20))
    with co4:
        st.plotly_chart(fig_gauge, use_container_width=True)

    with st.expander("💡 AI Insights: Mitigation Performance"):
        best_single = scenarios.iloc[1:4].loc[scenarios.iloc[1:4]["Reduction (tCO₂e)"].idxmax()]
        st.success(f"""
        * 🌱 **Cumulative Impact:** Executing the combined strategy removes **{comb_red_emissions:,.0f} tCO₂e** from your annual footprint.
        * 💰 **Capital Preservation:** This approach prevents an estimated **${calc_savings(comb_red_emissions):,.0f}** in regulatory fines.
        * ✅ **Most Effective Single Measure:** On its own, **{best_single['Scenario'].replace('S1: ', '').replace('S2: ', '').replace('S3: ', '')}** provides the highest independent return, reducing baseline emissions by {best_single['Reduction %']:.1f}%.
        * 📉 **Residual Liability:** Your portfolio will still generate **{comb_remain:,.0f} tCO₂e**. Further decarbonization or carbon offsets will be required to reach Net Zero.
        """)

    st.markdown("### 📉 Impact Breakdown")
    r2c1, r2c2 = st.columns(2)
    
    with r2c1:
        fig_waterfall = go.Figure(go.Waterfall(
            name="2026 Path", orientation="v",
            measure=["absolute", "relative", "relative", "relative", "total"],
            x=["Baseline", "Efficiency", "Renewables", "Retrofits", "Final Residual"],
            textposition="outside",
            text=[f"{v/1000:.1f}k" for v in [base_emissions, -s1_red_emissions, -s2_red_emissions, -s3_red_emissions, comb_remain]],
            y=[base_emissions, -s1_red_emissions, -s2_red_emissions, -s3_red_emissions, comb_remain],
            decreasing={"marker": {"color": COLOR_GREEN}},
            increasing={"marker": {"color": COLOR_RED}},
            totals={"marker": {"color": COLOR_BLUE}}
        ))
        fig_waterfall.update_layout(get_layout("Emissions Reduction Waterfall (tCO₂e)"))
        st.plotly_chart(fig_waterfall, use_container_width=True)
        st.caption("Visualizing the step-by-step reduction from current baseline to the final projected residual footprint.")

    with r2c2:
        categories = ['CO₂ Reduction %', 'Penalty Savings %', 'Bldgs Impacted %']
        fig_radar = go.Figure()
        
        def add_radar_trace(name, red_pct, bldg_count, color):
            fig_radar.add_trace(go.Scatterpolar(
                r=[red_pct, red_pct, (bldg_count/len(df))*100 if len(df)>0 else 0], 
                theta=categories, fill='toself', name=name, marker=dict(color=color)
            ))
            
        add_radar_trace("S1: Efficiency", (s1_red_emissions/base_emissions)*100, s1_bldgs, COLOR_BLUE)
        add_radar_trace("S2: Renewables", (s2_red_emissions/base_emissions)*100, s2_bldgs, COLOR_ORANGE)
        add_radar_trace("S3: Retrofit", (s3_red_emissions/base_emissions)*100, s3_bldgs, COLOR_RED)
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#334155")),
            showlegend=True,
            **get_layout("Scenario Effectiveness Radar")
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("Comparing the holistic impact footprint of each independent strategy.")

    r3c1, r3c2 = st.columns(2)
    
    with r3c1:
        plot_df = scenarios.iloc[1:4].melt(id_vars="Scenario", value_vars=["Reduction (tCO₂e)", "$ Saved (LL97)"])
        fig_comp = px.bar(plot_df, x="Scenario", y="value", color="variable", barmode="group",
                          color_discrete_sequence=[COLOR_GREEN, COLOR_BLUE])
        fig_comp.update_layout(get_layout("Individual Scenario Return vs Impact"))
        fig_comp.update_yaxes(showticklabels=False, title="")
        st.plotly_chart(fig_comp, use_container_width=True)
        st.caption("Hover over bars to view exact physical vs financial yield for each scenario.")

    with r3c2:
        df_roadmap = pd.DataFrame([
            dict(Task="Phase 1: Energy Audits & Upgrades", Start='2024-01-01', Finish='2024-12-31', Phase="Short-term"),
            dict(Task="Phase 2: Power Purchase Agreements", Start='2024-06-01', Finish='2025-06-30', Phase="Mid-term"),
            dict(Task="Phase 3: Deep Envelope Retrofits", Start='2025-01-01', Finish='2026-12-31', Phase="Long-term")
        ])
        fig_timeline = px.timeline(df_roadmap, x_start="Start", x_end="Finish", y="Task", color="Phase", 
                                   color_discrete_sequence=[COLOR_BLUE, COLOR_ORANGE, COLOR_GREEN])
        fig_timeline.update_layout(get_layout("Strategic Implementation Roadmap"))
        st.plotly_chart(fig_timeline, use_container_width=True)
        st.caption("A proposed multi-year project timeline to execute the combined strategy.")

    st.markdown("---")
    st.info("💡 **C-Suite Financial Integration:** Looking for detailed **Regulatory & Grid Shock Sensitivity Analysis (`$/ft²`)** or **Decade-Built WET Decarbonization Payback Modeling**? Navigate directly to **Section 4: Financial Sensitivity & CAPEX Scenarios** above to explore Hagar Hussein's financial engineering suites.")

# ---------------------------------------------------------
# TAB 3: ML PREDICTION ENGINE
# ---------------------------------------------------------
with tab3:
    st.markdown("### 🤖 AI-Powered Emissions & LL97 Liability Predictor")
    st.caption("Enter a building's characteristics to forecast GHG emissions and estimate Local Law 97 penalty exposure using the trained Random Forest model.")

    ml_model, ml_encoders = load_ml_assets()

    if ml_model is None or ml_encoders is None:
        st.error(
            "⚠️ ML model assets not found. Please ensure 'll97_model.joblib' and "
            "'ll97_encoders.joblib' exist in the 'models' directory and were generated "
            "by one of the training scripts."
        )
    elif not isinstance(ml_encoders, dict) or "bor" not in ml_encoders or "typ" not in ml_encoders:
        st.error("⚠️ The loaded encoders file is malformed. Expected keys 'bor' and 'typ' were not found.")
    else:
        borough_classes = list(ml_encoders["bor"].classes_)
        type_classes = list(ml_encoders["typ"].classes_)
        type_avg, global_avg = compute_peer_benchmarks(raw_df, ml_encoders)

        st.markdown("---")
        st.markdown("#### 🔮 Building Profile")

        with st.form("ml_prediction_form"):
            f1, f2, f3 = st.columns(3)
            with f1:
                input_year_built = st.number_input("Year Built", min_value=1800, max_value=2026, value=1990, step=1)
                input_gfa = st.number_input("Gross Floor Area (sq ft)", min_value=1.0, value=100000.0, step=1000.0)
            with f2:
                input_score = st.number_input("ENERGY STAR Score", min_value=0, max_value=100, value=50, step=1)
                input_borough = st.selectbox("Borough", borough_classes)
            with f3:
                input_type = st.selectbox("Primary Property Type", type_classes)
                st.markdown("&nbsp;")

            submitted = st.form_submit_button("⚡ Generate Prediction", use_container_width=True)

        if submitted:
            validation_errors = validate_ml_inputs(input_year_built, input_gfa, input_score)

            if validation_errors:
                for error in validation_errors:
                    st.error(error)
            else:
                try:
                    borough_code = ml_encoders["bor"].transform([input_borough])[0]
                    type_code = ml_encoders["typ"].transform([input_type])[0]

                    feature_columns = [
                        "Year Built",
                        "Property GFA - Calculated (Buildings and Parking) (ft²)",
                        "ENERGY STAR Score",
                        "Borough_Enc",
                        "Type_Enc"
                    ]
                    input_frame = pd.DataFrame(
                        [[input_year_built, input_gfa, input_score, borough_code, type_code]],
                        columns=feature_columns
                    )

                    predicted_emissions = float(ml_model.predict(input_frame)[0])
                    predicted_penalty = predicted_emissions * 268
                    liability_psf = predicted_penalty / input_gfa
                    predicted_intensity = predicted_emissions / input_gfa
                    ll97_limit = CURRENT_LIMITS.get(input_type, CURRENT_LIMITS.get("Default", 0.00750))
                    is_compliant = predicted_intensity <= ll97_limit

                    diagnosis, recommendations, efficiency_gap = get_data_driven_insights(
                        input_year_built, input_score, predicted_emissions, input_gfa,
                        input_type, type_avg, global_avg
                    )

                    st.markdown("---")
                    st.markdown("#### 📋 Prediction Results")

                    gap_card_class = "risk" if efficiency_gap > 0 else "good"
                    gap_icon = "📈" if efficiency_gap > 0 else "📉"
                    compliance_card_class = "good" if is_compliant else "risk"
                    compliance_label = "Compliant" if is_compliant else "Non-Compliant"
                    compliance_icon = "✅" if is_compliant else "🚫"

                    st.markdown(f"""
                        <div class="kpi-container">
                            <div class="kpi-card risk"><div class="kpi-title">Predicted GHG Emissions</div><div class="kpi-value">🏭 {predicted_emissions:,.1f} tCO₂e/yr</div></div>
                            <div class="kpi-card risk"><div class="kpi-title">Est. LL97 Penalty</div><div class="kpi-value">💵 ${predicted_penalty:,.0f}/yr</div></div>
                            <div class="kpi-card"><div class="kpi-title">Liability per Sq Ft</div><div class="kpi-value">📐 ${liability_psf:.2f}/ft²</div></div>
                            <div class="kpi-card {gap_card_class}"><div class="kpi-title">Peer Comparison</div><div class="kpi-value">{gap_icon} {efficiency_gap:+.1f}%</div></div>
                        </div>
                        <div class="kpi-container">
                            <div class="kpi-card {compliance_card_class}"><div class="kpi-title">LL97 Compliance Status</div><div class="kpi-value">{compliance_icon} {compliance_label}</div></div>
                            <div class="kpi-card"><div class="kpi-title">Emission Intensity</div><div class="kpi-value">📊 {predicted_intensity:.5f} tCO₂e/ft²</div></div>
                            <div class="kpi-card"><div class="kpi-title">Current LL97 Limit</div><div class="kpi-value">🎯 {ll97_limit:.5f} tCO₂e/ft²</div></div>
                        </div>
                    """, unsafe_allow_html=True)

                    insight_col1, insight_col2 = st.columns(2)
                    with insight_col1:
                        with st.expander("🔍 Data-Driven Diagnosis", expanded=True):
                            for item in diagnosis:
                                st.info(item)
                    with insight_col2:
                        with st.expander("🛠️ Recommended Actions", expanded=True):
                            for item in recommendations:
                                st.success(item)

                    if not ML_INSIGHTS_AVAILABLE:
                        st.warning(
                            "Diagnostic insights are running in fallback mode because "
                            "'models/ll97_playground.py' could not be imported."
                        )

                except Exception as exc:
                    st.error(f"⚠️ Prediction failed due to an unexpected error: {exc}")

        st.markdown("---")
        st.markdown("#### 📈 Model Insights")

        if hasattr(ml_model, "feature_importances_"):
            importance_df = pd.DataFrame({
                "Feature": ["Year Built", "GFA (Area)", "ENERGY STAR Score", "Borough", "Property Type"],
                "Importance": ml_model.feature_importances_
            }).sort_values("Importance", ascending=True)

            st.plotly_chart(
                plot_horizontal_bar(importance_df, "Importance", "Feature", "Model Feature Importance", COLOR_BLUE),
                use_container_width=True
            )
            st.caption("Relative contribution of each input feature to the Random Forest's emissions predictions.")
        else:
            st.info("Feature importance is unavailable for this model type.")

# ---------------------------------------------------------
# TAB 4: FINANCIAL SENSITIVITY & CAPEX SCENARIOS
# ---------------------------------------------------------
with tab4:
    st.markdown("### 💼 C-Suite Financial Modeling: Sensitivity & Decarbonization Payback Scenarios")
    st.caption("Integrates Hagar Hussein's financial engineering models directly from the Excel project suite (`Sensitivity` & `Scenario` sheets) to evaluate regulatory shocks, CAPEX co-funding, and Whole-Building Energy Transformation (WET) payback cascades.")

    st.markdown("---")

    # =========================================================
    # SECTION 4.1: SENSITIVITY MATRIX (REGULATORY & GRID SHOCKS)
    # =========================================================
    st.markdown("#### 1️⃣ Regulatory & Grid Shock Sensitivity Simulator")
    st.markdown("Evaluate portfolio-wide financial liability per square foot (`$/ft²`) under varying Local Law 97 penalty rates and grid emission factor escalations.")

    scol1, scol2 = st.columns(2)
    with scol1:
        sim_penalty_rate = st.slider(
            "⚖️ Statutory Fine Rate ($ / Metric Ton CO₂e)",
            min_value=268, max_value=400, value=268, step=16,
            help="Mandatory fine rate under Local Law 97 ($268/MT baseline statutory rate)."
        )
    with scol2:
        sim_shock_pct = st.slider(
            "⚡ Grid / Operational Emissions Shock (%)",
            min_value=0, max_value=25, value=0, step=5,
            help="Simulates sudden increases in grid carbon intensity or extreme weather heating demand."
        )

    base_portfolio_ghg = df[C_GHG].sum() if C_GHG in df.columns else 10560815.4
    total_portfolio_gfa = 2014727607.4  # Exact portfolio GFA from Excel Sensitivity Sheet

    sim_ghg = base_portfolio_ghg * (1 + sim_shock_pct / 100.0)
    sim_total_penalty = sim_ghg * sim_penalty_rate
    sim_penalty_psf = sim_total_penalty / total_portfolio_gfa
    baseline_psf_excel = 1.4048045585936528

    psf_variance = ((sim_penalty_psf - baseline_psf_excel) / baseline_psf_excel) * 100.0
    psf_card_class = "risk" if psf_variance > 0 else "good"

    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card risk"><div class="kpi-title">Simulated Portfolio Fine Exposure</div><div class="kpi-value">💵 ${sim_total_penalty:,.0f} / yr</div></div>
            <div class="kpi-card {psf_card_class}"><div class="kpi-title">True Penalty Per SqFt</div><div class="kpi-value">📐 ${sim_penalty_psf:.3f} / ft²</div></div>
            <div class="kpi-card"><div class="kpi-title">Variance vs Baseline ($1.405/ft²)</div><div class="kpi-value">📊 {psf_variance:+.1f}%</div></div>
            <div class="kpi-card"><div class="kpi-title">Simulated Emissions Volume</div><div class="kpi-value">🏭 {sim_ghg:,.0f} tCO₂e</div></div>
        </div>
    """, unsafe_allow_html=True)

    z_matrix = [
        [1.405, 1.475, 1.545, 1.616],
        [1.573, 1.651, 1.730, 1.808],
        [1.835, 1.926, 2.018, 2.110]
    ]
    fig_sens = go.Figure(data=go.Heatmap(
        z=z_matrix,
        x=["+0% Shock", "+5% Shock", "+10% Shock", "+15% Shock"],
        y=["$268 / MT (Base)", "$300 / MT (Moderate)", "$350 / MT (Severe)"],
        colorscale=[[0, "#0f1729"], [0.25, "#00D2FF"], [0.5, "#A855F7"], [0.75, "#FFB800"], [1, "#FF4B6E"]],
        texttemplate="<b>$%{z:.3f}</b>",
        textfont={"size": 16, "color": "white", "family": "Inter"},
        hovertemplate="Penalty: %{y}<br>Shock: %{x}<br>Liability: <b>$%{z:.3f}/ft²</b><extra></extra>"
    ))
    fig_sens.update_layout(
        title=dict(text="Portfolio Liability Intensity Matrix ($/ft²)", font=dict(size=15, color="#ffffff", family="Inter")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", family="Inter"),
        height=300,
        margin=dict(t=50, b=30, l=160, r=40)
    )
    st.plotly_chart(fig_sens, use_container_width=True)

    st.markdown("---")

    # =========================================================
    # SECTION 4.2: THE 5 STRATEGIC DECARBONIZATION PLAYBOOKS
    # =========================================================
    st.markdown("#### 2️⃣ The 5 Strategic Decarbonization & Engineering Playbooks (`Scenario` Sheet)")
    st.markdown("Explore Hagar Hussein's **5 core engineering playbooks** from the Excel model, spanning quick-win operational repairs, retro-commissioning, targeted package retrofits, historic WET wastewater heat recovery, and full electrification.")

    playbook_scenarios = pd.DataFrame([
        {
            "Scenario": "1. Surgical Strike (Top 10 Worst Offenders Quick Win)",
            "Target": "10 Worst Offenders (0.07% Portfolio Area)",
            "CAPEX": 500000.0,
            "Annual_Savings": 20594117.0,
            "Payback_Years": 0.024,
            "Baseline_Penalty": 51485292.0,
            "Post_Penalty": 30891175.0,
            "Desc": "Dispatch engineering task force for Level 2 Energy Audit strictly on Top 10 worst offenders. Execute rapid low-cost OPEX repairs (fixing leaks, recalibrating sensors, correcting BMS scheduling). Immediately wipes out nearly 2% of portfolio penalty exposure."
        },
        {
            "Scenario": "2. Retro-commissioning & BMS Optimization (RCx Turnaround)",
            "Target": "Buildings with ENERGY STAR Score < 50",
            "CAPEX": 802166574.0,
            "Annual_Savings": 243615631.0,
            "Payback_Years": 3.29,
            "Baseline_Penalty": 974462526.0,
            "Post_Penalty": 730846894.0,
            "Desc": "Implement Retro-commissioning (RCx) and BMS optimization ($1.50/sq.ft) to bring underperforming properties up to a target ENERGY STAR score of 75. Achieves a 25% drop in energy consumption and LL97 penalties."
        },
        {
            "Scenario": "3. 1960s Smart Scale Strategy (Optimization Package)",
            "Target": "1960s Built Properties ($2.50/sq.ft Package)",
            "CAPEX": 785244162.0,
            "Annual_Savings": 88033696.0,
            "Payback_Years": 8.92,
            "Baseline_Penalty": 440168480.0,
            "Post_Penalty": 352134784.0,
            "Desc": "Deploy $2.50/sq.ft optimization package: networked LED lighting with daylight sensors, VFD HVAC motor integration, Demand Control Ventilation (DCV CO2 sensors), and mechanical tuning (steam traps, boiler controls)."
        },
        {
            "Scenario": "4. 1930s Infrastructure Innovation (WET Systems - Wastewater Energy Transfer)",
            "Target": "1930s Historic Pre-War Properties",
            "CAPEX": 1499764152.0,
            "Annual_Savings": 61195324.0,
            "Payback_Years": 12.25,
            "Baseline_Penalty": 305976618.0,
            "Post_Penalty": 183585971.0,
            "Desc": "Public-Private Partnership (PPP) with 50% government grant ($749.88M). Intercept municipal wastewater lines in basement with industrial heat exchangers and amplify thermal energy via High-Efficiency Heat Pumps."
        },
        {
            "Scenario": "5. Electrification Push (Fuel Mix Optimization - Oil #4 to Heat Pumps)",
            "Target": "Properties using high-risk Fuel Oil #4",
            "CAPEX": 1889125740.0,
            "Annual_Savings": 181993196.0,
            "Payback_Years": 10.38,
            "Baseline_Penalty": 134362550.0,
            "Post_Penalty": 94053785.0,
            "Desc": "Replace fossil Fuel Oil #4 boilers with Electric Heat Pumps ($20/sq.ft). Combines 30% penalty reduction with $1.50/sq.ft utility bill savings to achieve a ~10-year payback."
        }
    ])

    sel_scenario_name = st.selectbox(
        "🎯 Select Engineering Playbook Scenario to Analyze",
        playbook_scenarios["Scenario"].tolist(),
        index=0
    )

    selected_playbook = playbook_scenarios[playbook_scenarios["Scenario"] == sel_scenario_name].iloc[0]

    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card"><div class="kpi-title">Required CAPEX Investment</div><div class="kpi-value">💵 ${selected_playbook['CAPEX']:,.0f}</div></div>
            <div class="kpi-card good"><div class="kpi-title">Annual Corporate Savings</div><div class="kpi-value">💰 ${selected_playbook['Annual_Savings']:,.0f}/yr</div></div>
            <div class="kpi-card good"><div class="kpi-title">Payback Period</div><div class="kpi-value">⏱️ {selected_playbook['Payback_Years']:.2f} Years</div></div>
            <div class="kpi-card risk"><div class="kpi-title">Baseline Fine Exposure</div><div class="kpi-value">🚨 ${selected_playbook['Baseline_Penalty']:,.0f}</div></div>
            <div class="kpi-card good"><div class="kpi-title">Post-Playbook Penalty</div><div class="kpi-value">✅ ${selected_playbook['Post_Penalty']:,.0f}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # Short labels for clean chart display
    short_labels = [
        "Surgical Strike",
        "Retro-commissioning",
        "1960s Smart Scale",
        "1930s WET Systems",
        "Electrification Push"
    ]
    playbook_scenarios["Short"] = short_labels

    pb_chart_col, pb_info_col = st.columns([1.2, 1.2])

    with pb_chart_col:
        fig_pb = px.bar(
            playbook_scenarios.sort_values("Payback_Years", ascending=True),
            y="Short",
            x="Payback_Years",
            orientation="h",
            color="Annual_Savings",
            color_continuous_scale=[[0, "#00D2FF"], [0.5, "#A855F7"], [1, "#00F59B"]],
            labels={"Payback_Years": "Payback Period (Years)", "Short": ""},
            text=playbook_scenarios.sort_values("Payback_Years", ascending=True)["Payback_Years"].apply(lambda v: f"{v:.2f} yrs")
        )
        fig_pb.update_traces(marker_line_width=0, opacity=0.9, textposition="outside", textfont=dict(color="#ffffff", size=13))
        fig_pb.update_layout(
            title=dict(text="Payback Period across the 5 Strategic Playbooks", font=dict(size=15, color="#ffffff", family="Inter")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1", family="Inter", size=13),
            margin=dict(t=50, b=30, l=10, r=60),
            height=380,
            xaxis=dict(gridcolor="rgba(100,116,139,0.1)", title=""),
            yaxis=dict(gridcolor="rgba(100,116,139,0.1)", automargin=True)
        )
        st.plotly_chart(fig_pb, use_container_width=True)

    with pb_info_col:
        st.markdown(f"""
            <div class="exec-panel" style="height: 380px; overflow-y: auto;">
                <h4 style="color: {COLOR_GREEN} !important; -webkit-text-fill-color: {COLOR_GREEN} !important; background: none !important;">⚙️ Playbook Engineering Blueprint</h4>
                <p style="color: #e2e8f0; margin-bottom: 12px;"><span style="color: {COLOR_BLUE}; font-weight: 700;">Target Scope:</span> {selected_playbook['Target']}</p>
                <p style="color: #e2e8f0; margin-bottom: 12px;"><span style="color: {COLOR_BLUE}; font-weight: 700;">Execution Strategy:</span> {selected_playbook['Desc']}</p>
                <hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(0, 210, 255, 0.3), transparent); margin: 14px 0;">
                <p style="margin-bottom: 0; font-size: 0.9rem; color: #94a3b8;">
                    💡 <span style="color: {COLOR_GREEN}; font-weight: 700;">Self-Funding Model:</span> Phase 1 quick wins (Surgical Strike at <span style="color: #ffffff; font-weight: 700;">0.02 yrs payback</span>) generate immediate cash flow to subsidize Phases 2 & 3.
                </p>
            </div>
        """, unsafe_allow_html=True)