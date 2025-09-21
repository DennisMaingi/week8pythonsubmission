import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('ncr_ride_bookings.csv')

# Quick preview
print(df.head())
print("Shape:", df.shape)
df.info()
print(df.describe())

# Combine 'Date' and 'Time' into a single datetime column
df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['weekday'] = df['datetime'].dt.day_name()
df['month_year'] = df['datetime'].dt.to_period('M')

# Drop columns with more than 70% missing values
threshold = 0.7 * len(df)
df = df.dropna(thresh=threshold, axis=1)

# ===========================
# 1. Bookings per Year
# ===========================
bookings_per_year = df['year'].value_counts().sort_index()
plt.figure(figsize=(8, 4))
bookings_per_year.plot(kind='bar')
plt.title('Bookings per Year')
plt.xlabel('Year')
plt.ylabel('Number of Bookings')
plt.tight_layout()
plt.show()

# ===========================
# 2. Monthly Bookings Trend
# ===========================
monthly_bookings = df['month_year'].value_counts().sort_index()
plt.figure(figsize=(12, 5))
monthly_bookings.plot()
plt.title('Monthly Bookings Trend')
plt.xlabel('Month-Year')
plt.ylabel('Number of Bookings')
plt.tight_layout()
plt.show()

# ===========================
# 3. Top Pickup and Drop Locations
# ===========================
top_pickup = df['Pickup Location'].value_counts().head(10)
top_drop = df['Drop Location'].value_counts().head(10)

plt.figure(figsize=(8, 4))
top_pickup.plot(kind='barh', title='Top 10 Pickup Locations')
plt.xlabel('Number of Bookings')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 4))
top_drop.plot(kind='barh', title='Top 10 Drop Locations')
plt.xlabel('Number of Bookings')
plt.tight_layout()
plt.show()

# ===========================
# 4. Average Booking Value and Ride Distance Over Time
# ===========================
df_monthly = df.groupby('month_year').agg({
    'Booking Value': 'mean',
    'Ride Distance': 'mean'
}).dropna()

df_monthly.plot(title='Avg Booking Value and Ride Distance Over Time', figsize=(10, 5))
plt.ylabel('Average')
plt.xlabel('Month-Year')
plt.tight_layout()
plt.show()

# ===========================
# 5. Payment Method Distribution
# ===========================
if 'Payment Method' in df.columns:
    plt.figure(figsize=(6, 6))
    df['Payment Method'].value_counts().plot(
        kind='pie', autopct='%1.1f%%', title='Payment Method Distribution')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

# ===========================
# 6. Ratings Distribution
# ===========================
if 'Driver Ratings' in df.columns and 'Customer Rating' in df.columns:
    df[['Driver Ratings', 'Customer Rating']].dropna().hist(bins=10, figsize=(10, 4))
    plt.suptitle('Ratings Distribution')
    plt.tight_layout()
    plt.show()

# ===========================
# 7. Cancellation Reasons
# ===========================
if 'Driver Cancellation Reason' in df.columns:
    plt.figure(figsize=(8, 4))
    df['Driver Cancellation Reason'].value_counts().plot(
        kind='barh', title='Driver Cancellation Reasons')
    plt.tight_layout()
    plt.show()

if 'Reason for cancelling by Customer' in df.columns:
    plt.figure(figsize=(8, 4))
    df['Reason for cancelling by Customer'].value_counts().plot(
        kind='barh', title='Customer Cancellation Reasons')
    plt.tight_layout()
    plt.show()

# ===========================
# Show columns and save cleaned data
# ===========================
print("Final columns in dataset:", df.columns.tolist())


