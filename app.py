import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Pakistan Air Quality Dashboard",
    layout="wide"
)

# -----------------------------
# Custom Background Color
# -----------------------------

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Pakistan Air Quality Dashboard",
    layout="wide"
)
 
# -----------------------------
# Sky Blue Theme (CSS)
# -----------------------------
st.markdown(
    """
    <style>
    /* Main app background */
    .stApp {
        background-color: #E6F7FF;
    }
 
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #87CEEB;
    }
    section[data-testid="stSidebar"] * {
        color: #01579B !important;
    }
 
    /* All text color */
    html, body, [class*="css"] {
        color: #01579B;
    }
 
    /* Titles / headers */
    h1, h2, h3, h4, h5, h6 {
        color: #0277BD !important;
    }
 
    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #B3E5FC;
        border: 1px solid #4FC3F7;
        border-radius: 10px;
        padding: 12px;
    }
    div[data-testid="stMetricLabel"] {
        color: #01579B !important;
    }
    div[data-testid="stMetricValue"] {
        color: #0277BD !important;
    }
 
    /* Tabs */
    button[data-baseweb="tab"] {
        color: #01579B;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0277BD;
        border-bottom-color: #0277BD !important;
    }
 
    /* Buttons */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #4FC3F7;
        color: white;
        border: none;
        border-radius: 8px;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #0288D1;
        color: white;
    }
 
    /* Dataframe / table */
    div[data-testid="stDataFrame"] {
        background-color: #F0F9FF;
    }
 
    /* Divider */
    hr {
        border-color: #4FC3F7 !important;
    }
 
    /* Alerts / warnings / info boxes */
    div[data-testid="stAlert"] {
        background-color: #B3E5FC;
        color: #01579B;
    }
    </style>
    """,
    unsafe_allow_html=True
)
 
# Sky blue color palette reused for Plotly charts
SKY_BLUE_SEQUENCE = ["#3BB8FC", "#779FB1", "#01579B", "#81D4FA", "#0277BD"]
 
# -----------------------------
# Constants
# -----------------------------
# Major Pakistani cities with (lat, lon) — used for the Live Data tab
PK_CITIES = {
    "Lahore": (31.5497, 74.3436),
    "Karachi": (24.8607, 67.0011),
    "Islamabad": (33.6844, 73.0479),
    "Rawalpindi": (33.5651, 73.0169),
    "Faisalabad": (31.4504, 73.1350),
    "Multan": (30.1575, 71.5249),
    "Peshawar": (34.0151, 71.5249),
    "Quetta": (30.1798, 66.9750),
    "Sialkot": (32.4945, 74.5229),
}

# Default OpenWeatherMap API key (used if not set in st.secrets or entered manually).
# NOTE: If you share/publish this code (e.g. on GitHub), remove the key from here
# and use a .streamlit/secrets.toml file instead — hardcoded keys in public code
# can be misused by others and may hit your usage limits.
DEFAULT_OPENWEATHER_API_KEY = 
# OpenWeatherMap AQI index (1-5) -> category label
OWM_AQI_LABELS = {
    1: "Good",
    2: "Fair",
    3: "Moderate",
    4: "Poor",
    5: "Very Poor",
}

# -----------------------------
# Live data helpers (OpenWeatherMap)
# -----------------------------
@st.cache_data(ttl=300, show_spinner=False)
def fetch_live_air_quality(lat: float, lon: float, api_key: str):
    """Fetch current air pollution data from OpenWeatherMap."""
    url = "
    params = {"lat": lat, "lon": lon, "appid": api_key}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


