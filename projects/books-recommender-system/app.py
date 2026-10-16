
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Books Recommender System",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Books Recommender System")

st.write(
    "Explore books, rating activity, and book information "
    "to support the development of a book recommendation system."
)

# Load the prepared dataset
DATA_PATH = "/Users/hariharakrishnan/Downloads/Books-Recommender-System/artifacts/dataset/clean_data/clean_data.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(DATA_PATH)

    st.success("Dataset loaded successfully!")

    # Basic dataset overview
    col1, col2, col3 = st.columns(3)

    col1.metric("Records", f"{len(df):,}")
    col2.metric("Unique books", f"{df['ISBN'].nunique():,}")
    col3.metric("Unique users", f"{df['user_id'].nunique():,}")

    st.subheader("Explore a book")

    # One row per ISBN for book information
    books = df.drop_duplicates(subset="ISBN").copy()
    books["book_label"] = (
        books["title"].fillna("Unknown title").astype(str)
        + " — "
        + books["author"].fillna("Unknown author").astype(str)
    )

    selected_label = st.selectbox(
        "Select a book",
        books["book_label"].sort_values().tolist()
    )

    selected_book = books.loc[
        books["book_label"] == selected_label
    ].iloc[0]

    st.write("**Title:**", selected_book["title"])
    st.write("**Author:**", selected_book["author"])
    st.write("**Publication year:**", selected_book["year"])
    st.write("**Publisher:**", selected_book["publisher"])
    st.write("**ISBN:**", selected_book["ISBN"])
    st.write(
        "**Number of ratings:**",
        selected_book["num_of_rating"]
    )

    st.subheader("Rating distribution")

    rating_counts = df["rating"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    rating_counts.plot(kind="bar", ax=ax)

    ax.set_xlabel("Rating")
    ax.set_ylabel("Number of records")
    ax.set_title("Distribution of Book Ratings")

    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Note: Zero ratings need to be interpreted carefully. "
        "Their meaning should be verified from the source data."
    )

except FileNotFoundError:
    st.error(
        "Could not find clean_data.csv. "
        "Place the prepared dataset in this folder, or update DATA_PATH "
        "to point to its actual location."
    )
