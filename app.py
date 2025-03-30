import streamlit as st
import pandas as pd
import io

# Load CSV
books = pd.read_csv('Books.csv')

# 🖼️ AKC Logo
st.image("https://www.akcommunity.org/Portals/0/akcommunity_logo.png", width=200)

# Title & Intro
st.title("📚 Book Recommender for Al Khor Community Library")
st.markdown("""
Welcome to our community-powered book discovery tool!  
Explore our library collection by selecting genres, age groups, or searching by author/title.  
""")

# 🧠 Sidebar Filters
with st.sidebar:
    st.header("🔍 Filter Books")
    genres = st.multiselect("Choose genres:", options=books['Genre(s)'].unique())
    age = st.selectbox("Select your age group:", options=books['Age Group'].unique())
    search_query = st.text_input("Search by book title or author")

# 🔍 Filtering logic
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

    # 📘 Section Divider
    st.markdown("""---  
    ### 📘 Your Book Recommendations  
    """)

    for _, book in filtered_books.iterrows():
        # Cover image or fallback
        if pd.notna(book['Cover Image URL']):
            st.image(book['Cover Image URL'], width=120)
        else:
            st.image("https://via.placeholder.com/120x180.png?text=No+Cover", width=120)

        # Book Info
        st.markdown(f"""
        ### 📖 {book['Book Title']}
        **Author:** {book['Author']}  
        **Genre:** 🏷️ `{book['Genre(s)']}`  
        **Age Group:** {book['Age Group']}  
        **Popularity:** ⭐ {book['Popularity Score']}  
        _{book['Short Description']}_  
        """)

    # 📥 Download button
    csv = filtered_books.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Save My Reading List", csv, "recommended_books.csv", "text/csv")

    # 💡 Suggestion Note
    st.markdown("💡 Have a favorite book to suggest? Let the librarian or volunteer team know!")

else:
    st.info("Please select at least one genre and an age group from the sidebar.")

# ✍️ Footer
st.markdown("""
---
Made with ❤️ by **Abhishek Vulla**, AKC Youth Volunteer  
Empowering our readers — one book at a time.  
""")