@st.cache_data(ttl=300, show_spinner=False)
def fetch_live_weather(lat: float, lon: float, api_key: str):
    """Fetch current weather (temp, humidity, wind, pressure) from OpenWeatherMap."""
    url = ""
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def render_live_tab():
    st.subheader("🔴 Live Air Quality (OpenWeatherMap)")

    # API key priority: st.secrets (if a secrets.toml exists) -> hardcoded default -> manual input
    api_key = ""
    try:
        api_key = st.secrets.get("OPENWEATHER_API_KEY", "")
    except Exception:
        # No secrets.toml file found — that's fine, just fall through
        api_key = ""
    if not api_key:
        api_key = DEFAULT_OPENWEATHER_API_KEY
    if not api_key:
        api_key = st.text_input(
            "🔑 Enter your OpenWeatherMap API key",
            type="password",
            help="Get a free key at https:"
        )

    col_a, col_b = st.columns([2, 1])
    with col_a:
        live_city = st.selectbox("Select City", sorted(PK_CITIES.keys()), key="live_city")
    with col_b:
        st.write("")
        st.write("")
        refresh = st.button("🔄 Refresh Now")

    if refresh:
        fetch_live_air_quality.clear()
        fetch_live_weather.clear()

    if not api_key:
        st.info("Enter an OpenWeatherMap API key above to load live data.")
        return

    lat, lon = PK_CITIES[live_city]

    try:
        with st.spinner("Fetching live data..."):
            aq_data = fetch_live_air_quality(lat, lon, api_key)
            weather_data = fetch_live_weather(lat, lon, api_key)
    except requests.exceptions.HTTPError as e:
        st.error(f"API error: {e}. Please check that your API key is valid and active.")
        return
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach OpenWeatherMap: {e}")
        return

    components = aq_data["list"][0]["components"]
    owm_aqi = aq_data["list"][0]["main"]["aqi"]
    aqi_label = OWM_AQI_LABELS.get(owm_aqi, "Unknown")

    st.caption(f"📍 {live_city} • Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # KPI cards - weather
    st.markdown("#### 📊 Current Weather")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡 Temperature", f"{weather_data['main']['temp']} °C")
    c2.metric("💧 Humidity", f"{weather_data['main']['humidity']} %")
    c3.metric("🌬 Wind Speed", f"{weather_data['wind']['speed']} m/s")
    c4.metric("📊 Pressure", f"{weather_data['main']['pressure']} hPa")

    st.divider()

    # KPI cards - pollutants
    st.markdown("#### 🌫 Current Air Pollutants")
    d1, d2, d3, d4, d5 = st.columns(5)
    d1.metric("🌫 PM2.5", f"{components['pm2_5']} ")
    d2.metric("🌫 PM10", f"{components['pm10']} ")
    d3.metric("☀️ Ozone (O₃)", f"{components['o3']} ")
    d4.metric("🟤 NO₂", f"{components['no2']} ")
    d5.metric("🏷 AQI Category", aqi_label)

    e1, e2, e3 = st.columns(3)
    e1.metric("🟡 SO₂", f"{components['so2']} ")
    e2.metric("⚫ CO", f"{components['co']} ")
    e3.metric("🟢 NH₃", f"{components['nh3']} ")

    st.divider()
    st.caption("Data auto-refreshes every 5 minutes (cached), or click 🔄 Refresh Now for the latest reading.")


# -----------------------------
# Title
# -----------------------------
st.title("🌍 Pakistan Air Quality Dashboard")
st.markdown("Monitor Pakistan Air Quality using historical data or live readings.")

tab_historical, tab_live = st.tabs(["📊 Historical Data", "🔴 Live Data"])

# =====================================================
# TAB 1: Historical Data (original functionality)
# =====================================================
with tab_historical:

    # -----------------------------
    # Load Data
    # -----------------------------
    df = pd.read_csv("database/cleaned_air_quality.csv")

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # -----------------------------
    # Sidebar
    # -----------------------------
    st.sidebar.header("🔎 Historical Filters")

    cities = st.sidebar.selectbox(
        "Select City",
        sorted(df["city"].unique())
    )

    date = st.sidebar.date_input(
        "Select Date",
        value=df["timestamp"].dt.date.min()
    )

    # -----------------------------
    # Filter Data
    # -----------------------------
    city_data = df[df["city"] == cities]

    filtered_data = city_data[
        city_data["timestamp"].dt.date == date
    ]

    st.write(f"### 📍 City: {cities}")
    st.write(f"### 📅 Date: {date}")

    if filtered_data.empty:

        st.warning("No data available for the selected city and date.")

    else:

        latest = filtered_data.iloc[-1]

        # -----------------------------
        # KPI Cards
        # -----------------------------
        st.subheader("📊 Air Quality Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🌡 Temperature", f"{latest['temperature']} °C")
        col2.metric("💧 Humidity", f"{latest['humidity']} %")
        col3.metric("🌬 Wind Speed", f"{latest['wind_speed']} km/h")
        col4.metric("📊 Pressure", f"{latest['pressure']} hPa")

        st.divider()

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
        "🌫 Dust",
        f"{latest['dust']}"
    )

        col2.metric(
        "🌫 PM10",
        f"{latest['pm10']}"
    )

        col3.metric(
        "☀️ Ozone",
        f"{latest['ozone']}"
    )

        col4.metric(
        "🌫 PM2.5",
        f"{latest['pm2_5']}"
    )

        col5.metric(
           "🏷 AQI Category",
           f"{latest['aqi_category']}"
           )

        st.divider()

        # -----------------------------
        # Charts
        # -----------------------------
        st.subheader("📈 Historical Trends")

        c1, c2 = st.columns(2)

        with c1:

            fig1 = px.line(
                city_data,
                x="timestamp",
                y="temperature",
                title="🌡 Temperature Trend"
            )

            fig1.update_layout(height=300)

            st.plotly_chart(fig1, use_container_width=True)

        with c2:

            fig2 = px.line(
                city_data,
                x="timestamp",
                y="humidity",
                title="💧 Humidity Trend"
            )

            fig2.update_layout(height=300)

            st.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns(2)

        with c3:

            fig3 = px.line(
                city_data,
                x="timestamp",
                y="pm2_5",
                title="🌫 PM2.5 Trend"
            )

            fig3.update_layout(height=300)

            st.plotly_chart(fig3, use_container_width=True)

        with c4:

            fig4 = px.line(
                city_data,
                x="timestamp",
                y="pm10",
                title="🌫 PM10 Trend"
            )

            fig4.update_layout(height=300)

            st.plotly_chart(fig4, use_container_width=True)

        st.divider()

        # -----------------------------
        # Filtered Data
        # -----------------------------
        st.subheader("📋 Filtered Data")

        st.dataframe(filtered_data)

        # -----------------------------
        # Download Button
        # -----------------------------
        csv = filtered_data.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="filtered_air_quality.csv",
            mime="text/csv"
        )

# =====================================================
# TAB 2: Live Data (OpenWeatherMap)
# =====================================================
with tab_live:
    render_live_tab()
