import pandas as pd
from google.cloud import bigquery

# Set your BigQuery credentials and project details
PROJECT_ID = "gcp_project_id"  # Replace with your project ID
DATASET_ID = "weather_data"  # Replace with your dataset name
TABLE_ID = "london"  # Replace with your table name

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_credential_json_file"

# Initialize BigQuery client
client = bigquery.Client()

# Load the CSV file into a Pandas DataFrame
file_path = "london.csv"  # Update the path if necessary
df = pd.read_csv(file_path, index_col=False)

# Clean the data to match BigQuery schema
df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)
#df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.date  # Convert 'date' to YYYY-MM-DD
df['is_day'] = df['is_day'].astype(bool)  # Convert 'is_day' to boolean
df['year'] = df['year'].astype(int)  # Ensure 'year' is an integer
df['month'] = df['month'].astype(int)  # Ensure 'month' is an integer
df['day'] = df['day'].astype(int)  # Ensure 'day' is an integer
df['hour'] = df['hour'].astype(int)  # Ensure 'hour' is an integer
df['cluster'] = df['cluster'].astype(int)  # Ensure 'cluster' is an integer

# Specify the full table ID
table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# Upload the DataFrame to BigQuery
job = client.load_table_from_dataframe(df, table_id)

# Wait for the job to complete
job.result()

# Confirm the data upload
print(f"Loaded {job.output_rows} rows into {table_id}.")
