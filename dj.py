import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="GigFlow MVP", layout="wide")

# ------------------ MOCK DATABASE ------------------
artists = pd.DataFrame({
    "Name": ["Shiv Band", "Unwind Voices", "Sagar Waliya", "Roohine"],
    "Type": ["Band", "Band", "Band", "Band"],
    "Genre": ["Rock", "Bollywood", "Sufi", "Sufi"],
    "Cost": [50000, 40000, 45000, 42000],
    "City": ["Nagpur", "Nagpur", "Nagpur", "Nagpur"],
    "Rating": [4.7, 4.5, 4.6, 4.4],
    "Available Dates": [
        "2026-04-20", "2026-04-22", "2026-04-25", "2026-04-23"
    ],
    "Image": [
        "https://images.unsplash.com/photo-1507878866276-a947ef722fee",
        "https://images.unsplash.com/photo-1464375117522-1311dd6b1f76",
        "https://images.unsplash.com/photo-1497032205916-ac775f0649ae",
        "https://images.unsplash.com/photo-1511379938547-c1f69419868d"
    ]
})

bookings = []

# ------------------ SIDEBAR ------------------
st.sidebar.title("🎧 GigFlow MVP")
page = st.sidebar.radio("Navigate", [
    "Home", "Artist Profiles", "Search & Filter", "Calendar", "Bookings", "Clubs Near Me"
])

# ------------------ HOME ------------------
if page == "Home":
    st.title("🎤 Book Artists Like BookMyShow")
    st.write("Find DJs & Live Bands near you and book instantly")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Artists", len(artists))
    with col2:
        st.metric("Avg Cost", f"₹{int(artists['Cost'].mean())}")

# ------------------ ARTIST PROFILES ------------------
elif page == "Artist Profiles":
    st.title("🎧 Artist Profiles")

    for i, row in artists.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(row["Image"], use_container_width=True)
            with col2:
                st.subheader(row["Name"])
                st.write(f"🎵 {row['Genre']} | {row['Type']}")
                st.write(f"📍 {row['City']}")
                st.write(f"⭐ Rating: {row['Rating']}")
                st.write(f"💰 Cost: ₹{row['Cost']}")
                st.write(f"📅 Available: {row['Available Dates']}")

                if st.button(f"Book {row['Name']}", key=i):
                    bookings.append({
                        "Artist": row['Name'],
                        "Cost": row['Cost'],
                        "Date": row['Available Dates']
                    })
                    st.success("Booking Request Sent!")

# ------------------ SEARCH & FILTER ------------------
elif page == "Search & Filter":
    st.title("🔍 Find Your Artist")

    genre = st.selectbox("Genre", ["All"] + list(artists['Genre'].unique()))
    max_price = st.slider("Max Budget", 10000, 100000, 50000)
    city = st.selectbox("City", ["All"] + list(artists['City'].unique()))

    filtered = artists.copy()

    if genre != "All":
        filtered = filtered[filtered['Genre'] == genre]
    if city != "All":
        filtered = filtered[filtered['City'] == city]

    filtered = filtered[filtered['Cost'] <= max_price]

    st.write(f"### Results: {len(filtered)} artists")

    for i, row in filtered.iterrows():
        st.write(f"**{row['Name']}** - ₹{row['Cost']} - {row['Genre']}")

# ------------------ CALENDAR ------------------
elif page == "Calendar":
    st.title("📅 Availability Calendar")

    artists['Available Dates'] = pd.to_datetime(artists['Available Dates'])
    selected_date = st.date_input("Select Date", datetime.today())

    available = artists[artists['Available Dates'] == pd.to_datetime(selected_date)]

    st.write(f"Available Artists: {len(available)}")
    st.dataframe(available[["Name", "Type", "Cost"]])

# ------------------ BOOKINGS ------------------
elif page == "Bookings":
    st.title("💳 Booking Dashboard")

    if len(bookings) == 0:
        st.info("No bookings yet")
    else:
        df = pd.DataFrame(bookings)
        st.dataframe(df)
        st.metric("Total Revenue", f"₹{df['Cost'].sum()}")

# ------------------ MAP ------------------
elif page == "Clubs Near Me":
    st.title("📍 Clubs & Pubs Near You")

    m = folium.Map(location=[21.1458, 79.0882], zoom_start=12)

    clubs = [
        {"name": "Club A", "lat": 21.145, "lon": 79.088},
        {"name": "Pub B", "lat": 21.150, "lon": 79.090},
        {"name": "Lounge C", "lat": 21.140, "lon": 79.085}
    ]

    for club in clubs:
        folium.Marker(
            [club['lat'], club['lon']],
            popup=club['name'],
            icon=folium.Icon(color="purple", icon="music")
        ).add_to(m)

    st_folium(m, width=700, height=500)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("🚀 GigFlow MVP - Artist Booking SaaS Prototype")
