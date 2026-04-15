import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Artist Management App", layout="wide")

# ---------------- Sample Data ----------------
dj_data = pd.DataFrame({
    "Name": ["DJ Alpha", "DJ Blaze", "DJ Night"],
    "Cost": [20000, 30000, 25000],
    "Available Dates": ["2026-04-20", "2026-04-22", "2026-04-25"],
    "Image": [
        "https://images.search.yahoo.com/search/images;_ylt=AwrgxTSmNt9pmAIAQXVXNyoA;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA3BpdnM-?p=shivam+joshi&fr2=piv-web&type=E210US885G0&fr=mcafee&imgurl=https%3A%2F%2Fwww.indianspeakerbureau.com%2Fimg%2F1626169842_4ffcc45e-0474-41f5-8939-8147099135a4.jpeg",
        "https://images.unsplash.com/photo-1507874457470-272b3c8d8ee2",
        "https://images.unsplash.com/photo-1497032205916-ac775f0649ae"
    ]
})

band_data = pd.DataFrame({
    "Name": ["Rockers", "Jazz Band", "Fusion Crew"],
    "Cost": [50000, 45000, 60000],
    "Available Dates": ["2026-04-21", "2026-04-23", "2026-04-26"],
    "Image": [
        "https://images.unsplash.com/photo-1507878866276-a947ef722fee",
        "https://images.unsplash.com/photo-1464375117522-1311dd6b1f76",
        "https://images.unsplash.com/photo-1518972559570-7cc1309f3229"
    ]
})

# ---------------- Sidebar ----------------
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Artist Profiles", "Calendar View", "Clubs Near Me"])

# ---------------- Artist Profiles ----------------
if section == "Artist Profiles":
    st.title("🎧 Artist Profiles")
    category = st.selectbox("Select Category", ["DJ", "Live Band"])

    data = dj_data if category == "DJ" else band_data

    for i, row in data.iterrows():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(row["Image"], use_container_width=True)
        with col2:
            st.subheader(row["Name"])
            st.write(f"💰 Cost: ₹{row['Cost']}")
            st.write(f"📅 Available: {row['Available Dates']}")
            st.button(f"Book {row['Name']}", key=i)

# ---------------- Calendar View ----------------
elif section == "Calendar View":
    st.title("📅 Artist Availability Calendar")

    combined = pd.concat([dj_data.assign(Type="DJ"), band_data.assign(Type="Band")])
    combined['Available Dates'] = pd.to_datetime(combined['Available Dates'])

    selected_date = st.date_input("Select Date")

    available = combined[combined['Available Dates'] == pd.to_datetime(selected_date)]

    st.write(f"### Available Artists on {selected_date}")
    st.write(f"Total Available: {len(available)}")

    st.dataframe(available[["Name", "Type", "Cost"]])

# ---------------- Map View ----------------
elif section == "Clubs Near Me":
    st.title("📍 Clubs & Pubs Near Me")

    # Default location (Nagpur approx)
    m = folium.Map(location=[21.1458, 79.0882], zoom_start=12)

    clubs = [
        {"name": "Club A", "lat": 21.145, "lon": 79.088},
        {"name": "Pub B", "lat": 21.150, "lon": 79.090},
        {"name": "Lounge C", "lat": 21.140, "lon": 79.085}
    ]

    for club in clubs:
        folium.Marker(
            [club["lat"], club["lon"]],
            popup=club["name"],
            icon=folium.Icon(color="purple", icon="music")
        ).add_to(m)

    st_data = st_folium(m, width=700, height=500)

# ---------------- Footer ----------------
st.markdown("---")
st.markdown("🚀 Built for Artist Management Business Model")
