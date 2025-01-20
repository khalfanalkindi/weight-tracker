import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
def setup_gsheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("weight-track-ba123-7eb8e5bc0c15.json", scope)
    client = gspread.authorize(creds)
    return client

# Load data from Google Sheets
def load_data_from_gsheets(sheet_name="Weight Tracker"):
    client = setup_gsheets()
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    return {row["Date"]: row["Weight"] for row in data}

# Save data to Google Sheets
def save_data_to_gsheets(data, sheet_name="Weight Tracker"):
    client = setup_gsheets()
    sheet = client.open(sheet_name).sheet1
    sheet.clear()  # Clear the existing data
    sheet.append_row(["Date", "Weight"])  # Add headers
    for date, weight in data.items():
        sheet.append_row([date, weight])

# Fixed height in meters
HEIGHT = 1.82

# Load initial data from Google Sheets
if "weight_data" not in st.session_state:
    try:
        st.session_state.weight_data = load_data_from_gsheets()
    except Exception as e:
        st.error("Failed to load data from Google Sheets!")
        st.session_state.weight_data = {}

st.title("Weight & BMI Tracker")
st.write("Track your weight and BMI over time and visualize your progress.")

# Current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Input weight
user_input = st.text_input(f"Enter your weight for today ({current_date}) or leave blank to skip:")

if user_input:
    try:
        new_weight = float(user_input)
        st.session_state.weight_data[current_date] = new_weight
        save_data_to_gsheets(st.session_state.weight_data)  # Save to Google Sheets
        st.success("New weight data saved!")
    except ValueError:
        st.error("Invalid input. Please enter a numeric value.")

# Convert the dictionary to a DataFrame
if st.session_state.weight_data:
    weight_df = pd.DataFrame(list(st.session_state.weight_data.items()), columns=["Date", "Weight"])
    weight_df["Date"] = pd.to_datetime(weight_df["Date"])  # Ensure Date is in datetime format
    weight_df.sort_values("Date", inplace=True)  # Sort data by date
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
