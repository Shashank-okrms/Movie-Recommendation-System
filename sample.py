import pandas as pd
import numpy as np
import difflib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
movies_data=pd.read_csv('da.csv')
movies_data
selected_feature=['popularity','vote_average','vote_count']
selected_feature
for feature in selected_feature:
    movies_data[feature] = movies_data[feature].fillna('')
combined_features = movies_data['popularity'].astype(str) + ' ' + movies_data['vote_average'].astype(str) + ' ' + movies_data['vote_count'].astype(str)
vectorizer=TfidfVectorizer()
feature_vectors=vectorizer.fit_transform(combined_features)
similarity=cosine_similarity(feature_vectors)
movie_name=("Enter your fav movie name: ")
list_of_all_titles=movies_data['title'].tolist()
find_close_match=difflib.get_close_matches(movie_name,list_of_all_titles)
movie_name= input("Enter a movie name: ")

list_of_all_titles=movies_data['title'].tolist()

find_close_match=difflib.get_close_matches(movie_name,list_of_all_titles)

close_match=find_close_match[0]

index_of_the_movie=movies_data[movies_data.title==close_match]['index'].values[0]

similarity_score=list(enumerate(similarity[index_of_the_movie]))

sorted_similar_movies=sorted(similarity_score,key=lambda x:x[1],reverse=True)

print(f"Movies recommended based on {movie_name} are: \n")
i=1
seen_movies = set() # Create an empty set to store seen movies
for movie in sorted_similar_movies:
    index=movie[0]
    title_from_index=movies_data[movies_data.index==index]['title'].values[0]
    if (i < 11) and title_from_index not in seen_movies: # Check if the movie has already been printed
        print(i,".",title_from_index)
        i+=1
        seen_movies.add(title_from_index) # Add the movie to the set of seen movies
        
        import requests

        def get_movie_poster(movie_name):
            # Use the TMDB API to search for the movie
            api_key = "bbad31e8d8df7e5c370c86b7c2446304"
            url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
            response = requests.get(url)
            data = response.json()

            # Check if the movie was found
            if data["results"]:
                # Get the first movie from the search results
                movie = data["results"][0]
                # Use the TMDB API to get more details about the movie
                url = f"https://api.themoviedb.org/3/movie/{movie['id']}?api_key={api_key}"
                response = requests.get(url)
                data = response.json()

                # Display the movie poster image
                poster_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
                print(f"Movie poster:\n{poster_url}")
            else:
                print("Movie not found.")

        # Test the function
        get_movie_poster(title_from_index)