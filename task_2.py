import pandas as pd
import plotly.express as px
import datetime
import pytz
import streamlit as st

def main():
    # Load data
    app_df = pd.read_csv('googleplaystore.csv')

    # Clean installs data
    app_df = app_df[app_df['Installs'].str.contains(r'\d', regex=True)]
    app_df['Installs'] = app_df['Installs'].str.replace('[,+]', '', regex=True).astype(int)

    # Filter top 5 categories
    top_5_category = app_df['Category'].value_counts().head().index
    top_5_groups = app_df[app_df['Category'].isin(top_5_category)]

    # Exclude categories starting with A, C, G, S
    exclude_prefix = ('A', 'C', 'G', 'S')
    filter_top_categories = top_5_groups[~top_5_groups['Category'].str.startswith(exclude_prefix)].copy()

    # Highlight categories with installs > 1 million
    filter_top_categories['Highlight'] = filter_top_categories['Installs'] > 1000000

    # Group and summarize data
    category_summary = filter_top_categories.groupby('Category', as_index=False).agg({
        'Installs': 'sum', 
        'Highlight': 'max'
    })
    category_summary['Highlight_Label'] = category_summary['Highlight'].apply(
        lambda x: 'Above 1M Installs' if x else 'Below 1M Installs'
    )

    # Time restriction: 12 PM to 8 PM IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(ist).time()
    start_time = datetime.time(12, 0)
    end_time = datetime.time(20, 0)

    # Colorful visualization
    if start_time <= current_time <= end_time:
        fig = px.bar(
            category_summary,
            x='Category',
            y='Installs',
            color='Highlight_Label',
            title='🚀 App Installs by Category (Highlight: Above 1M)',
            text='Installs',
            color_discrete_map={
                '🔥 Above 1M Installs': '#FF5733',  # Bright orange
                '📊 Below 1M Installs': '#4caf50'   # Vibrant green
            }
        )

        # Update layout for a polished look
        fig.update_traces(
            texttemplate='%{text:,}', 
            textposition='outside'
        )

        fig.update_layout(
            xaxis_title='App Category',
            yaxis_title='Total Installs',
            legend_title='Install Range',
            plot_bgcolor='#f0f2f6',
            font=dict(family="Arial, sans-serif", size=12, color="black"),
            margin=dict(l=50, r=50, t=80, b=50),
            hovermode='x unified',
            height=600,
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("The dashboard is only available between 12 PM and 8 PM IST.")

if __name__ == '__main__':
    main()
