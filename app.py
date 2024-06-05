from io import BytesIO
from flask import Flask, render_template, request, jsonify
import pandas as pd
import difflib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import requests

app = Flask(__name__)

def load_initial_movie_data():
    return movies_data.head(100).to_dict(orient='records')

# app.py

def get_movie_poster(movie_name):
    try:
        api_key = "2cffaad2423995f5f40143734a7e4c7e"
        search_url = f"https://api.themoviedb.org/3/search/movie"
        params = {'api_key': api_key, 'query': movie_name}
        response = requests.get(search_url, params=params)
        data = response.json()

        if data["results"]:
            movie = data["results"][0]
            poster_path = movie['poster_path']
            poster_url = f"https://image.tmdb.org/t/p/w185{poster_path}"

            # Download the image content
            response = requests.get(poster_url)
            return response.content
        else:
            print(f"No results found for {movie_name}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error in get_movie_poster: {e}")
        return None

def recommend_movies(movie_name):
    list_of_all_titles = movies_data['title'].tolist()
    close_match = difflib.get_close_matches(movie_name, list_of_all_titles, n=1)

    if not close_match:
        return []

    index_of_the_movie = movies_data[movies_data.title == close_match[0]]['index'].values[0]

    similarity_score = list(enumerate(similarity[index_of_the_movie]))

    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended_movies = []

    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies_data.at[index, 'title']

        if title_from_index not in recommended_movies:
            poster_url = get_movie_poster(title_from_index)
            if poster_url:
                recommended_movies.append({'title': title_from_index, 'poster_url': poster_url})

            if len(recommended_movies) == 10:
                break

    return recommended_movies

@app.route('/')
def index():
    initial_movie_data = load_initial_movie_data()
    return render_template('index.html', movie_data=initial_movie_data)

@app.route('/load_more', methods=['POST'])
def load_more():
    current_count = int(request.form['current_count'])
    max_count = 100
    additional_movies = []

    for i in range(current_count, current_count + 25):
        if i >= max_count:
            break

        movie = movies_data.iloc[i]
        title = movie['title']
        poster_url = get_movie_poster(title)

        if poster_url:
            additional_movies.append({'title': title, 'poster_url': poster_url})

    return jsonify({'movies': additional_movies, 'current_count': current_count + 25, 'max_count': max_count})

@app.route('/recommendations', methods=['POST'])
def recommendations():
    movie_name = request.form['movie_name']
    recommended_movies = recommend_movies(movie_name)
    return render_template('recommendations.html', movies=recommended_movies)

from flask import send_file

@app.route('/get_image/<movie_name>')
def get_image(movie_name):
    poster_content = get_movie_poster(movie_name)
    if poster_content:
        return send_file(BytesIO(poster_content), mimetype='image/jpeg')
    else:
        # Return a placeholder image or handle the error as needed
        return send_file('path/to/placeholder-image.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    movies_data = pd.read_csv('da.csv')
    vectorizer = TfidfVectorizer()
    combined_features = movies_data['popularity'].astype(str) + ' ' + movies_data['vote_average'].astype(str) + ' ' + movies_data['vote_count'].astype(str)
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)
    app.run(debug=True)