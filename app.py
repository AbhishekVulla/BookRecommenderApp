import streamlit as st
import pandas as pd
import io

# Load CSV
books = pd.read_csv('Books.csv')

st.title("📚 Book Recommender for Al Khor Community Library")

# Welcome message
st.markdown("""
Welcome to the **Book Recommender for Al Khor Community Library**!  
Use the filters below to find books by genre, age group, or search by title/author.
""")

# Filters
genres = st.multiselect("Choose genres:", options=books['Genre(s)'].unique())
age = st.selectbox("Select your age group:", options=books['Age Group'].unique())
search_query = st.text_input("🔍 Search by book title or author")

# Apply filters
if genres and age:
    filtered_books = books[
        books['Genre(s)'].str.contains('|'.join(genres), case=False) &
        (books['Age Group'] == age)
    ]

    if search_query:
        filtered_books = filtered_books[
            filtered_books['Book Title'].str.contains(search_query, case=False) |
            filtered_books['Author'].str.contains(search_query, case=False)
        ]

    filtered_books = filtered_books.sort_values(by='Popularity Score', ascending=False)

    st.subheader("📖 Your Book Recommendations:")

    for _, book in filtered_books.iterrows():
        # Display cover image or fallback
        if pd.notna(book['Cover Image URL']):
            st.image(book['Cover Image URL'], width=120)
        else:
            st.image("https://via.placeholder.com/120x180.png?text=No+Cover", width=120)

        # Display book details
        st.markdown(f"""
        ### 📘 {book['Book Title']}
        **Author:** {book['Author']}  
        **Genre:** 🏷️ `{book['Genre(s)']}`  
        **Age Group:** {book['Age Group']}  
        **Popularity:** ⭐ {book['Popularity Score']}  
        _{book['Short Description']}_  
        """)

    # Download filtered list
    csv = filtered_books.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download recommendations as CSV", csv, "recommended_books.csv", "text/csv")

else:
    st.info("Please select at least one genre and an age group.")
