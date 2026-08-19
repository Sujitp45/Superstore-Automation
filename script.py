import os
import random
from datetime import datetime, timedelta
import pandas as pd
import gdown

# १. Google Drive File ID घेणे
FILE_ID = os.environ['GDRIVE_FILE_ID']

# २. gdown द्वारे फाईल डाऊनलोड करणे
url = f'https://drive.google.com/uc?id={FILE_ID}'
output = 'G_Superstore.csv'
gdown.download(url, output, quiet=False)

# ३. CSV फाईल वाचणे
df = pd.read_csv(output)

# ४. 'Order Date' कॉलमचे अचूक नाव शोधणे (Capitalization किंवा space मूळे होणारा फरक ओळखण्यासाठी)
date_col = None
for col in df.columns:
    if col.strip().lower().replace('_', ' ') == 'order date':
        date_col = col
        break

if not date_col:
    raise KeyError(f"Order Date कॉलम सापडला नाही. उपलब्ध कॉलम: {list(df.columns)}")

# ५. तारीख फॉरमॅट सेट करणे
df[date_col] = pd.to_datetime(df[date_col])
last_date = df[date_col].max()
next_date = last_date + timedelta(days=1)

# ६. नवीन ऑर्डर्स तयार करणे
num_new_orders = random.randint(15, 20)
new_rows = []

for _ in range(num_new_orders):
    sample_row = df.sample(1).iloc[0].to_dict()
    sample_row[date_col] = next_date
    
    # Ship Date कॉलम असल्यास तो अपडेट करणे
    for col in df.columns:
        if col.strip().lower().replace('_', ' ') == 'ship date':
            sample_row[col] = next_date + timedelta(days=random.randint(1, 5))
            
    if 'Order ID' in df.columns:
        sample_row['Order ID'] = f"CA-{next_date.year}-{random.randint(100000, 999999)}"
    if 'Sales' in df.columns:
        sample_row['Sales'] = round(random.uniform(10.0, 500.0), 2)
    if 'Quantity' in df.columns:
        sample_row['Quantity'] = random.randint(1, 5)
    if 'Discount' in df.columns:
        sample_row['Discount'] = round(random.uniform(0.0, 0.3), 2)
    if 'Profit' in df.columns:
        sample_row['Profit'] = round(sample_row['Sales'] * random.uniform(0.1, 0.4), 2)
        
    new_rows.append(sample_row)

# ७. नवीन डेटा अपडेट करून सेव्ह करणे
updated_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
updated_df.to_csv("G_Superstore.csv", index=False)

print(f"Successfully added {num_new_orders} orders for date {next_date.strftime('%Y-%m-%d')}!")
