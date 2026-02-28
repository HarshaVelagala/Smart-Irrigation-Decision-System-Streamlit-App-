"""
╔══════════════════════════════════════════════════════════════╗
║      Smart Irrigation Decision System  —  Streamlit App      ║
║      Senior Data Engineer · Full-Stack Python                ║
╚══════════════════════════════════════════════════════════════╝

Run:
    pip install streamlit pandas
    streamlit run app.py
"""

import io
import warnings
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Irrigation Decision System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# CUSTOM CSS  —  Clean agricultural-tech aesthetic
# Deep green primary · warm amber accent · data-dense but airy
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@700&display=swap');

/* ── Base ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #f7f9f5;
}

/* ── Hero header ───────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #1a4731 0%, #2d7a4f 50%, #1a4731 100%);
    border-radius: 18px;
    padding: 44px 48px 36px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.hero-banner::after {
    content: "";
    position: absolute;
    bottom: -40px; left: 30%;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.03);
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 6px 0;
    line-height: 1.15;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: rgba(255,255,255,0.72);
    margin: 0;
    font-weight: 300;
    letter-spacing: 0.3px;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.85);
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 14px;
    font-weight: 500;
}

/* ── Upload cards ──────────────────────────────────────── */
.upload-card {
    background: #ffffff;
    border: 1.5px dashed #b8d4c2;
    border-radius: 14px;
    padding: 28px 24px;
    text-align: center;
    transition: border-color 0.2s;
}
.upload-card:hover { border-color: #2d7a4f; }
.upload-icon { font-size: 2.2rem; margin-bottom: 8px; }
.upload-label {
    font-size: 0.95rem;
    font-weight: 600;
    color: #1a4731;
    margin-bottom: 4px;
}
.upload-hint { font-size: 0.8rem; color: #7a9e8a; }

/* ── Section headers ───────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 36px 0 18px 0;
}
.section-pill {
    background: #1a4731;
    color: white;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #1a3325;
    margin: 0;
}

/* ── KPI metric cards ──────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 22px 20px;
    border-left: 4px solid #2d7a4f;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.kpi-card.amber { border-left-color: #d97706; }
.kpi-card.red   { border-left-color: #dc2626; }
.kpi-card.blue  { border-left-color: #2563eb; }
.kpi-value {
    font-family: 'DM Mono', monospace;
    font-size: 2.1rem;
    font-weight: 500;
    color: #1a4731;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-card.amber .kpi-value { color: #d97706; }
.kpi-card.red   .kpi-value { color: #dc2626; }
.kpi-card.blue  .kpi-value { color: #2563eb; }
.kpi-label {
    font-size: 0.8rem;
    color: #6b7280;
    font-weight: 500;
    letter-spacing: 0.3px;
}

/* ── Recommendation badge ──────────────────────────────── */
.badge {
    display: inline-block;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    white-space: nowrap;
}
.badge-now   { background: #fef2f2; color: #b91c1c; border: 1px solid #fca5a5; }
.badge-soon  { background: #fff7ed; color: #c2410c; border: 1px solid #fdba74; }
.badge-light { background: #fefce8; color: #a16207; border: 1px solid #fde047; }
.badge-no    { background: #f0fdf4; color: #15803d; border: 1px solid #86efac; }

/* ── Zone summary cards ────────────────────────────────── */
.zone-card {
    background: white;
    border-radius: 14px;
    padding: 22px 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-top: 3px solid #2d7a4f;
    height: 100%;
}
.zone-name {
    font-size: 1rem;
    font-weight: 700;
    color: #1a4731;
    margin-bottom: 2px;
}
.zone-crop {
    font-size: 0.8rem;
    color: #7a9e8a;
    margin-bottom: 16px;
}
.zone-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid #f3f4f6;
    font-size: 0.82rem;
}
.zone-stat:last-child { border-bottom: none; }
.zone-stat-label { color: #6b7280; }
.zone-stat-value { font-weight: 600; color: #1a3325; font-family: 'DM Mono', monospace; }

/* ── Water bar ──────────────────────────────────────────── */
.water-bar-container {
    background: white;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 8px;
}
.water-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    margin-bottom: 6px;
    font-weight: 500;
}
.water-bar-zone { color: #1a4731; }
.water-bar-val  { color: #2d7a4f; font-family: 'DM Mono', monospace; }
.water-bar-bg {
    background: #f0fdf4;
    border-radius: 8px;
    height: 14px;
    overflow: hidden;
    margin-bottom: 14px;
}
.water-bar-fill {
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, #2d7a4f, #4ade80);
    transition: width 0.6s ease;
}

/* ── Info / warning boxes ──────────────────────────────── */
.info-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.85rem;
    color: #166534;
    margin-bottom: 20px;
}
.warn-box {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.85rem;
    color: #9a3412;
    margin-bottom: 20px;
}
.err-box {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.85rem;
    color: #991b1b;
    margin-bottom: 20px;
}

/* ── Dataframe tweaks ──────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

/* ── Sidebar ───────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #1a4731;
}
[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.88) !important;
}
[data-testid="stSidebar"] .stMarkdown h3 {
    color: white !important;
    font-size: 0.85rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    padding-bottom: 8px;
    margin-bottom: 12px;
}

/* ── Expander ──────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: #1a4731 !important;
}

/* ── Divider ───────────────────────────────────────────── */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, #2d7a4f22, #2d7a4f66, #2d7a4f22);
    margin: 32px 0;
    border: none;
}

/* ── Step indicator ────────────────────────────────────── */
.step-row {
    display: flex;
    gap: 0;
    margin-bottom: 28px;
}
.step-item {
    flex: 1;
    text-align: center;
    position: relative;
}
.step-item::after {
    content: "";
    position: absolute;
    top: 16px; left: 50%;
    width: 100%; height: 2px;
    background: #d1fae5;
    z-index: 0;
}
.step-item:last-child::after { display: none; }
.step-dot {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: #2d7a4f;
    color: white;
    font-size: 0.8rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 6px;
    position: relative;
    z-index: 1;
}
.step-dot.inactive {
    background: #d1fae5;
    color: #6b7280;
}
.step-text { font-size: 0.72rem; color: #6b7280; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────
SOIL_REQUIRED = [
    "date", "field_zone", "soil_moisture_pct", "soil_temp_celsius",
    "crop_type", "soil_ph", "nitrogen_ppm", "phosphorus_ppm", "potassium_ppm",
]
WEATHER_REQUIRED = [
    "date", "field_zone", "temperature_max_c", "temperature_min_c",
    "humidity_pct", "rainfall_mm", "evapotranspiration_mm",
    "wind_speed_kmh", "solar_radiation_mj", "weather_condition",
]

CROP_MOISTURE_OPTIMAL = {
    "Wheat":   (40, 65),
    "Corn":    (50, 75),
    "Soybean": (45, 70),
    "Rice":    (70, 95),
}

IRRIGATION_VOLUMES = {
    "Irrigate Now":    25,
    "Irrigate Soon":   15,
    "Light Irrigation": 8,
    "No Irrigation":    0,
}

ZONE_COLORS = ["#2d7a4f", "#2563eb", "#d97706", "#7c3aed"]


# ──────────────────────────────────────────────────────────────
# PIPELINE FUNCTIONS
# ──────────────────────────────────────────────────────────────

def validate_columns(df: pd.DataFrame, required: list, name: str):
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.markdown(
            f'<div class="err-box">❌ <strong>{name}</strong> is missing columns: '
            f'<code>{", ".join(missing)}</code></div>',
            unsafe_allow_html=True,
        )
        return False
    return True


def compute_moisture_deficit(row) -> float:
    lo, _ = CROP_MOISTURE_OPTIMAL.get(row["crop_type"], (40, 70))
    return round(max(lo - row["soil_moisture_pct"], 0), 2)


def compute_days_since_rain(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["field_zone", "date"]).copy()
    results = []
    for _, group in df.groupby("field_zone"):
        group = group.sort_values("date").copy()
        count, days = 0, []
        for rain in group["rainfall_mm"]:
            count = 0 if rain >= 1.0 else count + 1
            days.append(count)
        group["days_since_rain"] = days
        results.append(group)
    return pd.concat(results).sort_index()


def classify_irrigation(row) -> str:
    deficit = row["moisture_deficit"]
    wb      = row["water_balance_mm"]
    dsr     = row["days_since_rain"]
    stress  = row["temp_stress"]
    hum     = str(row["humidity_category"])

    if deficit > 20 or (wb < -4 and dsr >= 5) or (stress == 1 and deficit > 10):
        return "Irrigate Now"
    if (10 < deficit <= 20) or (wb < -2 and dsr >= 3) or (hum == "Low" and deficit > 5):
        return "Irrigate Soon"
    if (0 < deficit <= 10) or (wb < 0 and dsr >= 1):
        return "Light Irrigation"
    return "No Irrigation"


def build_explanation(row) -> str:
    rec     = row["irrigation_recommendation"]
    deficit = row["moisture_deficit"]
    wb      = row["water_balance_mm"]
    dsr     = int(row["days_since_rain"])
    stress  = int(row["temp_stress"])
    hum     = str(row["humidity_category"])
    crop    = row["crop_type"]
    lo, _   = CROP_MOISTURE_OPTIMAL.get(crop, (40, 70))

    parts = []
    if deficit > 0:
        parts.append(f"Moisture {deficit:.1f}% below optimal for {crop} (needs ≥{lo}%)")
    if wb < 0:
        parts.append(f"Negative water balance ({wb:.1f} mm)")
    if dsr > 0:
        parts.append(f"{dsr} consecutive dry day{'s' if dsr>1 else ''}")
    if stress:
        parts.append("Temperature stress detected")
    if hum == "Low":
        parts.append("Low humidity accelerating evaporation")
    if not parts:
        parts.append("Adequate moisture & positive water balance")
    return "; ".join(parts)


def run_pipeline(soil_df: pd.DataFrame, weather_df: pd.DataFrame) -> pd.DataFrame:
    soil_df["date"]    = pd.to_datetime(soil_df["date"])
    weather_df["date"] = pd.to_datetime(weather_df["date"])

    merged = pd.merge(soil_df, weather_df, on=["date", "field_zone"], how="inner")

    # Feature engineering
    merged["water_balance_mm"]  = (merged["rainfall_mm"] - merged["evapotranspiration_mm"]).round(2)
    merged["moisture_deficit"]  = merged.apply(compute_moisture_deficit, axis=1)
    merged["temp_stress"]       = ((merged["temperature_max_c"] > 35) | (merged["temperature_min_c"] < 10)).astype(int)
    merged["humidity_category"] = pd.cut(
        merged["humidity_pct"], bins=[0, 40, 70, 100],
        labels=["Low", "Moderate", "High"], right=True
    )
    merged = compute_days_since_rain(merged)

    merged["irrigation_recommendation"] = merged.apply(classify_irrigation, axis=1)
    merged["irrigation_volume_mm"]       = merged["irrigation_recommendation"].map(IRRIGATION_VOLUMES)
    merged["explanation"]                = merged.apply(build_explanation, axis=1)

    return merged


def zone_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("field_zone").agg(
        crop_type               = ("crop_type", "first"),
        avg_soil_moisture_pct   = ("soil_moisture_pct", "mean"),
        avg_moisture_deficit    = ("moisture_deficit", "mean"),
        avg_water_balance_mm    = ("water_balance_mm", "mean"),
        total_rainfall_mm       = ("rainfall_mm", "sum"),
        total_et_mm             = ("evapotranspiration_mm", "sum"),
        temp_stress_days        = ("temp_stress", "sum"),
        total_irrigation_mm     = ("irrigation_volume_mm", "sum"),
        irrigation_days         = ("irrigation_volume_mm", lambda x: (x > 0).sum()),
        irrigate_now_days       = ("irrigation_recommendation", lambda x: (x == "Irrigate Now").sum()),
        days_tracked            = ("date", "count"),
    ).round(2).reset_index()


# ──────────────────────────────────────────────────────────────
# RENDER HELPERS
# ──────────────────────────────────────────────────────────────

def rec_badge(rec: str) -> str:
    cls = {
        "Irrigate Now":    "badge-now",
        "Irrigate Soon":   "badge-soon",
        "Light Irrigation":"badge-light",
        "No Irrigation":   "badge-no",
    }.get(rec, "badge-no")
    return f'<span class="badge {cls}">{rec}</span>'


def render_hero():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">🌿 AgriTech · Data Engineering</div>
        <div class="hero-title">Smart Irrigation<br>Decision System</div>
        <div class="hero-sub">Upload sensor &amp; weather data → Join → Engineer features → Get recommendations</div>
    </div>
    """, unsafe_allow_html=True)


def render_step_indicator(step: int):
    steps = ["Upload", "Validate", "Join", "Features", "Recommend"]
    html = '<div class="step-row">'
    for i, s in enumerate(steps, 1):
        active = "step-dot" if i <= step else "step-dot inactive"
        html += f"""
        <div class="step-item">
            <div class="{active}">{i}</div>
            <div class="step-text">{s}</div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_kpi_row(df: pd.DataFrame):
    total_zones   = df["field_zone"].nunique()
    total_records = len(df)
    irrigate_now  = (df["irrigation_recommendation"] == "Irrigate Now").sum()
    total_water   = df["irrigation_volume_mm"].sum()

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-value">{total_zones}</div>
            <div class="kpi-label">Field Zones</div>
        </div>
        <div class="kpi-card blue">
            <div class="kpi-value">{total_records}</div>
            <div class="kpi-label">Zone-Day Records</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-value">{irrigate_now}</div>
            <div class="kpi-label">Irrigate Now Alerts</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-value">{int(total_water)}<span style="font-size:1rem">mm</span></div>
            <div class="kpi-label">Total Water Required</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_recommendation_table(df: pd.DataFrame):
    display_cols = [
        "date", "field_zone", "crop_type",
        "soil_moisture_pct", "moisture_deficit",
        "water_balance_mm", "days_since_rain", "temp_stress",
        "humidity_category", "irrigation_recommendation",
        "irrigation_volume_mm", "explanation",
    ]
    show_df = df[display_cols].copy()
    show_df["date"] = show_df["date"].dt.strftime("%Y-%m-%d")
    show_df.columns = [
        "Date", "Zone", "Crop",
        "Moisture %", "Deficit %",
        "Water Balance mm", "Dry Days", "Temp Stress",
        "Humidity", "Recommendation",
        "Volume mm", "Why",
    ]

    # Colour-coded recommendation column via styler
    def color_rec(val):
        colors = {
            "Irrigate Now":    "background-color:#fef2f2;color:#b91c1c;font-weight:600",
            "Irrigate Soon":   "background-color:#fff7ed;color:#c2410c;font-weight:600",
            "Light Irrigation":"background-color:#fefce8;color:#a16207;font-weight:600",
            "No Irrigation":   "background-color:#f0fdf4;color:#15803d;font-weight:600",
        }
        return colors.get(val, "")

    styled = (
        show_df.style
        .applymap(color_rec, subset=["Recommendation"])
        .format({"Moisture %": "{:.1f}", "Deficit %": "{:.1f}",
                 "Water Balance mm": "{:.2f}", "Volume mm": "{:.0f}"})
        .set_properties(subset=["Why"], **{"min-width": "260px", "font-size": "0.78rem"})
    )
    st.dataframe(styled, use_container_width=True, height=440)


def render_zone_cards(summary: pd.DataFrame):
    colors = ["#2d7a4f", "#2563eb", "#d97706", "#7c3aed"]
    cols = st.columns(min(len(summary), 4))
    for i, (_, row) in enumerate(summary.iterrows()):
        c = colors[i % len(colors)]
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div class="zone-card" style="border-top-color:{c}">
                <div class="zone-name">{row['field_zone']}</div>
                <div class="zone-crop">🌾 {row['crop_type']}</div>
                <div class="zone-stat">
                    <span class="zone-stat-label">Avg Moisture</span>
                    <span class="zone-stat-value">{row['avg_soil_moisture_pct']:.1f}%</span>
                </div>
                <div class="zone-stat">
                    <span class="zone-stat-label">Avg Deficit</span>
                    <span class="zone-stat-value">{row['avg_moisture_deficit']:.1f}%</span>
                </div>
                <div class="zone-stat">
                    <span class="zone-stat-label">Total Rainfall</span>
                    <span class="zone-stat-value">{row['total_rainfall_mm']:.1f} mm</span>
                </div>
                <div class="zone-stat">
                    <span class="zone-stat-label">Total ET₀</span>
                    <span class="zone-stat-value">{row['total_et_mm']:.1f} mm</span>
                </div>
                <div class="zone-stat">
                    <span class="zone-stat-label">Stress Days</span>
                    <span class="zone-stat-value">{int(row['temp_stress_days'])} days</span>
                </div>
                <div class="zone-stat">
                    <span class="zone-stat-label">Irrigate Now Days</span>
                    <span class="zone-stat-value" style="color:#b91c1c">{int(row['irrigate_now_days'])} days</span>
                </div>
                <div class="zone-stat">
                    <span class="zone-stat-label">Irrigation Days</span>
                    <span class="zone-stat-value">{int(row['irrigation_days'])} / {int(row['days_tracked'])}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_water_bars(summary: pd.DataFrame):
    max_vol = summary["total_irrigation_mm"].max()
    colors  = ["#2d7a4f", "#2563eb", "#d97706", "#7c3aed"]
    html = '<div class="water-bar-container">'
    for i, (_, row) in enumerate(summary.iterrows()):
        c   = colors[i % len(colors)]
        pct = (row["total_irrigation_mm"] / max_vol * 100) if max_vol > 0 else 0
        html += f"""
        <div class="water-bar-label">
            <span class="water-bar-zone">{row['field_zone']} — {row['crop_type']}</span>
            <span class="water-bar-val">{int(row['total_irrigation_mm'])} mm</span>
        </div>
        <div class="water-bar-bg">
            <div class="water-bar-fill" style="width:{pct:.1f}%;background:linear-gradient(90deg,{c}aa,{c})"></div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_download(df: pd.DataFrame, summary: pd.DataFrame):
    col1, col2 = st.columns(2)
    with col1:
        csv_full = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download Full Results CSV",
            csv_full, "smart_irrigation_results.csv",
            "text/csv", use_container_width=True,
        )
    with col2:
        csv_sum = summary.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download Zone Summary CSV",
            csv_sum, "zone_summary.csv",
            "text/csv", use_container_width=True,
        )


# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🌿 Pipeline Guide")
        st.markdown("""
**Step 1 — Upload**
Upload both CSV files in the main area.

**Step 2 — Validate**
Checks all required columns exist.

**Step 3 — INNER JOIN**
Merges on `[date, field_zone]`.
Only rows present in **both** files are processed.

**Step 4 — Feature Engineering**
- `water_balance_mm` = rainfall − ET₀
- `moisture_deficit` (crop-specific)
- `temp_stress` (>35°C or <10°C)
- `humidity_category` (Low/Moderate/High)
- `days_since_rain` (per zone streak)

**Step 5 — Recommendation Engine**

| Level | Volume |
|---|---|
| 🔴 Irrigate Now | 25 mm |
| 🟠 Irrigate Soon | 15 mm |
| 🟡 Light Irrigation | 8 mm |
| 🟢 No Irrigation | 0 mm |
        """)

        st.markdown("### 🌾 Crop Moisture Targets")
        for crop, (lo, hi) in CROP_MOISTURE_OPTIMAL.items():
            st.markdown(f"**{crop}**: {lo}–{hi}%")

        st.markdown("### ℹ️ About")
        st.caption(
            "Built with Pandas + Streamlit.\n"
            "INNER JOIN enforces data-quality: "
            "only zone-days with BOTH sensor and weather readings are processed."
        )


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

def main():
    render_hero()
    render_sidebar()

    # ── Step indicator ──────────────────────────────────────
    if "pipeline_done" not in st.session_state:
        st.session_state.pipeline_done = False

    step = 1
    if "soil_df" in st.session_state and "weather_df" in st.session_state:
        step = 2
    if st.session_state.pipeline_done:
        step = 5

    render_step_indicator(step)

    # ── Upload section ──────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <span class="section-pill">01</span>
        <span class="section-title">Upload Your Data Files</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="upload-card">
            <div class="upload-icon">🌱</div>
            <div class="upload-label">Soil Sensor Data</div>
            <div class="upload-hint">soil_sensor_data.csv</div>
        </div>
        """, unsafe_allow_html=True)
        soil_file = st.file_uploader(
            "soil_sensor_data.csv", type=["csv"],
            label_visibility="collapsed", key="soil_upload",
        )

    with col2:
        st.markdown("""
        <div class="upload-card">
            <div class="upload-icon">🌤️</div>
            <div class="upload-label">Weather Station Data</div>
            <div class="upload-hint">weather_data.csv</div>
        </div>
        """, unsafe_allow_html=True)
        weather_file = st.file_uploader(
            "weather_data.csv", type=["csv"],
            label_visibility="collapsed", key="weather_upload",
        )

    # ── Load & validate ─────────────────────────────────────
    if soil_file and weather_file:
        soil_df    = pd.read_csv(soil_file)
        weather_df = pd.read_csv(weather_file)

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
            <span class="section-pill">02</span>
            <span class="section-title">Validation &amp; Schema Check</span>
        </div>
        """, unsafe_allow_html=True)

        soil_ok    = validate_columns(soil_df, SOIL_REQUIRED, "soil_sensor_data.csv")
        weather_ok = validate_columns(weather_df, WEATHER_REQUIRED, "weather_data.csv")

        if soil_ok and weather_ok:
            st.markdown(
                f'<div class="info-box">✅ Both files passed validation. '
                f'Soil: <strong>{len(soil_df)} rows</strong> · '
                f'Weather: <strong>{len(weather_df)} rows</strong></div>',
                unsafe_allow_html=True,
            )

            with st.expander("🔍 Preview Raw Data", expanded=False):
                t1, t2 = st.tabs(["🌱 Soil Sensor", "🌤️ Weather"])
                with t1:
                    st.dataframe(soil_df.head(10), use_container_width=True)
                with t2:
                    st.dataframe(weather_df.head(10), use_container_width=True)

            # ── Run pipeline ────────────────────────────────
            with st.spinner("Running pipeline… joining, engineering features, applying rules…"):
                try:
                    result_df = run_pipeline(soil_df, weather_df)
                    summary   = zone_summary(result_df)
                    st.session_state.pipeline_done = True
                except Exception as e:
                    st.error(f"Pipeline error: {e}")
                    st.stop()

            # ── JOIN info ───────────────────────────────────
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <span class="section-pill">03</span>
                <span class="section-title">INNER JOIN Result</span>
            </div>
            """, unsafe_allow_html=True)

            join_kept = len(result_df)
            join_total = len(soil_df) + len(weather_df)
            st.markdown(
                f'<div class="info-box">🔗 <strong>INNER JOIN on [date, field_zone]</strong> — '
                f'Merged <strong>{join_kept} matched records</strong> from {len(soil_df)} soil + '
                f'{len(weather_df)} weather rows. Only zone-days present in BOTH files are processed — '
                f'this prevents null-poisoned recommendations from offline sensors or stations.</div>',
                unsafe_allow_html=True,
            )

            # ── KPIs ────────────────────────────────────────
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <span class="section-pill">04–05</span>
                <span class="section-title">Features &amp; Recommendations</span>
            </div>
            """, unsafe_allow_html=True)

            render_kpi_row(result_df)

            # ── Recommendation distribution ──────────────────
            dist  = result_df["irrigation_recommendation"].value_counts()
            dcols = st.columns(4)
            icons = {"Irrigate Now": "🔴", "Irrigate Soon": "🟠",
                     "Light Irrigation": "🟡", "No Irrigation": "🟢"}
            for i, (rec, vol) in enumerate(IRRIGATION_VOLUMES.items()):
                cnt = dist.get(rec, 0)
                pct = cnt / len(result_df) * 100
                with dcols[i]:
                    st.metric(
                        f"{icons[rec]} {rec}",
                        f"{cnt} days",
                        f"{pct:.0f}% · {vol} mm/event",
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Recommendation table ─────────────────────────
            with st.expander("📋 Full Recommendation Table", expanded=True):
                render_recommendation_table(result_df)

            # ── Zone summary ────────────────────────────────
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <span class="section-pill">06</span>
                <span class="section-title">Zone-Level Summary</span>
            </div>
            """, unsafe_allow_html=True)

            render_zone_cards(summary)

            # ── Water required ───────────────────────────────
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <span class="section-pill">07</span>
                <span class="section-title">Total Water Required per Zone</span>
            </div>
            """, unsafe_allow_html=True)

            render_water_bars(summary)

            # ── Feature explanation ──────────────────────────
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            with st.expander("📐 Feature Engineering Reference", expanded=False):
                st.markdown("""
| Feature | Formula | Purpose |
|---|---|---|
| `water_balance_mm` | `rainfall_mm − evapotranspiration_mm` | Net daily water gain/loss per zone |
| `moisture_deficit` | `max(crop_optimal_lo − soil_moisture, 0)` | Crop-specific shortfall below target |
| `temp_stress` | `1 if temp_max > 35°C or temp_min < 10°C` | Physiological stress flag |
| `humidity_category` | `Low(<40%) / Moderate(40-70%) / High(>70%)` | Evaporation pressure indicator |
| `days_since_rain` | Consecutive days with rainfall < 1 mm per zone | Cumulative drying streak |

**Decision Rule Hierarchy** *(first match wins)*
1. **Irrigate Now** → deficit > 20% OR (water_balance < −4 AND dry ≥ 5 days) OR (temp_stress AND deficit > 10%)
2. **Irrigate Soon** → deficit 10–20% OR (water_balance < −2 AND dry ≥ 3 days) OR (Low humidity AND deficit > 5%)
3. **Light Irrigation** → deficit 1–10% OR (water_balance < 0 AND dry ≥ 1 day)
4. **No Irrigation** → all other cases
                """)

            # ── Downloads ───────────────────────────────────
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <span class="section-pill">08</span>
                <span class="section-title">Export Results</span>
            </div>
            """, unsafe_allow_html=True)
            render_download(result_df, summary)

    else:
        # Landing state — show expected schema
        st.markdown('<br>', unsafe_allow_html=True)
        with st.expander("📄 Expected CSV Schemas", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**🌱 soil_sensor_data.csv**")
                st.dataframe(
                    pd.DataFrame({
                        "Column": SOIL_REQUIRED,
                        "Example": ["2024-06-01", "Zone_A", "42.5", "22.3",
                                    "Wheat", "6.8", "35.0", "18.0", "120.0"],
                    }),
                    use_container_width=True, hide_index=True,
                )
            with c2:
                st.markdown("**🌤️ weather_data.csv**")
                st.dataframe(
                    pd.DataFrame({
                        "Column": WEATHER_REQUIRED,
                        "Example": ["2024-06-01", "Zone_A", "34.0", "18.0",
                                    "55.0", "2.5", "4.8", "18.0", "19.0", "Sunny"],
                    }),
                    use_container_width=True, hide_index=True,
                )
        st.markdown(
            '<div class="info-box" style="text-align:center">⬆ Upload both CSV files above to run the full pipeline</div>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
