import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set Streamlit page config
st.set_page_config(page_title="Uber Ride Data Dashboard", layout="wide")

st.title("🚖 Uber Ride Bookings Dashboard (NCR)")

# Upload CSV
uploaded_file = st.file_uploader("Upload the Uber ride bookings CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Combine Date and Time into a single datetime column
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['weekday'] = df['datetime'].dt.day_name()
    df['month_year'] = df['datetime'].dt.to_period('M')

    # Drop columns with too many missing values
    threshold = 0.7 * len(df)
    df = df.dropna(thresh=threshold, axis=1)

    # Sidebar filters
    st.sidebar.header("Filters")
    selected_years = st.sidebar.multiselect("Select year(s):", sorted(df['year'].dropna().unique()), default=df['year'].dropna().unique())
    df = df[df['year'].isin(selected_years)]

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.markdown("---")

    # 1. Bookings per Year
    st.subheader("📅 Bookings per Year")
    bookings_per_year = df['year'].value_counts().sort_index()
    st.bar_chart(bookings_per_year)

    # 2. Monthly Booking Trend
    st.subheader("📈 Monthly Booking Trend")
    monthly_bookings = df['month_year'].value_counts().sort_index()
    st.line_chart(monthly_bookings)

    # 3. Top Pickup and Drop Locations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Top 10 Pickup Locations")
        top_pickup = df['Pickup Location'].value_counts().head(10)
        st.bar_chart(top_pickup)

    with col2:
        st.subheader("📌 Top 10 Drop Locations")
        top_drop = df['Drop Location'].value_counts().head(10)
        st.bar_chart(top_drop)

    # 4. Average Booking Value and Ride Distance Over Time
    st.subheader("💰 Avg Booking Value & Distance Over Time")
    df_monthly = df.groupby('month_year')[['Booking Value', 'Ride Distance']].mean().dropna()
    st.line_chart(df_monthly)

    # 5. Payment Method Distribution
    if 'Payment Method' in df.columns:
        st.subheader("💳 Payment Method Distribution")
        payment_counts = df['Payment Method'].value_counts()
        st.dataframe(payment_counts)
        fig, ax = plt.subplots()
        payment_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

    # 6. Ratings Distribution
    if 'Driver Ratings' in df.columns and 'Customer Rating' in df.columns:
        st.subheader("🌟 Ratings Distribution")
        col3, col4 = st.columns(2)

        with col3:
            st.write("**Driver Ratings**")
            st.bar_chart(df['Driver Ratings'].dropna().value_counts().sort_index())

        with col4:
            st.write("**Customer Ratings**")
            st.bar_chart(df['Customer Rating'].dropna().value_counts().sort_index())

    # 7. Cancellation Reasons
    if 'Driver Cancellation Reason' in df.columns:
        st.subheader("❌ Driver Cancellation Reasons")
        st.bar_chart(df['Driver Cancellation Reason'].value_counts())

    if 'Reason for cancelling by Customer' in df.columns:
        st.subheader("❌ Customer Cancellation Reasons")
        st.bar_chart(df['Reason for cancelling by Customer'].value_counts())

    # Footer
    st.markdown("---")
    st.markdown("🚀 Built with Streamlit | Developed by You 😎")

else:
    st.warning("👆 Upload a CSV file to get started.")
