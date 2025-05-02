import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Read the data from the CSV file
try:
    df = pd.read_csv('rentfaster_cleaned.csv')
except FileNotFoundError:
    st.error("The file 'rentfaster_cleaned.csv' was not found. Please ensure it exists in the same directory as this script.")
    st.stop()

st.title('Canadian Rental Price Analysis')
st.write("This app analyzes rental prices in Canada based on various features")


st.subheader('Raw Data')
st.write(df)


def price_per_province(df):
    # Plotting average rental price per province based on the number of rooms
    # Using selectbox to filter the data based on the number of rooms
    st.subheader('Average Rental Price per Province')
    option = st.selectbox(
        'Select Number of Rooms', 
        sorted(df['beds'].unique()), 
        key='room_selection'
        )

    if option:
        filtered_df = df[df['beds'] == option]
        avg_price_per_province = filtered_df.groupby('province')['price'].mean().reset_index()
        
        st.write(f"Average rental price for {option} room(s)")
        st.bar_chart(avg_price_per_province.set_index('province')['price'], use_container_width=True)
        
#price_per_province(df)

def mapped_price(df):
    # Mapping rental prices to provinces using a slider for price range + a selectbox for house types + a heatmap
    st.subheader('Mapped Rental Prices')
    selectbox_option = st.selectbox(
        'Select House Type',
        sorted(df['type'].unique()),
        key='house_type_selection'
    )
    
    slider_option = st.slider(
        'Select Price Range',
        min_value=int(df['price'].min()),
        max_value=int(df['price'].max()),
        value=(int(df['price'].min()), int(df['price'].max())),
        key='price_range_selection'
    )
    
    if selectbox_option and slider_option:
        filtered_df = df[(df['type'] == selectbox_option) & (df['price'].between(slider_option[0], slider_option[1]))]
        
        avg_price_per_province = filtered_df.groupby('province')['price'].mean().reset_index()
        st.write(f"Average rental price for {selectbox_option} in the selected price range")
        st.map(filtered_df)
   
#mapped_price(df)
    

def price_per_housetype(df):
    # Price per house type using a selectbox for house types
    pass


def price_per_sqft(df):
    # Price per square foot using a slider for price range
    pass

# Seperate page

def lease_term_analysis(df):
    # Bar chart of average price by lease term // Do prices differ based on lease term (e.g., monthly vs yearly)?
    pass

def price_outlier_analysis(df):
    # Boxplot of rental prices to identify outliers // using IQR or z-score to flag extreme prices.
    pass