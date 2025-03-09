import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def main():
    # Load data
    apps_df = pd.read_csv('googleplaystore.csv')
    review_df = pd.read_csv('googleplaystore_user_reviews.csv')

    # Clean and filter data
    apps_df = apps_df[apps_df['Reviews'].str.contains(r'\d', regex=True)]
    apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'].str.replace(',', ''), errors='coerce')
    apps_df = apps_df[apps_df['Reviews'] > 1000]

    # Merge data
    merge_df = pd.merge(review_df, apps_df, on='App')

    # Group ratings
    def rating_groups(rating):
        if rating >= 4:
            return '4-5 stars'
        elif rating >= 3:
            return '3-4 stars'
        else:
            return '1-2 stars'

    merge_df['Rating Groups'] = merge_df['Rating'].apply(rating_groups)

    # Filter top 5 categories
    top_category = merge_df["Category"].value_counts().head(5).index
    merge_df = merge_df[merge_df["Category"].isin(top_category)]

    # Prepare data for plotting
    sentiment_count = merge_df.groupby(["Category", "Rating Groups", "Sentiment"]).size().unstack(fill_value=0).reset_index()

    # Custom color palette
    color_map = {
        'Positive': '#4caf50',  # Green
        'Neutral': '#ffeb3b',   # Yellow
        'Negative': '#f44336',  # Red
    }

    # Plot
    fig = go.Figure()

    for category in sentiment_count['Category'].unique():
        subset = sentiment_count[sentiment_count['Category'] == category]

        fig.add_trace(go.Bar(
            x=subset['Rating Groups'], 
            y=subset['Positive'], 
            name=f'{category} - Positive',
            marker_color=color_map['Positive']
        ))

        fig.add_trace(go.Bar(
            x=subset['Rating Groups'], 
            y=subset['Neutral'], 
            name=f'{category} - Neutral',
            marker_color=color_map['Neutral']
        ))

        fig.add_trace(go.Bar(
            x=subset['Rating Groups'], 
            y=subset['Negative'], 
            name=f'{category} - Negative',
            marker_color=color_map['Negative']
        ))

    # Layout updates
    fig.update_layout(
        barmode='stack',
        title='Sentiment Distribution by Rating Group (Top 5 Categories)',
        xaxis_title='Rating Groups',
        yaxis_title='Number of Reviews',
        legend_title='Sentiment',
        plot_bgcolor='#f4f4f4',
        font=dict(family="Arial, sans-serif", size=12, color="black"),
        margin=dict(l=50, r=50, t=80, b=50),
        hovermode='x unified',
        width=1000,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
