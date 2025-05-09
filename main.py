import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


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
        key='new_house_type_selection'
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
    
    option_province = st.selectbox(
        'Select Province',
        sorted(df['province'].unique()),
        key='province_selection'
        )
    
    if option_province:
        filtered_df = df[(df['province'] == option_province)]
       
        filtered_df['per_sqft'] = filtered_df['price'] / filtered_df['sq_feet']
        avg_sqft_per_province = filtered_df.groupby('type')['per_sqft'].mean().reset_index()
        
        st.write(f"Average rental price per square foot for {option_province}")
        st.bar_chart(avg_sqft_per_province.set_index('type')['per_sqft'], use_container_width=True)
        
    
#price_per_sqft(df) 

# Seperate page

def lease_term_analysis(df):
    # Bar chart of average price by lease term // Do prices differ based on lease term (e.g., monthly vs yearly)?
    pass

def price_outlier_analysis(df):
    # Boxplot of rental prices to identify outliers // using IQR or z-score to flag extreme prices.
    pass

def rental_price_distribution_analysis(df):
    # Distribution of rental prices per provience using a histogram 
    option_province = st.selectbox(
        'Select Province',
        sorted(df['province'].unique()),
        key = 'new_province_selection'
        )
    
    if option_province:
        histogram_data = df[df['province'] == option_province]['price']

        if not histogram_data.empty:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x = histogram_data,
                nbinsx = 30,
                name = 'Rental Price Distribution',
                marker_color = 'light blue',
                opacity = 0.75
            ))
            
            fig.update_layout(title_text = f'Listing Frequency by Price in {option_province}',
                            xaxis_title = 'Rental Price',
                            yaxis_title = 'Number of Listings',
                            bargap = 0.05,
                            height = 600)
                   
            st.plotly_chart(fig) 
            
        else:
            st.warning('No data available for {option_province}. Please select a different province.')
        
#rental_price_distribution_analysis(df)
    
    

def pie_chart_analysis(df):
    # Pie chart to show the distribution of different house types in the dataset.
    st.subheader('House Type Distribution')
    house_type_counts = df['type'].value_counts()
    
    fig = px.pie(house_type_counts,
                 values = house_type_counts.values,
                 names = house_type_counts.index,
                 color_discrete_sequence = px.colors.sequential.Viridis)
    
    fig.update_traces(hovertemplate='%{label}: %{percent:.2%}', texttemplate='%{percent:.2%}')
    
    st.plotly_chart(fig)

#pie_chart_analysis(df)
  

def scatter_plot_analysis(df):
    # Scatter plot to show the relationship between rental prices and the number of bedrooms.
    
    st.subheader('Size vs Price')
    st.write('Scatter Plot of Rental Prices vs Number of Bedrooms including number of bedrooms')
    
    chart_data = df[['price', 'sq_feet']]
    chart_data = chart_data[chart_data['sq_feet'] > 50]  # Filter out rows with zero square feet
    
    
    fig = px.scatter(chart_data, 
                     x = 'sq_feet', 
                     y = 'price', 
                     trendline = 'ols',
                     height = 600,
                     labels = {'sq_feet': 'Square Feet', 'price': 'Rental Price'},
                     color_discrete_sequence = ['blue'])
    
    fig.data[1].update(name = 'Trendline', line_color = 'red')
    
    fig.update_layout(
        xaxis = dict(range = [0, chart_data['sq_feet'].max() * 1.1]),
        yaxis = dict(range = [0, chart_data['price'].max() * 1.1])
    )
    
 
    st.plotly_chart(fig)
    



    
#scatter_plot_analysis(df)  