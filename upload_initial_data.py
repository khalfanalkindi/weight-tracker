import duckdb

# Connect to DuckDB database (creates a file named weight_tracker.db)
conn = duckdb.connect("weight_tracker.db")

# Create table if it doesn't exist
conn.execute("""
CREATE TABLE IF NOT EXISTS weight_data (
    date VARCHAR PRIMARY KEY,
    weight DOUBLE
)
""")

# Sample weight data
initial_weight_data = [
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

# Insert data into the database
for date, weight in initial_weight_data:
    conn.execute("INSERT INTO weight_data (date, weight) VALUES (?, ?) ON CONFLICT (date) DO NOTHING", (date, weight))

print("Initial data uploaded to DuckDB!")
