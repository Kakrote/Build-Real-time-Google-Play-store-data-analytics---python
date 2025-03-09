import pandas as pd
import plotly.express as px
import datetime as dt
import pytz
import streamlit as st

def main():
    # Load data
    apps_df = pd.read_csv('googleplaystore.csv')

    # Clean installs and reviews data
    apps_df = apps_df[apps_df['Installs'].str.contains(r'\d', regex=True, na=False)]
    apps_df['Installs'] = apps_df['Installs'].str.replace(r'[+,]', '', regex=True).astype(int)
    apps_df['Reviews'] = apps_df['Reviews'].astype(int)

    # Filter apps
    filter_apps = apps_df[
        (~apps_df['App'].str.startswith(('x', 'y', 'z'))) &
        (apps_df['Category'].str.startswith(('E', 'C', 'B'))) &
        (apps_df['Reviews'] > 500)
    ].copy()

    # Time series data
    filter_apps['Last Updated'] = pd.to_datetime(filter_apps['Last Updated'], errors='coerce')
    filter_apps['YearMonth'] = filter_apps['Last Updated'].dt.to_period('M').astype(str)
    time_series = filter_apps.groupby(['YearMonth', 'Category']).agg({'Installs': 'sum'}).reset_index()
    time_series = time_series.sort_values(by=['Category', 'YearMonth'])

    # Calculate MoM growth
    time_series['previous'] = time_series.groupby('Category')['Installs'].shift(1)
    time_series['MoM'] = ((time_series['Installs'] - time_series['previous']) / time_series['previous']) * 100
    time_series['Significant'] = time_series['MoM'] > 20

    # Time restriction: 12 PM to 9 PM IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = dt.datetime.now(ist).time()
    start_time = dt.time(12, 0)
    end_time = dt.time(21, 0)

    # Define custom colors
    category_colors = {
        'ENTERTAINMENT': '#FF5733',  # Orange
        'COMMUNICATION': '#4caf50',   # Green
        'BUSINESS': '#6C63FF',        # Purple
    }

    if start_time <= current_time <= end_time:
        # Create the line chart
        fig = px.line(
            time_series,
            x='YearMonth',
            y='Installs',
            color='Category',
            title='📈 Total Installs Over Time by App Category',
            color_discrete_map=category_colors
        )

        # Highlight significant growth periods
        for category in time_series['Category'].unique():
            significant_growth = time_series[(time_series['Category'] == category) & (time_series['Significant'])]
            fig.add_traces(
                px.area(significant_growth, x='YearMonth', y='Installs', color_discrete_sequence=['#FFD700']).data
            )

        # Customize layout
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Installs',
            legend_title='App Category',
            plot_bgcolor='#f0f2f6',
            font=dict(family='Arial, sans-serif', size=12, color='black'),
            hovermode='x unified',
            margin=dict(l=50, r=50, t=80, b=50),
            height=600,
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("The graph is only visible between 12 PM and 9 PM IST.")

if __name__ == '__main__':
    main()
