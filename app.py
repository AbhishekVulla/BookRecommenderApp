import streamlit as st
import pandas as pd

# Load CSV (Make sure the filename matches exactly!)
books = pd.read_csv('Books.csv')

st.title("📚 Book Recommender for Al Khor Community Library")

# Filters
genres = st.multiselect("Choose genres:", options=books['Genre(s)'].unique())
age = st.selectbox("Select your age group:", options=books['Age Group'].unique())

# Filtering
if genres and age:
    filtered_books = books[
        books['Genre(s)'].str.contains('|'.join(genres), case=False) &
        (books['Age Group'] == age)
    ]
    filtered_books = filtered_books.sort_values(by='Popularity Score', ascending=False)

    st.subheader("📖 Your Book Recommendations:")
    for _, book in filtered_books.iterrows():
        st.markdown(f"**{book['Book Title']}** by *{book['Author']}*  \n_{book['Short Description']}_")
else:
    st.info("Please select at least one genre and an age group.")
