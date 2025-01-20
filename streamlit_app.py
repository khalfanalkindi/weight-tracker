import duckdb
import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Khalfan Weight & BMI Tracker",
    page_icon="📈",
    layout="wide"
)

# Fixed height in meters
HEIGHT = 1.82

# Initial weight data
INITIAL_WEIGHT_DATA = [
    ("2024-11-06", 118.2),
    ("2024-11-13", 115.5),
    ("2024-11-19", 112.3),
    ("2024-11-27", 111.4),
    ("2024-12-04", 110.2),
    ("2024-12-11", 109.2),
    ("2024-12-18", 108.4),
    ("2024-12-25", 107.3),
    ("2025-01-01", 105.4),
    ("2025-01-08", 104.9),
    ("2025-01-15", 103.8),
]

# Database initialization
def initialize_db():
    conn = duckdb.connect("weight_tracker.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS weight_data (
        date VARCHAR PRIMARY KEY,
        weight DOUBLE
    )
    """)
    existing_data_count = conn.execute("SELECT COUNT(*) FROM weight_data").fetchone()[0]
    if existing_data_count == 0:
        conn.executemany("INSERT INTO weight_data (date, weight) VALUES (?, ?)", INITIAL_WEIGHT_DATA)
    conn.close()

# Fetch data from the database
def get_data():
    conn = duckdb.connect("weight_tracker.db")
    result = conn.execute("SELECT date, weight FROM weight_data ORDER BY date").fetchall()
    conn.close()
    return {row[0]: row[1] for row in result}

# Save new data to the database
def save_data(date, weight):
    conn = duckdb.connect("weight_tracker.db")
    conn.execute("INSERT INTO weight_data (date, weight) VALUES (?, ?) ON CONFLICT (date) DO UPDATE SET weight = ?", (date, weight, weight))
    conn.close()

# Initialize database
initialize_db()

# Load data into session state
if "weight_data" not in st.session_state:
    st.session_state.weight_data = get_data()

st.sidebar.title("Navigation")
st.sidebar.divider()

st.title("Khalfan Weight & BMI Tracker 📈")
st.write("Track my weight and BMI over time and visualize my progress.")

# Current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Input weight
user_input = st.text_input(f"My weight for today ({current_date}): (leave blank to skip)")

if user_input:
    try:
        new_weight = float(user_input)
        st.session_state.weight_data[current_date] = new_weight
        save_data(current_date, new_weight)
        st.success("New weight data saved!")
    except ValueError:
        st.error("Invalid input. Please enter a numeric value.")

# Convert the dictionary to a DataFrame
if st.session_state.weight_data:
    weight_df = pd.DataFrame(list(st.session_state.weight_data.items()), columns=["Date", "Weight"])
    weight_df["Date"] = pd.to_datetime(weight_df["Date"])
    weight_df.sort_values("Date", inplace=True)
    weight_df.reset_index(drop=True, inplace=True)

    # Calculate BMI
    weight_df["BMI"] = weight_df["Weight"] / (HEIGHT ** 2)

    # Display the DataFrame
    st.subheader("Your Weight & BMI Data")
    st.dataframe(weight_df)

    # Chart 1: Weight Progress
    st.subheader("Weight Progress Chart")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(weight_df["Date"], weight_df["Weight"], marker="o", linestyle="-", linewidth=2, label="Weight (kg)")
    ax1.set_title("Weight Over Time", fontsize=16)
    ax1.set_xlabel("Date", fontsize=12)
    ax1.set_ylabel("Weight (kg)", fontsize=12)
    ax1.grid(True)
    st.pyplot(fig1)

    # Chart 2: BMI Progress
    st.subheader("BMI Progress Chart")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(weight_df["Date"], weight_df["BMI"], marker="o", linestyle="-", linewidth=2, label="BMI", color="orange")
    ax2.set_title("BMI Over Time", fontsize=16)
    ax2.set_xlabel("Date", fontsize=12)
    ax2.set_ylabel("BMI", fontsize=12)
    ax2.grid(True)
    st.pyplot(fig2)

    # Chart 3: Weight and BMI Combined
    st.subheader("Weight and BMI Combined Chart")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(weight_df["Date"], weight_df["Weight"], marker="o", linestyle="-", linewidth=2, label="Weight (kg)")
    ax3.plot(weight_df["Date"], weight_df["BMI"], marker="o", linestyle="--", linewidth=2, label="BMI", color="orange")
    ax3.set_title("Weight and BMI Over Time", fontsize=16)
    ax3.set_xlabel("Date", fontsize=12)
    ax3.legend()
    ax3.grid(True)
    st.pyplot(fig3)
else:
    st.info("No weight data available. Enter your weight to start tracking.")
