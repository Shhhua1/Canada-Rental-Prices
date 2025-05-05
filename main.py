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
    st.subheader('Average Rental Price per Province')
    option = st.selectbox(
        'Select House Type',
        sorted(df['type'].unique()), 
        key='house_type_selection'
        )
    
    if option:
        filtered_df = df[df['type'] == option]
        avg_price_per_province = filtered_df.groupby('province')['price'].mean().reset_index()
        
        st.write(f"Average rental price for {option}")
        st.bar_chart(avg_price_per_province.set_index('province')['price'], use_container_width=True) 
    

#price_per_housetype(df)

def price_per_sqft(df):
    # Price per square foot using a slider for price range
    st.subheader('Price per Square Foot')
    option = st.selectbox(
        'Select House Type',
        sorted(df['type'].unique()), 
        key='house_type_selection'
        )
    
    if option:
        filtered_df = df[df['type'] == option]
        
        filtered_df['per_sqft'] = filtered_df['price'] / filtered_df['sq_feet']
        avg_sqft_per_province = filtered_df.groupby('province')['per_sqft'].mean().reset_index()
        
        st.write(f"Average rental price per square foot for {option}")
        st.bar_chart(avg_sqft_per_province.set_index('province')['per_sqft'], use_container_width=True)
        
    
#price_per_sqft(df) 

# Seperate page

def lease_term_analysis(df):
    # Bar chart of average price by lease term // Do prices differ based on lease term (e.g., monthly vs yearly)?
    pass

def price_outlier_analysis(df):
    # Boxplot of rental prices to identify outliers // using IQR or z-score to flag extreme prices.
    pass

def frequency_distribution_analysis(df):
    # Frequency distribution of rental prices // histogram or density plot.
    pass

def pie_chart_analysis(df):
    # Pie chart to show the distribution of different house types in the dataset.
    st.subheader('House Type Distribution')
    house_type_counts = df['type'].value_counts()
    
    fig, ax = plt.subplots()
    ax.pie(house_type_counts.values, labels=house_type_counts.index, autopct='%1.1f%%', startangle=45)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.pyplot(fig)


#pie_chart_analysis(df)
  

def scatter_plot_analysis(df):
    # Scatter plot to show the relationship between rental prices and the number of bedrooms.
    pass 


# Todo:
# 1. add a frequency distribution of rental prices to see how they are distributed across different ranges.
# --> this could be a histogram or density plot.
# 2. add a pie chart to show the distribution of different house types in the dataset.
# --> this could be a good way to visualize the data and see which types of houses are most common in the rental market.
# 3. add a scatter plot to show the relationship between rental prices and the number of bedrooms.
# --> this could be a good way to visualize the data and see if larger houses tend to have higher rental prices. 