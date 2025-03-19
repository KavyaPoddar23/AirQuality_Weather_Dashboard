import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
AIRVISUAL_API_KEY = os.getenv("AIRVISUAL_API_KEY")

st.set_page_config(page_title="🌤️ Real-Time Air Quality & Weather Dashboard", layout="wide")

st.markdown(
    """
    <style>
        body {
            background-color: #1e1e1e;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .main-title {
            font-size: 28px; /* Reduced size */
            font-weight: bold;
            text-align: center;
            background: -webkit-linear-gradient(45deg, #ff7e5f, #feb47b); /* Changed color */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 16px;
            animation: fadeIn 1.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .highlight-box {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.4);
            transition: transform 0.2s ease-in-out;
            margin-bottom: 20px;
            height: 180px; /* Fixed height for equal alignment */
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .highlight-box:hover {
            transform: translateY(-5px);
            background-color: rgba(255, 255, 255, 0.2);
        }
        .stButton>button {
            background-color: #ff4b2b;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ff416c;
            transform: scale(1.05);
        }
        .header-img {
            width: 100%; /* Keep it responsive */
            height: 200px; /* Reduced height */
            object-fit: cover;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.6);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("🌍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Weather & Air Quality", "Historical Data"])

POPULAR_CITIES = [
    "New York", "Los Angeles", "London", "Tokyo", "Paris",
    "Chicago", "Houston", "San Diego", "Boston", "Denver"
]

city = st.sidebar.selectbox("Select a city", POPULAR_CITIES, index=0)

if page == "Home":
    st.markdown('<h1 class="main-title">Welcome to Real-Time Air Quality & Weather Dashboard!</h1>', unsafe_allow_html=True)

    st.markdown("### Why Use This Dashboard?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="highlight-box fade-in">
                <h3>🌦️ Real-Time Weather</h3>
                <p>Get live updates on temperature, humidity, and wind speed.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="highlight-box fade-in">
                <h3>🌫️ Air Quality Insights</h3>
                <p>Monitor AQI levels and understand pollution trends.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="highlight-box fade-in">
                <h3>📊 Historical Data</h3>
                <p>Analyze trends over time to plan your day better.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Explore Now 👇")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📍 Check Weather"):
            page = "Weather & Air Quality"
    with col2:
        if st.button("📈 View Historical Data"):
            page = "Historical Data"

if page == "Weather & Air Quality":
    st.title(f"🌤️ Weather & Air Quality in {city}")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    weather = requests.get(url).json()

    if weather:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌡️ Temperature", f"{weather['main']['temp']} °C")
            st.metric("💧 Humidity", f"{weather['main']['humidity']}%")
            st.metric("💨 Wind Speed", f"{weather['wind']['speed']} m/s")
        with col2:
            st.image(f"http://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png")
            st.write(f"**Condition:** {weather['weather'][0]['description'].title()}")

        aqi = 75
        st.metric("🌫️ AQI (US)", aqi)

        if aqi <= 50:
            st.success("Good 👍")
        elif aqi <= 100:
            st.info("Moderate 😐")
        elif aqi <= 150:
            st.warning("Unhealthy for Sensitive Groups 🤧")
        else:
            st.error("Unhealthy 😷")

    else:
        st.error("Weather data not available!")

if page == "Historical Data":
    st.title("📈 Historical Weather & Air Quality Data")

    data = pd.DataFrame({
        'Time': pd.date_range(start="2025-01-01", periods=24, freq='H'),
        'AQI': 50 + (pd.Series(range(24)) - 12).apply(lambda x: x * 3),
        'Temperature': 20 + (pd.Series(range(24)) - 12).apply(lambda x: x * 1.5)
    })

    fig_aqi = px.line(data, x='Time', y='AQI', title="AQI Over Time", markers=True)
    fig_temp = px.line(data, x='Time', y='Temperature', title="Temperature Over Time", markers=True)

    st.plotly_chart(fig_aqi)
    st.plotly_chart(fig_temp)

st.markdown("---")
st.caption("Developed using Streamlit")