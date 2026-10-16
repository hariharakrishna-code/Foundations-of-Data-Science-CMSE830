# Books Recommender System

## 1. Project Overview

This project explores book ratings and book metadata through an interactive Streamlit application. The long-term goal is to build a book recommendation system that helps users discover books.

**Current status:** Initial data exploration and book-browsing prototype. Personalized recommendations have not yet been implemented.

## 2. Dataset

The prepared dataset contains 59,850 records, 9 columns, 888 unique users, and 2,144 unique ISBNs.

The dataset columns include:

- `user_id`: User identifier
- `ISBN`: Book identifier
- `rating`: Recorded rating value
- `title`: Book title
- `author`: Book author
- `year`: Publication year
- `publisher`: Publisher
- `image_url`: Book image URL
- `num_of_rating`: Number of ratings associated with the book

Many rating values are zero. Their meaning must be verified before interpreting them as explicit user ratings.

## 3. Current Application Features

- Display basic dataset metrics
- Select a book from a dropdown menu
- Explore book metadata
- View a book-rating distribution chart

The current application is a book exploration prototype, not yet a personalized recommendation engine.

## 4. Technologies

- Python
- Pandas
- Streamlit
- Matplotlib
- Jupyter Notebook

## 5. Dataset Access

The dataset is not included in this repository yet. Verify its source, license, and size before sharing it. The application requires the prepared `clean_data.csv` file to be available locally.

## 6. Setup and Run

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

These instructions require the application file, dependencies file, and dataset path to be configured correctly.

## 7. Data Quality and Limitations

- Zero-valued ratings account for approximately 75.03% of the prepared records; their meaning requires further investigation.
- Some publication-year values are zero and need verification.
- Personalized recommendations have not yet been implemented.
- Dataset source and licensing need to be verified.

## 8. Planned Improvements

1. Investigate zero-valued ratings and publication years.
2. Implement a simple recommendation method.
3. Improve visualizations and interactive filtering.
4. Document the dataset source and setup process.
5. Test the application in a clean environment.

## 9. AI Assistance

AI tools were used to explain Python concepts, debug code, and assist with setting up the Streamlit application. The project author should review the code and validate the results.
