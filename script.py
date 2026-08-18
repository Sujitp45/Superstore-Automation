from datetime import datetime, timedelta
import io
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import numpy as np
import pandas as pd

# Fetch credentials and File ID from GitHub Secrets
token_info = json.loads(os.environ['GDRIVE_TOKEN'])

# Service Account credentials वापरा:
creds = Credentials.from_service_account_info(
    token_info, scopes=['https://www.googleapis.com/auth/drive.file']
)

service = build('drive', 'v3', credentials=creds)
FILE_ID = os.environ['GDRIVE_FILE_ID']

# 1. Download existing CSV file from Google Drive
request = service.files().get_media(fileId=FILE_ID)
file_stream = io.BytesIO()
downloader = MediaIoBaseDownload(file_stream, request)
done = False
while not done:
  _, done = downloader.next_chunk()

file_stream.seek(0)
df = pd.read_csv(file_stream, encoding='latin1')

# 2. Parse Order.Date and determine the next order date
df['Order.Date'] = pd.to_datetime(df['Order.Date'], errors='coerce')
last_date = df['Order.Date'].max()
new_order_date = last_date + timedelta(days=1)

# 3. Generate random 15 to 20 new orders
np.random.seed(None)
num_new_orders = np.random.randint(15, 21)

new_rows = []
for i in range(num_new_orders):
  sample_row = df.sample(1).iloc[0].copy()
  sample_row['Order.Date'] = new_order_date.strftime('%Y-%m-%d')
  sample_row['Ship.Date'] = (new_order_date + timedelta(days=2)).strftime(
      '%Y-%m-%d'
  )
  sample_row['Sales'] = int(np.random.randint(100, 1000))
  sample_row['Profit'] = float(
      round(sample_row['Sales'] * np.random.uniform(0.15, 0.35), 2)
  )
  sample_row['Quantity'] = int(np.random.randint(1, 6))
  sample_row['Year'] = int(new_order_date.year)
  new_rows.append(sample_row)

# 4. Append new rows to the dataframe
df_new_day = pd.DataFrame(new_rows)
updated_df = pd.concat([df, df_new_day], ignore_index=True)
updated_df['Order.Date'] = pd.to_datetime(updated_df['Order.Date']).dt.strftime(
    '%Y-%m-%d'
)

# 5. Upload updated CSV back to Google Drive
temp_csv = 'updated_output.csv'
updated_df.to_csv(temp_csv, index=False)

media = MediaFileUpload(temp_csv, mimetype='text/csv', resumable=True)
service.files().update(fileId=FILE_ID, media_body=media).execute()

if os.path.exists(temp_csv):
  os.remove(temp_csv)

print(
    f"Successfully updated Drive CSV for date:"
    f' {new_order_date.strftime("%Y-%m-%d")}'
)
