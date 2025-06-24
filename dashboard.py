import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Retail Orders Dashboard", layout="wide")
st.title("📊 Retail Orders Dashboard with Prediction")

# 📁 File uploader
uploaded_file = st.file_uploader("Upload your orders.csv file", type=['csv'])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("orders.csv")  # Default file in project folder

# 🔄 Data preprocessing
df.columns = df.columns.str.lower().str.replace(' ', '_')
df['discount'] = df['list_price'] * df['discount_percent'] * 0.01
df['sale_price'] = df['list_price'] - df['discount']
df['profit'] = df['sale_price'] - df['cost_price']
df['order_date'] = pd.to_datetime(df['order_date'])
df['day'] = df['order_date'].dt.dayofyear

# 📅 Date filter
st.sidebar.header("Filter by Date")
date_range = st.sidebar.date_input("Select range", [df['order_date'].min(), df['order_date'].max()])
if len(date_range) == 2:
    df = df[(df['order_date'] >= pd.to_datetime(date_range[0])) & (df['order_date'] <= pd.to_datetime(date_range[1]))]

# 📊 Show table
st.subheader("Filtered Order Data")
st.dataframe(df.head())

# 📈 Line chart - Profit Over Time
fig = px.line(df, x='order_date', y='profit', title="Profit Over Time")
st.plotly_chart(fig, use_container_width=True)

# 🏙️ Top 5 Cities
st.subheader("Top 5 Cities by Profit")
top_cities = df.groupby('city')['profit'].sum().sort_values(ascending=False).head(5)
st.bar_chart(top_cities)

# 🔮 Profit Prediction
st.subheader("📈 Predict Profit on a Future Day")
future_day = st.slider("Pick a day of year (1 to 365)", 1, 365, 200)
X = df[['day']]
y = df['profit']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
predicted = model.predict([[future_day]])
st.success(f"Predicted profit on day {future_day}: ₹{predicted[0]:.2f}")

# 📤 Download processed Excel
if st.button("Export to Excel"):
    df.to_excel("processed_orders.xlsx", index=False)
    with open("processed_orders.xlsx", "rb") as f:
        st.download_button("Download Excel", f, file_name="processed_orders.xlsx")
