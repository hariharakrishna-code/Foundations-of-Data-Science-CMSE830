

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# --------------------------------------------------
# 1. Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Books Recommender System",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# 2. Find and load the dataset
# --------------------------------------------------


APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "data" / "clean_data.csv"


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


if not DATA_PATH.is_file():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

try:
    df = load_data(str(DATA_PATH))
except Exception as error:
    st.error(f"The dataset could not be loaded: {error}")
    st.stop()



# --------------------------------------------------
# 3. Application title and purpose
# --------------------------------------------------

st.title("📚 Books Recommender System")

st.markdown(
    """
    **Discover books and explore reading activity through data.**

    This interactive application helps readers explore book information
    and helps users understand patterns in book-rating activity.

    **Main question:** What can the available book and rating data tell
    us about book popularity and the challenges of building a
    recommendation system?
    """
)

st.info(
    "This is an exploratory prototype. It currently supports book "
    "discovery and data analysis; personalized recommendations have "
    "not yet been implemented."
)


if DATA_PATH is None:
    st.error(
        "The dataset could not be found. Place clean_data.csv in the "
        "'data' folder beside app.py, or update DATA_CANDIDATES in "
        "the code to match your dataset location."
    )

    st.code(
        "CMSE830_Streamlit/\n"
        "├── app.py\n"
        "├── requirements.txt\n"
        "└── data/\n"
        "    └── clean_data.csv"
    )

    st.stop()


try:
    df = load_data(str(DATA_PATH))
except Exception as error:
    st.error(f"The dataset could not be loaded: {error}")
    st.stop()


required_columns = [
    "user_id", "ISBN", "rating", "title", "author",
    "year", "publisher", "num_of_rating"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The dataset is missing required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# One row per ISBN for book-level exploration
books = df.drop_duplicates(subset="ISBN").copy()

books["title"] = books["title"].fillna("Unknown title").astype(str)
books["author"] = books["author"].fillna("Unknown author").astype(str)
books["ISBN"] = books["ISBN"].astype(str)

books["book_label"] = (
    books["title"]
    + " — "
    + books["author"]
    + " (ISBN: "
    + books["ISBN"]
    + ")"
)


# --------------------------------------------------
# 4. Navigation
# --------------------------------------------------

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Explore Books",
        "Data Insights",
        "Data Quality & Limitations"
    ]
)


# --------------------------------------------------
# 5. Home
# --------------------------------------------------

if page == "Home":

    st.header("Project Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Records", f"{len(df):,}")
    col2.metric("Unique ISBNs", f"{df['ISBN'].nunique():,}")
    col3.metric("Unique users", f"{df['user_id'].nunique():,}")

    st.subheader("What can you explore?")

    st.markdown(
        """
        - **Explore Books:** Search for a book and inspect its
          publication information.
        - **Data Insights:** Examine rating activity, rating counts,
          and books with the highest rating counts.
        - **Data Quality & Limitations:** Review data-quality checks
          and understand what the analysis cannot yet establish.
        """
    )

    st.subheader("About the dataset")

    st.write(
        "Each record represents a user-book rating record in the "
        "prepared dataset. ISBN identifies the book publication record "
        "used for the book-level summaries."
    )

    st.caption(
        "The dataset contains user identifiers, ISBNs, ratings, book "
        "metadata, and the number of ratings associated with each ISBN."
    )


# --------------------------------------------------
# 6. Explore Books
# --------------------------------------------------

elif page == "Explore Books":

    st.header("🔎 Explore Books")

    st.write(
        "Search for a title or author, then select a book publication "
        "record to view its details."
    )

    search_text = st.text_input(
        "Search by title or author",
        placeholder="For example, 1984 or George Orwell"
    )

    filtered_books = books.copy()

    if search_text.strip():
        search = search_text.strip().casefold()

        filtered_books = filtered_books[
            filtered_books["title"].str.casefold().str.contains(
                search, regex=False
            )
            | filtered_books["author"].str.casefold().str.contains(
                search, regex=False
            )
        ]

    if filtered_books.empty:
        st.warning("No matching books were found. Try another search.")

    else:
        options = filtered_books["book_label"].sort_values().tolist()

        selected_label = st.selectbox(
            "Select a book",
            options
        )

        selected_book = filtered_books.loc[
            filtered_books["book_label"] == selected_label
        ].iloc[0]

        st.subheader(selected_book["title"])

        left, right = st.columns(2)

        with left:
            st.write("**Author:**", selected_book["author"])
            st.write("**ISBN:**", selected_book["ISBN"])
            st.write("**Publisher:**", selected_book["publisher"])

        with right:
            year = selected_book["year"]

            if pd.isna(year) or year == 0:
                st.write("**Publication year:** Unknown or unavailable")
            else:
                st.write("**Publication year:**", int(year))

            st.write(
                "**Number of ratings:**",
                f"{selected_book['num_of_rating']:,}"
            )

            st.caption(
                "Rating count measures rating activity, not book quality."
            )


# --------------------------------------------------
# 7. Data Insights
# --------------------------------------------------

