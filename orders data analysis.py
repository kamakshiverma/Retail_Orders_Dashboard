import pandas as pd

# Read the CSV
df = pd.read_csv('orders.csv', na_values=['Not Available', 'unknown'])

# Clean column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Create new columns
df['discount'] = df['list_price'] * df['discount_percent'] * 0.01
df['sale_price'] = df['list_price'] - df['discount']
df['profit'] = df['sale_price'] - df['cost_price']

# Convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'], format="%Y-%m-%d")

# Drop unused columns
df.drop(columns=['list_price', 'cost_price', 'discount_percent'], inplace=True)

# Optional: preview
print(df.head())
