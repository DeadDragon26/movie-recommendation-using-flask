import flask
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Load and preprocess the dataset
try:
    df = pd.read_csv('./model/tmdb.csv')
except FileNotFoundError:
    raise Exception("Dataset file 'tmdb.csv' not found in './model/'. Please ensure the file exists.")

# Ensure required columns are present
if 'title' not in df.columns or 'soup' not in df.columns:
    raise Exception("The dataset must contain 'title' and 'soup' columns.")

# Fill missing values in 'soup' column
df['soup'] = df['soup'].fillna('')

# Compute the TF-IDF matrix and cosine similarity
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['soup'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Reset indices and create a reverse lookup for titles
df = df.reset_index()
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

# Recommendation function
def get_recommendations(title, n=10):
    if title not in indices:
        return [], [], []
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n + 1]
    movie_indices = [i[0] for i in sim_scores]

    # Get the movie titles, release dates, and mock homepages
    movie_titles = df['title'].iloc[movie_indices].tolist()
    release_dates = df['release_date'].iloc[movie_indices].fillna('Unknown').tolist() if 'release_date' in df.columns else ['Unknown'] * n
    homepages = ["#"] * n  # Replace "#" with actual homepage links if available in your dataset

    return movie_titles, release_dates, homepages

# Routes
@app.route("/", methods=["GET", "POST"])
def main():
    if flask.request.method == "POST":
        movie_name = flask.request.form.get("movie_name")
        movie_titles, release_dates, homepages = get_recommendations(movie_name)
        return flask.render_template("found.html", search_name=movie_name, movie_names=movie_titles, movie_releaseDate=release_dates, movie_homepage=homepages)
    return flask.render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


