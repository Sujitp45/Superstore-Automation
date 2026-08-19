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

# ३. डाऊनलोड झालेली CSV फाईल वाचणे
df = pd.read_csv(output)

# ४. 'Order Date' तारीख स्वरूपात बदलणे
df['Order Date'] = pd.to_datetime(df['Order Date'])
last_date = df['Order Date'].max()
next_date = last_date + timedelta(days=1)

# ५. नवीन ऑर्डर्स तयार करणे
num_new_orders = random.randint(15, 20)
new_rows = []

for _ in range(num_new_orders):
    sample_row = df.sample(1).iloc[0].to_dict()
    sample_row['Order Date'] = next_date
    sample_row['Ship Date'] = next_date + timedelta(days=random.randint(1, 5))
    sample_row['Order ID'] = f"CA-{next_date.year}-{random.randint(100000, 999999)}"
    sample_row['Sales'] = round(random.uniform(10.0, 500.0), 2)
    sample_row['Quantity'] = random.randint(1, 5)
    sample_row['Discount'] = round(random.uniform(0.0, 0.3), 2)
    sample_row['Profit'] = round(sample_row['Sales'] * random.uniform(0.1, 0.4), 2)
    new_rows.append(sample_row)

# ६. अपडेटेड डेटा लोकल फाईलमध्ये सेव्ह करणे
updated_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
updated_df.to_csv("G_Superstore.csv", index=False)

print(f"Successfully added {num_new_orders} orders for date {next_date.strftime('%Y-%m-%d')}!")
