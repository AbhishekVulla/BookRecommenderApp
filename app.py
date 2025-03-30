import streamlit as st
import pandas as pd
import io

# Load CSV
books = pd.read_csv('Books.csv')

st.title("📚 Book Recommender for Al Khor Community Library")

# Welcome message
st.markdown("""
Welcome to the **Book Recommender for Al Khor Community Library**!  
Use the filters below to find books by genre and age group.
""")

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
        st.image(book['Cover Image URL'], width=120)
        st.markdown(f"""
        ### 📘 {book['Book Title']}
        **Author:** {book['Author']}  
        **Genre:** {book['Genre(s)']}  
        **Age Group:** {book['Age Group']}  
        **Popularity:** ⭐ {book['Popularity Score']}  
        _{book['Short Description']}_  
        """)

    # Optional: Download filtered recommendations
    csv = filtered_books.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download recommendations as CSV", csv, "recommended_books.csv", "text/csv")

else:
    st.info("Please select at least one genre and an age group.")
