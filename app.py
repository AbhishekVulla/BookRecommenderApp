import streamlit as st
import pandas as pd
import io

# Load book data
books = pd.read_csv('Books.csv')

# Set page config (optional: sets light theme when opening app)
st.set_page_config(page_title="AKC Library Book Recommender", layout="centered")

# 🔝 AKC Library Banner
st.image("https://www.akcommunity.org/Portals/_default/Skins/mes/img/facilities_banner.jpg", use_column_width=True)

# 🏷 Title & Description
st.title("Book Recommender for Al Khor Community Library")
st.markdown("""
Welcome to the Al Khor Community Library’s digital book finder.  
Discover age-appropriate reads by filtering through genres, age groups, or searching by author or title.
""")

# 📌 Sidebar Filters
with st.sidebar:
    st.header("Filter Books")
    genres = st.multiselect("Choose genres:", options=books['Genre(s)'].unique())
    age = st.selectbox("Select your age group:", options=books['Age Group'].unique())
    search_query = st.text_input("Search by book title or author")

# ✅ Filter Logic
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

    st.markdown("---")
    st.subheader("Your Book Recommendations")

    for _, book in filtered_books.iterrows():
        # Show image or fallback
        cover = book['Cover Image URL']
        if pd.notna(cover) and cover.strip() != "":
            st.image(cover, width=120)
        else:
            st.image("https://via.placeholder.com/120x180.png?text=Cover+Not+Available", width=120)

        st.markdown(f"""
        ### {book['Book Title']}
        **Author:** {book['Author']}  
        **Genre:** {book['Genre(s)']}  
        **Age Group:** {book['Age Group']}  
        **Popularity:** {book['Popularity Score']} / 5  
        _{book['Short Description']}_  
        """)

    # 📥 Download button
    csv = filtered_books.to_csv(index=False).encode('utf-8')
    st.download_button("Save My Reading List", csv, "recommended_books.csv", "text/csv")

    # Suggestion note
    st.markdown("Have a favorite book to suggest? Kindly inform the library staff.")

else:
    st.info("Please select at least one genre and an age group from the sidebar to get recommendations.")
