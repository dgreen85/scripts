#Primarily created with OpenAI's ChatGPT 4o
#This script was writen to combine URLs from a GA4 landing page + query string report export. 

import pandas as pd

# Load your data into a DataFrame (assuming it's in the same directory as the script)
df = pd.read_csv('data.csv')

# Remove query parameters from URLs
df['Base URL'] = df['Landing page + query string'].str.split('?').str[0]

# Convert columns to numeric, handling errors by coercing invalid values to NaN
df['Sessions'] = pd.to_numeric(df['Sessions'], errors='coerce')
df['Engaged sessions'] = pd.to_numeric(df['Engaged sessions'], errors='coerce')
df['Bounce rate'] = pd.to_numeric(df['Bounce rate'], errors='coerce').fillna(0)
df['Session key event rate'] = pd.to_numeric(df['Session key event rate'], errors='coerce').fillna(0)

# Group by the base URL and sum numeric columns
grouped_df = df.groupby('Base URL').agg({
    'Sessions': 'sum',
    'Engaged sessions': 'sum',
    'Active users': 'sum',
    'New users': 'sum',
    'Key events': 'sum',
    'Conversion Value': 'sum',
    # Calculate bounce rate: 1 - (Engaged sessions / Sessions)
    'Bounce rate': lambda x: 1 - (df.loc[x.index, 'Engaged sessions'].sum() / df.loc[x.index, 'Sessions'].sum()) if df.loc[x.index, 'Sessions'].sum() != 0 else 0
}).reset_index()

# Save the aggregated data to a CSV file
grouped_df.to_csv('aggregated_ga4_data.csv', index=False)

print("Aggregated data saved to 'aggregated_ga4_data.csv'.")
