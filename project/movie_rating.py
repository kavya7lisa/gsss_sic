import pandas as pd

# ------------------ Step 1 – Load Data ------------------

# Load CSVs (ensure they are in the same folder as this script)
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
users = pd.read_csv("users.csv")

# Inspect data
print("Movies:\n", movies.head())
print("\nRatings:\n", ratings.head())
print("\nUsers:\n", users.head())

# ------------------ Step 2 – Data Cleaning ------------------

# Check for missing values
print("\nMissing values:\n")
print("Movies:\n", movies.isnull().sum())
print("Ratings:\n", ratings.isnull().sum())
print("Users:\n", users.isnull().sum())

# Fill missing ratings with NaN or 0 (here we use NaN)
ratings['Rating'] = ratings['Rating'].astype(float)

# Remove duplicates
movies.drop_duplicates(inplace=True)
ratings.drop_duplicates(inplace=True)
users.drop_duplicates(inplace=True)

# ------------------ Step 3 – Merge Datasets ------------------

# Merge ratings with movies on MovieID
merged = pd.merge(ratings, movies, on="MovieID", how="left")

# Merge with users on UserID
merged = pd.merge(merged, users, on="UserID", how="left")

print("\nMerged Data:\n", merged.head())

# ------------------ Step 4 – Pivot Table Analysis ------------------

# Average rating per movie
movie_avg_rating = merged.pivot_table(index="Title", values="Rating", aggfunc="mean")
print("\nAverage Rating per Movie:\n", movie_avg_rating)

# Average rating per genre
genre_avg_rating = merged.pivot_table(index="Genre", values="Rating", aggfunc="mean")
print("\nAverage Rating per Genre:\n", genre_avg_rating)

# Average rating per user
user_avg_rating = merged.pivot_table(index="UserID", values="Rating", aggfunc="mean")
print("\nAverage Rating per User:\n", user_avg_rating)

# Count of ratings per movie
movie_rating_count = merged.pivot_table(index="Title", values="Rating", aggfunc="count").rename(columns={"Rating": "RatingCount"})
print("\nRating Count per Movie:\n", movie_rating_count)

# ------------------ Step 5 – Filtering & Sorting ------------------

# Movies with average rating >= 4.0
highly_rated_movies = movie_avg_rating[movie_avg_rating["Rating"] >= 4.0]
print("\nMovies with Average Rating >= 4.0:\n", highly_rated_movies)

# Users who rated more than 5 movies
user_rating_counts = merged.groupby("UserID").size()
active_users = user_rating_counts[user_rating_counts > 5]
print("\nUsers who rated more than 5 movies:\n", active_users)

# Top 5 most rated movies
top5_most_rated = movie_rating_count.sort_values(by="RatingCount", ascending=False).head(5)
print("\nTop 5 Most Rated Movies:\n", top5_most_rated)

# Movies with highest and lowest average ratings
highest_rated = movie_avg_rating.sort_values(by="Rating", ascending=False).head(1)
lowest_rated = movie_avg_rating.sort_values(by="Rating", ascending=True).head(1)
print("\nHighest Rated Movie:\n", highest_rated)
print("\nLowest Rated Movie:\n", lowest_rated)

# ------------------ Step 6 – Derived Columns ------------------

# Add RatingCategory
def categorize_rating(r):
    if r >= 4:
        return "High"
    elif 3 <= r < 4:
        return "Medium"
    else:
        return "Low"

merged["RatingCategory"] = merged["Rating"].apply(categorize_rating)

# Add IsPopular column (more than 10 ratings)
movie_rating_counts = merged.groupby("Title")["Rating"].count().reset_index(name="RatingCount")
merged = pd.merge(merged, movie_rating_counts, on="Title", how="left")
merged["IsPopular"] = merged["RatingCount"].apply(lambda x: "Yes" if x > 10 else "No")

print("\nData with Derived Columns:\n", merged.head())

# ------------------ Step 7 – Export Results ------------------

# Export pivot tables
movie_avg_rating.to_csv("movie_avg_ratings.csv")
genre_avg_rating.to_csv("genre_avg_ratings.csv")
user_avg_rating.to_csv("user_avg_ratings.csv")

# Export cleaned & merged dataset
merged.to_csv("cleaned_movie_ratings.csv", index=False)

print("\n✅ All processing complete. Files exported.")

