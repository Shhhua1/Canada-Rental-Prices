# Import necessary libraries
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Import analysis functions from data_analysis.py
from data_analysis import (
    price_per_province,
    mapped_price,
    price_per_housetype,
    price_per_sqft,
    lease_term_analysis,
    outlier_analysis,
    rental_price_distribution_analysis,
    pie_chart_analysis_house_type,
    pie_chart_analysis_province,
    scatter_plot_analysis
)

# Read the data from the CSV file
try:
    df = pd.read_csv('rentfaster_cleaned.csv')
except FileNotFoundError:
    st.error("The file 'rentfaster_cleaned.csv' was not found. Please ensure it exists in the same directory as this script.")
    st.stop()

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Page title and separator
st.markdown("<h2 style='text-align: center;'>Canadian Rental Price Analysis</h2>", unsafe_allow_html=True)
st.markdown('---')

# Dictionary mapping graph names to their respective functions
graph_functions = {
    'Price per Province': price_per_province,
    'Map': mapped_price,
    'Price per Rental Type': price_per_housetype,
    'Price per Square Foot': price_per_sqft,
    'Lease Term Analysis': lease_term_analysis,
    'Outlier Analysis': outlier_analysis,
    'Rental Price Distribution Analysis': rental_price_distribution_analysis,
    'Pie Chart Analysis: House': pie_chart_analysis_house_type,
    'Pie Chart Analysis: Province': pie_chart_analysis_province,
    'Scatter Plot Analysis': scatter_plot_analysis
}

# Sidebar navigation
st.sidebar.title('Navigation')
st.sidebar.write('Select a page to view.')
st.sidebar.write('---')

def page_home():
    """Display the home page with a welcome message."""
    st.markdown("<h1 style='text-align: center;'>Welcome!</h1>", unsafe_allow_html=True)
    st.write(' ')
    st.markdown("<h5 style='text-align: center;'>This app provides insights into rental prices across Canada based on various features.</h5>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Use the sidebar on the left to get started.</h5>", unsafe_allow_html=True)

def main():
    """Display analysis graphs based on sidebar toggles."""
    for graph_name, graph_func in graph_functions.items():
        if st.sidebar.toggle(graph_name):
            st.subheader(graph_name)
            graph_func(df)

def page_summary():
    """Display a summary of the analysis and personal insights."""
    st.markdown("<h1 style='text-align: center;'>Summary of Analysis</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, border=True)
    with col1:
        # Key findings from the analysis
        st.subheader("Key Findings:")
        st.write("The following key findings were made during the analysis:")
        st.write("- The average rental price in Canada is ${:,.2f}.".format(df['price'].mean()))
        st.write("- The province with the highest average rental price is {}.".format(df.groupby('province')['price'].mean().idxmax()))
        st.write("- The most expensive house type per square foot is {}.".format(df.groupby('type')['sq_feet'].mean().idxmax()))
        st.write("- Short-term leases tend to have higher average prices than long-term leases.")
        st.write("- Outlier analysis reveals a small number of extremely high-priced rentals.")
        st.write("- Rental price distribution is right-skewed, indicating most rentals are below the mean price.")
        st.write("- The majority of listings are for apartments and condos.")
        st.write("- The most common house type is {}.".format(df['type'].mode()[0]))
        st.write("- There is a positive correlation between square footage and rental price, but with significant variance.")
    with col2:
        # Personal insights and data limitations
        st.subheader('Personal Insights:')
        st.write('After working on this project these are my key takeaways:')
        st.write('- Due to the limited data, the analysis may not be fully representative of the true Canadian rental market. Furthermore, since the data has no date, it is difficult to determine if the data is current or not.')
        st.write('- Overall the data appears to provide a somewhat accurate representation of the rental market in Canada in select provinces.')
        st.write('- The first issue with the data that I noticed is that the data is limited to mainly Alberta and Ontario (as seen in the pie chart). This means that the analysis may not be fully representative of the true Canadian rental market.')
        st.write('- The next issue with the data is the distribution of house types. The data is limited to the house types of apartments, condos, and houses (again as seen in the pie chart).')
        st.write('- The last issue with the data is that there are a number of outliers in the data that dont appear to be representative of the true rental market. We can see these issues arise when looking at the higest average rental price (as seen in the key findings). Moreover this is evident in the outlier analysis and the rental price distribution analysis.')

def contact():
    """Display contact information."""
    st.title("Contact Me")
    st.write("If you have any questions or feedback, please reach out to me at:")
    st.write('---')
    st.write("Github: [Link](https://github.com/Shhhua1)")
    st.write("LinkedIn: [Link](https://www.linkedin.com/in/josh-d-158587101/)")

def page_raw_data():
    """Display the raw data and its overview."""
    st.title("Raw Data")
    st.write("Here is the raw data used for the analysis:")
    st.dataframe(df)

    st.subheader("Data Overview:")
    st.write("The dataset contains {} rows and {} columns.".format(df.shape[0], df.shape[1]))
    st.write("The dataset includes the following columns:")
    st.write(df.columns.tolist())
    st.write("The dataset contains the following unique values:")
    for column in df.columns:
        st.write("- {}: {} unique values".format(column, df[column].nunique()))
    st.write("The dataset contains the following data types:")
    st.write(df.dtypes)
    st.write("The dataset contains the following descriptive statistics:")
    st.write(df.describe())

# Sidebar page selection
page = st.sidebar.selectbox("Choose a page", ["Home", "Analysis", "Summary", "Raw Data", "Contact"])

# Render the selected page
if page == "Home":
    page_home()
elif page == "Analysis":
    main()
elif page == "Raw Data":
    page_raw_data()
elif page == "Summary":
    page_summary()
elif page == "Contact":
    contact()