from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# ---------- Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MOVIES_FILE = os.path.join(DATA_DIR, "movies.csv")
RATINGS_FILE = os.path.join(DATA_DIR, "ratings.csv")
USERS_FILE = os.path.join(DATA_DIR, "users.csv")

def load_dfs():
    """Read fresh copies each request so pages reflect new submissions immediately."""
    movies_df = pd.read_csv(MOVIES_FILE)
    ratings_df = pd.read_csv(RATINGS_FILE)
    users_df = pd.read_csv(USERS_FILE)

    if "Review" not in ratings_df.columns:
        ratings_df["Review"] = ""
    ratings_df["Rating"] = pd.to_numeric(ratings_df["Rating"], errors="coerce")

    # Ensure Description and PhotoURL exist
    if "Description" not in movies_df.columns:
        movies_df["Description"] = ""
    if "PhotoURL" not in movies_df.columns:
        movies_df["PhotoURL"] = "/static/images/default.jpg"

    return movies_df, ratings_df, users_df

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/movies")
def movies():
    movies_df, ratings_df, users_df = load_dfs()

    if not ratings_df.empty:
        agg = ratings_df.groupby("MovieID")["Rating"].agg(["mean", "count"]).reset_index()
        merged = movies_df.merge(agg, on="MovieID", how="left").rename(
            columns={"mean": "AvgRating", "count": "NumRatings"}
        )
    else:
        merged = movies_df.copy()
        merged["AvgRating"] = None
        merged["NumRatings"] = 0

    return render_template("movies.html", movies=merged.to_dict(orient="records"))

@app.route("/ratings")
def ratings():
    movies_df, ratings_df, users_df = load_dfs()
    merged = ratings_df.merge(movies_df, on="MovieID", how="left").merge(users_df, on="UserID", how="left")
    return render_template(
        "ratings.html",
        movies=movies_df.to_dict(orient="records"),
        users=users_df.to_dict(orient="records"),
        reviews=merged.to_dict(orient="records"),
    )

@app.route("/submit_rating", methods=["POST"])
def submit_rating():
    _, ratings_df, _ = load_dfs()
    user_id = request.form["user"]
    movie_id = request.form["movie"]
    rating = request.form["rating"]
    review = request.form["review"]

    new_entry = {"UserID": user_id, "MovieID": movie_id, "Rating": rating, "Review": review}
    ratings_df = pd.concat([ratings_df, pd.DataFrame([new_entry])], ignore_index=True)
    ratings_df.to_csv(RATINGS_FILE, index=False)

    return redirect(url_for("ratings"))

@app.route("/stats")
def stats():
    movies_df, ratings_df, users_df = load_dfs()

    avg_by_user = ratings_df.groupby("UserID")["Rating"].mean().reset_index()
    avg_by_user = avg_by_user.merge(users_df, on="UserID", how="left")

    avg_by_movie = ratings_df.groupby("MovieID")["Rating"].mean().reset_index()
    avg_by_movie = avg_by_movie.merge(movies_df, on="MovieID", how="left")

    return render_template(
        "stats.html",
        avg_by_user=avg_by_user.to_dict(orient="records"),
        avg_by_movie=avg_by_movie.to_dict(orient="records"),
    )

if __name__ == "__main__":
    app.run(debug=True)
