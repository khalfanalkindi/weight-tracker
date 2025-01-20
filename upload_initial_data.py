import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("weight-track-ba123-7eb8e5bc0c15.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("Weight Tracker").sheet1  # Replace "Weight Tracker" with your sheet's name

# Initial weight data
initial_weight_data = [
    ["2024-11-06", 118.2],
    ["2024-11-13", 115.5],
    ["2024-11-19", 112.3],
    ["2024-11-27", 111.4],
    ["2024-12-04", 110.2],
    ["2024-12-11", 109.2],
    ["2024-12-18", 108.4],
    ["2024-12-25", 107.3],
    ["2025-01-01", 105.4],
    ["2025-01-08", 104.9],
    ["2025-01-15", 103.8],
]

# Upload data to the Google Sheet
for row in initial_weight_data:
    sheet.append_row(row)

print("Data uploaded to Google Sheets!")
