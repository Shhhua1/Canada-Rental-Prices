import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def price_per_province(df):
    """
    Plot average rental price per province based on the number of rooms.
    Allows filtering by number of rooms using a selectbox.
    """
    st.write('This graph shows the average rental price per province based on the number of rooms')
    option = st.selectbox(
        'Select Number of Rooms',
        sorted(df['beds'].unique()),
        key='room_selection_price_per_province'
    )

    if option:
        # Filter data for selected number of rooms
        filtered_df = df[df['beds'] == option].copy()
        avg_price_per_province = filtered_df.groupby('province')['price'].mean().reset_index()

        # Create bar chart
        fig = px.bar(
            avg_price_per_province,
            x='province',
            y='price',
            color='province'
        )
        fig.update_layout(
            title_text=f'Average Rental Price for {option} Room(s)',
            xaxis_title='Province',
            yaxis_title='Average Price',
            height=600,
            coloraxis_colorbar=dict(title="Province")
        )

        st.plotly_chart(fig)

def mapped_price(df):
    """
    Map rental prices to provinces using a slider for price range and a selectbox for house types.
    Displays a map of filtered listings.
    """
    selectbox_option = st.selectbox(
        'Select Rental Type',
        sorted(df['type'].unique()),
        key='house_type_selection_mapped_price'
    )

    slider_option = st.slider(
        'Select Price Range',
        min_value=int(df['price'].min()),
        max_value=int(df['price'].max()),
        value=(int(df['price'].min()), int(df['price'].max())),
        key='price_range_selection_mapped_price'
    )

    if selectbox_option and slider_option:
        # Filter data by rental type and price range
        filtered_df = df[
            (df['type'] == selectbox_option) &
            (df['price'].between(slider_option[0], slider_option[1]))
        ].copy()

        avg_price_per_province = filtered_df.groupby('province')['price'].mean().reset_index()
        st.write(f"Location of {selectbox_option} rentals across Canada")
        st.map(filtered_df)

def price_per_housetype(df):
    """
    Plot average price per rental type based on the province.
    Allows filtering by rental type using a selectbox.
    """
    st.write('This graph shows the average price per rental type based on the province')

    option = st.selectbox(
        'Select Rental Type',
        sorted(df['type'].unique()),
        key='house_type_selection_price_per_housetype'
    )

    if option:
        # Filter data for selected rental type
        filtered_df = df[df['type'] == option].copy()
        avg_price_per_province = filtered_df.groupby('province')['price'].mean().reset_index()

        # Create bar chart
        fig = px.bar(
            avg_price_per_province,
            x='province',
            y='price',
            color='province'
        )
        fig.update_layout(
            title_text=f'Average Rental Price for {option}',
            xaxis_title='Province',
            yaxis_title='Average Price',
            height=600,
            coloraxis_colorbar=dict(title="Province")
        )

        st.plotly_chart(fig)

def price_per_sqft(df):
    """
    Plot average rental price per square foot by rental type and province.
    Allows filtering by province using a selectbox.
    """
    st.write('This graph shows the average rental price per square foot based on the rental type and province')

    option_province = st.selectbox(
        'Select Province',
        sorted(df['province'].unique()),
        key='province_selection_price_per_sqft'
    )

    if option_province:
        # Filter data for selected province and remove zero sqft
        filtered_df = df[df['province'] == option_province].copy()
        filtered_df = filtered_df[filtered_df['sq_feet'] > 0]

        # Calculate price per square foot
        filtered_df['per_sqft'] = filtered_df['price'] / filtered_df['sq_feet']
        avg_sqft_per_province = filtered_df.groupby('type')['per_sqft'].mean().reset_index()

        # Create bar chart
        fig = px.bar(
            avg_sqft_per_province,
            x='type',
            y='per_sqft',
            color='type'
        )
        fig.update_layout(
            title_text=f'Average Rental Price for {option_province}',
            xaxis_title='House Type',
            yaxis_title='Price per Square Foot',
            height=600,
            coloraxis_colorbar=dict(title="type")
        )

        st.plotly_chart(fig)

