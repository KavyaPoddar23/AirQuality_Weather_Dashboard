import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image

load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
AIRVISUAL_API_KEY = os.getenv("AIRVISUAL_API_KEY")

st.set_page_config(page_title="🌤️ Real-Time Air Quality & Weather Dashboard", layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "Home"


# Custom CSS
st.markdown(
    """
    <style>
        body {
            background-color: #1e1e1e;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .main-title {
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            background: -webkit-linear-gradient(45deg, #ff7e5f, #feb47b);
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
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
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
        .metric-box {
            background-color: rgba(255, 255, 255, 0.08);
            padding: 16px;
            border-radius: 12px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.4);
            text-align: center;
            margin-bottom: 16px;
            transition: transform 0.2s ease-in-out;
        }
        .metric-box:hover {
            transform: translateY(-5px);
            background-color: rgba(255, 255, 255, 0.12);
        }
        .heading-box {
            padding: 12px;
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            border-radius: 12px; 
            box-shadow: 0px 4px 8px rgba(0,0,0,0.4);
            transition: transform 0.2s ease-in-out;
        }
        .heading-box:hover {
            transform: translateY(-5px);
            background-color: rgba(255, 255, 255, 0.2);
        }

        /* New Styles for Weather Icon and Condition Text */
        .weather-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }
        .weather-icon img {
            width: 120px; /* Increased size */
            height: 120px;
            object-fit: contain;
        }
        .weather-condition {
            font-size: 22px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 10px;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
st.sidebar.title("🌍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Weather & Air Quality", "Historical Data"], index=["Home", "Weather & Air Quality", "Historical Data"].index(st.session_state.page))

# Popular Cities Dropdown
POPULAR_CITIES = [
    "Tokyo", "Los Angeles", "New York", "London", "Paris",
    "Chicago", "Houston", "San Diego", "Boston", "Denver"
]
city = st.sidebar.selectbox("Select a city", POPULAR_CITIES, index=0)

# Home Page
# Home Page
if page == "Home":
    st.markdown(
        """
        <div class="heading-box">
            <h1 class="main-title">Welcome to Real-Time Air Quality & Weather Dashboard!</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display images in columns
    col1, col2, col3 = st.columns(3)
    img_width = 250
    img_height = 350

    img1 = Image.open("image1.jpg").resize((img_width, img_height))
    img2 = Image.open("image2.jpg").resize((img_width, img_height))
    img3 = Image.open("image3.jpg").resize((img_width, img_height))

    with col1:
        st.image(img1, width=img_width)
    with col2:
        st.image(img2, width=img_width)
    with col3:
        st.image(img3, width=img_width)

    # Why Use This Dashboard Section
    st.markdown("### Why Use This Dashboard?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="highlight-box">
                <h3>🌦️ Real-Time Weather</h3>
                <p>Get live updates on temperature, humidity, and wind speed.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="highlight-box">
                <h3>🌫️ Air Quality Insights</h3>
                <p>Monitor AQI levels and understand pollution trends.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="highlight-box">
                <h3>📊 Historical Data</h3>
                <p>Analyze trends over time to plan your day better.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Weather & Air Quality Page
if page == "Weather & Air Quality":
    st.markdown(
        f"""
        <div class="heading-box">
            <h1 class="main-title">🌤️ Weather & Air Quality in {city}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    weather = requests.get(url).json()

    if weather:
        st.image(f"http://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png", width=100)
        st.write(f"**Condition:** {weather['weather'][0]['description'].title()}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='metric-box'>🌡️ Temperature: {weather['main']['temp']} °C</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-box'>🌅 Sunrise: {datetime.fromtimestamp(weather['sys']['sunrise']).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)           
            st.markdown(f"<div class='metric-box'>🌍 Visibility: {weather.get('visibility', 0) / 1000} km</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div class='metric-box'>💧 Humidity: {weather['main']['humidity']}%</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-box'>🌇 Sunset: {datetime.fromtimestamp(weather['sys']['sunset']).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-box'>📏 Pressure: {weather['main']['pressure']} hPa</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='metric-box'>💨 Wind Speed: {weather['wind']['speed']} m/s</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-box'>💭 Cloudiness: {weather['clouds']['all']}%</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-box'>🌡️ Feels Like: {weather['main']['feels_like']} °C</div>", unsafe_allow_html=True)

        # AQI Display
    # Map cities to their corresponding state and country
if page == "Weather & Air Quality":
    CITY_STATE_COUNTRY_MAP = {
        "Tokyo": ("Tokyo", "Japan"),
        "Los Angeles": ("California", "USA"),
        "New York": ("New York", "USA"),
        "London": ("England", "United Kingdom"),
        "Paris": ("Ile-de-France", "France"),
        "Chicago": ("Illinois", "USA"),
        "Houston": ("Texas", "USA"),
        "San Diego": ("California", "USA"),
        "Boston": ("Massachusetts", "USA"),
        "Denver": ("Colorado", "USA")
    }

    state, country = CITY_STATE_COUNTRY_MAP.get(city, (None, None))

    if state and country:
        aqi_url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={AIRVISUAL_API_KEY}"
        try:
            aqi_response = requests.get(aqi_url).json()

            # Debugging: Print the response for inspection
            print(f"API Response for {city}: {aqi_response}")

            if aqi_response.get('status') == 'success' and 'data' in aqi_response:
                try:
                    aqi = aqi_response['data']['current']['pollution']['aqius']
                    st.metric("🌫️ AQI (US)", aqi)

                    # AQI Status Messages
                    if aqi <= 50:
                        st.success("Good 👍")
                        st.write("➡️ Air quality is satisfactory, and air pollution poses little or no risk.")
                    elif aqi <= 100:
                        st.info("Moderate 😐")
                        st.write("➡️ Air quality is acceptable. However, there may be a moderate health concern for some sensitive people.")
                    elif aqi <= 150:
                        st.warning("Unhealthy for Sensitive Groups 🤧")
                        st.write("➡️ Members of sensitive groups may experience health effects. General public not likely affected.")
                    elif aqi <= 200:
                        st.error("Unhealthy 😷")
                        st.write("➡️ Everyone may begin to experience health effects; sensitive groups may experience more serious effects.")
                    elif aqi <= 300:
                        st.error("Very Unhealthy 😨")
                        st.write("➡️ Health alert: everyone may experience more serious health effects.")
                    else:
                        st.error("Hazardous ☠️")
                        st.write("➡️ Health warning: emergency conditions. Everyone more likely to be affected.")
                except KeyError:
                    st.error("AQI data not available! (Missing Key)")
            else:
                error_message = aqi_response.get('data', {}).get('message', 'No data available')
                st.error(f"AQI data not available for {city}")

        except Exception as e:
            st.error(f"Failed to fetch AQI data: {e}")

    else:
        st.error("Invalid city selection for AQI data.")

    # Create a dataframe with AQI data for comparison
    aqi_data = []
    for city, (state, country) in CITY_STATE_COUNTRY_MAP.items():
        aqi_url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={AIRVISUAL_API_KEY}"
        try:
            aqi_response = requests.get(aqi_url).json()
            if aqi_response.get('status') == 'success' and 'data' in aqi_response:
                aqi = aqi_response['data']['current']['pollution']['aqius']
                aqi_data.append({'City': city, 'AQI': aqi})
        except Exception as e:
            print(f"Failed to fetch AQI for {city}: {e}")

    # Convert to DataFrame
    df_aqi = pd.DataFrame(aqi_data)

    if not df_aqi.empty:
        st.markdown("### 🌍 AQI Comparison Across Cities")
        
        # Create a bar chart using Plotly
        fig_aqi_comparison = px.bar(
            df_aqi,
            x='City',
            y='AQI',
            color='AQI',
            color_continuous_scale='plasma',
            labels={'AQI': 'Air Quality Index (US)'},
            title="Comparison of AQI Levels Across Cities"
        )
        fig_aqi_comparison.update_layout(
            xaxis_title="City",
            yaxis_title="AQI Level",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
            title_font=dict(size=24)
        )

        st.plotly_chart(fig_aqi_comparison, use_container_width=True)


# Historical Data Page
if page == "Historical Data":
    st.markdown(
        """
        <div class="heading-box">
            <h1 class="main-title">📈 Historical Weather & Air Quality Data</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    data = pd.DataFrame({
        'Time': pd.date_range(start="2025-01-01", periods=24, freq='H'),
        'AQI': 50 + (pd.Series(range(24)) - 12).apply(lambda x: x * 3),
        'Temperature': 20 + (pd.Series(range(24)) - 12).apply(lambda x: x * 1.5)
    })

    # AQI Chart
    fig_aqi = px.line(data, x='Time', y='AQI', title="AQI Over Time", markers=True)
    st.plotly_chart(fig_aqi)

    # Temperature Chart
    fig_temp = px.line(data, x='Time', y='Temperature', title="Temperature Over Time", markers=True)
    st.plotly_chart(fig_temp)

# Footer Section (Dynamic based on page)
st.markdown("---")
st.markdown("### Explore Now 👇")

if page == "Home":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📍 Check Weather", key="weather_1"):
            st.session_state.page = "Weather & Air Quality"
            st.rerun()
    with col2:
        if st.button("📈 View Historical Data", key="history_1"):
            st.session_state.page = "Historical Data"
            st.rerun()

if page == "Weather & Air Quality":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Home", key="home_1"):
            st.session_state.page = "Home"
            st.rerun()
    with col2:
        if st.button("📈 View Historical Data", key="history_2"):
            st.session_state.page = "Historical Data"
            st.rerun()

if page == "Historical Data":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Home", key="home_2"):
            st.session_state.page = "Home"
            st.rerun()
    with col2:
        if st.button("📍 Check Weather", key="weather_2"):
            st.session_state.page = "Weather & Air Quality"
            st.rerun()

# Credit
st.caption("Developed using Streamlit by Kavya Poddar")