elif page == "Data Insights":

    st.header("📊 Data Insights")

    st.write(
        "These visualizations examine rating activity and the "
        "distribution of ratings across the dataset."
    )

    # Rating distribution
    st.subheader("1. How are rating values distributed?")

    rating_counts = df["rating"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(9, 4))
    rating_counts.plot(kind="bar", ax=ax)

    ax.set_title("Distribution of Rating Values")
    ax.set_xlabel("Rating value")
    ax.set_ylabel("Number of records")
    ax.tick_params(axis="x", rotation=0)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "The rating column contains values from 0 to 10. "
        "The meaning of zero ratings has not been verified."
    )

    # Zero versus nonzero
    st.subheader("2. How common are zero ratings?")

    zero_count = int((df["rating"] == 0).sum())
    nonzero_count = int((df["rating"] != 0).sum())
    total_count = len(df)

    col1, col2 = st.columns(2)

    col1.metric(
        "Zero ratings",
        f"{zero_count:,}",
        f"{zero_count / total_count:.2%} of records"
    )

    col2.metric(
        "Nonzero ratings",
        f"{nonzero_count:,}",
        f"{nonzero_count / total_count:.2%} of records"
    )

    comparison = pd.Series({
        "Zero rating": zero_count,
        "Nonzero rating": nonzero_count
    })

    fig, ax = plt.subplots(figsize=(7, 4))
    comparison.plot(kind="bar", ax=ax)

    ax.set_title("Most Records Have a Rating of Zero")
    ax.set_xlabel("Rating group")
    ax.set_ylabel("Number of records")
    ax.tick_params(axis="x", rotation=0)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.warning(
        "Zero is a recorded value in this dataset, but its meaning "
        "has not been confirmed. Do not assume it means a missing "
        "rating or a negative opinion."
    )

    # Rating counts per ISBN
    st.subheader("3. How does rating activity vary across books?")

    book_counts = (
        books["num_of_rating"]
        .dropna()
    )

    if not book_counts.empty:
        col1, col2, col3 = st.columns(3)

        col1.metric("Median rating count", f"{book_counts.median():.0f}")
        col2.metric("Mean rating count", f"{book_counts.mean():.2f}")
        col3.metric("Maximum rating count", f"{book_counts.max():.0f}")

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.hist(book_counts, bins=25, edgecolor="black")
        ax.set_title("Rating Counts Are Uneven Across ISBNs")
        ax.set_xlabel("Number of ratings per ISBN")
        ax.set_ylabel("Number of ISBNs")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "A right-skewed distribution indicates that some ISBNs "
            "have considerably more rating activity than others."
        )

    # Top 10 ISBNs
    st.subheader("4. Which ISBNs have the highest rating counts?")

    top_books = books.nlargest(10, "num_of_rating").copy()

    top_books["label"] = (
        top_books["title"]
        + " (ISBN: "
        + top_books["ISBN"]
        + ")"
    )

    top_books = top_books.sort_values(
        "num_of_rating",
        ascending=True
    )

    fig, ax = plt.subplots(figsize=(11, 7))

    ax.barh(
        top_books["label"],
        top_books["num_of_rating"]
    )

    ax.set_title("Top 10 ISBNs by Number of Ratings")
    ax.set_xlabel("Number of ratings")
    ax.set_ylabel("Book title and ISBN")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "The chart compares ISBN-level rating counts. Multiple ISBNs "
        "may share the same title, and higher rating counts do not "
        "necessarily mean higher reader satisfaction."
    )


# --------------------------------------------------
# 8. Data Quality and Limitations
# --------------------------------------------------

elif page == "Data Quality & Limitations":

    st.header("🧹 Data Quality & Limitations")

    st.write(
        "These checks describe the prepared dataset. They do not "
        "prove that every value is semantically correct."
    )

    quality_checks = pd.DataFrame({
        "Check": [
            "Missing values",
            "Exact duplicate rows",
            "Repeated user-book pairs",
            "Records with rating zero",
            "Records with publication year zero",
            "Unique ISBNs with publication year zero"
        ],
        "Result": [
            int(df.isnull().sum().sum()),
            int(df.duplicated().sum()),
            int(df.duplicated(subset=["user_id", "ISBN"]).sum()),
            int((df["rating"] == 0).sum()),
            int((df["year"] == 0).sum()),
            int(df.loc[df["year"] == 0, "ISBN"].nunique())
        ]
    })

    st.dataframe(quality_checks, hide_index=True, use_container_width=True)

    title_isbn_counts = (
        df.groupby("title")["ISBN"]
        .nunique()
    )

    multi_isbn_titles = int((title_isbn_counts > 1).sum())

    st.metric(
        "Titles associated with multiple ISBNs",
        f"{multi_isbn_titles:,}"
    )

    st.subheader("Interpretation")

    st.markdown(
        """
        - **Missing values:** The prepared dataset has no explicit
          missing values according to `isnull()`. This does not
          guarantee that all values are meaningful.
        - **Zero ratings:** Their meaning must be verified from the
          original data source before changing or removing them.
        - **Publication year zero:** These records need investigation.
          Zero may indicate an unavailable year, but that has not
          been confirmed.
        - **Multiple ISBNs per title:** Different ISBNs may represent
          different editions or publication formats. They should not
          automatically be treated as separate book titles.
        - **Rating counts:** A large number of ratings measures
          activity, not necessarily quality or satisfaction.
        """
    )

    st.subheader("Current project limitations")

    st.markdown(
        """
        1. Personalized recommendations have not yet been implemented.
        2. The meaning of zero ratings has not been verified.
        3. Publication year zero has not been fully investigated.
        4. Multiple ISBNs for the same title may create repeated titles
           in book-level results.
        5. No recommendation model has been evaluated yet.
        """
    )

    st.info(
        "These limitations are disclosed so users can distinguish "
        "observed data patterns from conclusions that still require "
        "verification."
    )


# --------------------------------------------------
# 9. Footer
# --------------------------------------------------

st.divider()

st.caption(
    "CMSE 830 Midterm Project | Books Recommender System | "
    "Exploratory analysis and book discovery prototype"
)