def lease_term_analysis(df):
    """
    Bar chart of average price by lease term.
    Allows multi-selection of lease terms.
    """
    st.write('This graph compares rental price based on the lease term.')

    options = sorted(df['lease_term'].unique())
    selection = st.segmented_control(
        " ", options, selection_mode="multi"
    )

    if selection:
        # Filter data for selected lease terms
        filtered_df = df[df['lease_term'].isin(selection)].copy()
        avg_price_per_lease_term = filtered_df.groupby('lease_term')['price'].mean().reset_index()

        # Create bar chart
        fig = px.bar(
            avg_price_per_lease_term,
            x='lease_term',
            y='price',
            color='lease_term'
        )
        fig.update_layout(
            title_text='Average Rental Price by Lease Term',
            xaxis_title='Lease Term',
            yaxis_title='Average Price',
            height=600,
            coloraxis_colorbar=dict(title="Lease Term")
        )

        st.plotly_chart(fig)

def outlier_analysis(df):
    """
    Boxplot of rental prices to identify outliers by province.
    Allows filtering by province using a selectbox.
    """
    st.write('This graph shows the outliers in rental prices based on the province')

    option_province = st.selectbox(
        'Select Province',
        sorted(df['province'].unique()),
        key='province_selection_outlier_analysis'
    )

    if option_province:
        # Filter data for selected province
        filtered_df = df[df['province'] == option_province].copy()

        # Create boxplot
        fig = px.box(
            filtered_df,
            x='price',
            y='province',
            points='outliers'
        )
        fig.update_layout(
            width=1000,
            height=600,
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
        )

        st.plotly_chart(fig)

def rental_price_distribution_analysis(df):
    """
    Histogram of rental price distribution per province.
    Allows filtering by province using a selectbox.
    """
    st.write('This graph shows the distribution of rental prices based on the province')

    option_province = st.selectbox(
        'Select Province',
        sorted(df['province'].unique()),
        key='province_selection_rental_price_distribution_analysis'
    )

    if option_province:
        histogram_data = df[df['province'] == option_province]['price'].copy()

        if not histogram_data.empty:
            # Create histogram
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=histogram_data,
                nbinsx=30,
                name='Rental Price Distribution',
                marker_color='light blue',
                opacity=0.75
            ))

            fig.update_layout(
                title_text=f'Listing Frequency by Price in {option_province}',
                xaxis_title='Rental Price',
                yaxis_title='Number of Listings',
                bargap=0.05,
                height=600
            )

            st.plotly_chart(fig)
        else:
            st.warning(f'No data available for {option_province}. Please select a different province.')

def pie_chart_analysis_house_type(df):
    """
    Pie chart to show the distribution of different house types in the dataset.
    """
    st.write('This graph shows the distribution of different rental types in the dataset.')

    house_type_counts = df['type'].value_counts()

    # Create pie chart
    fig = px.pie(
        house_type_counts,
        values=house_type_counts.values,
        names=house_type_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    fig.update_traces(
        hovertemplate='%{label}: %{percent:.2%}',
        texttemplate='%{percent:.2%}'
    )

    st.plotly_chart(fig)

def scatter_plot_analysis(df):
    """
    Scatter plot to show the relationship between rental prices and total square feet.
    """
    st.write('This graph shows the relationship between rental prices and total square feet.')
    chart_data = df[['price', 'sq_feet', 'type']].copy()
    chart_data = chart_data[chart_data['sq_feet'] > 50]  # Filter out rows with small square feet

    # Create scatter plot with trendline
    fig = px.scatter(
        chart_data,
        x='sq_feet',
        y='price',
        color='type',
        trendline='ols',
        height=800,
        width=1000,
        labels={'sq_feet': 'Square Feet', 'price': 'Rental Price'},
        color_discrete_sequence=['light blue'],
    )

    fig.update_layout(
        xaxis=dict(range=[0, chart_data['sq_feet'].max() * 1.1]),
        yaxis=dict(range=[0, chart_data['price'].max() * 1.1])
    )

    st.plotly_chart(fig)

def pie_chart_analysis_province(df):
    """
    Pie chart to show the distribution of different provinces in the dataset.
    """
    st.write('This graph shows the distribution of different provinces in the dataset.')

    province_counts = df['province'].value_counts()

    # Create pie chart
    fig = px.pie(
        province_counts,
        values=province_counts.values,
        names=province_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    fig.update_traces(
        hovertemplate='%{label}: %{percent:.2%}',
        texttemplate='%{percent:.2%}'
    )

    st.plotly_chart(fig)