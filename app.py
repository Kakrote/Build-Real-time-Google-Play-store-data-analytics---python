import streamlit as st
import task_1
import task_2
import task_3

# Sidebar for navigation
st.sidebar.title('Google Play Store Data Analysis')
option = st.sidebar.selectbox(
    'Select Task',
    ['Sentiment Distribution', 'Global Installs by Category', 'Installs Trend Over Time']
)

# Display task outputs based on selection
if option == 'Sentiment Distribution':
    st.title('Sentiment Distribution by Rating Groups')
    task_1.main()
elif option == 'Global Installs by Category':
    st.title('Global Installs by Category')
    task_2.main()
elif option == 'Installs Trend Over Time':
    st.title('Installs Trend Over Time')
    task_3.main()
