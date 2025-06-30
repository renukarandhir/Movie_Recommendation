import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    try:
        # Make API request to fetch movie data
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=ba656a583244ebe146106dd50543a2b1&language=en-US')
        # Check if the response is valid (status code 200)
        if response.status_code == 200:
            data = response.json()
            if 'poster_path' in data:
                return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            else:
                return None  # No poster found
        else:
            return None  # Invalid response from API
    except Exception as e:
        st.error(f"Error fetching poster for movie ID {movie_id}: {str(e)}")
        return None

# Recommendation function to get similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # Get the index of the selected movie
    distances = similarity[movie_index]  # Get similarity scores for the selected movie
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # Get top 5 similar movies

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        # Access movie_id using bracket notation to avoid AttributeError
        movie_id = movies.iloc[i[0]]['id']  # Corrected line: use bracket notation

        recommended_movies.append(movies.iloc[i[0]]['title'])  # Append the movie title
        poster_url = fetch_poster(movie_id)  # Fetch the poster using the movie_id
        recommended_movies_posters.append(poster_url if poster_url else "https://via.placeholder.com/500")  # Fallback if poster is not available

    return recommended_movies, recommended_movies_posters  # Return both movie names and posters

# Load movie data and similarity matrix from pickle files
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))  # Assuming 'movie_dict.pkl' contains movie data with 'id'
movies = pd.DataFrame(movies_dict)  # Convert the dictionary into a DataFrame

similarity = pickle.load(open('similarity.pkl', 'rb'))  # Load the similarity matrix

# Streamlit app setup
st.title('Movie Recommender System')

# Dropdown to select a movie
selected_movie_name = st.selectbox('Select a movie to get recommendations:', movies['title'].values)

# Display movie recommendations when the 'Recommend' button is clicked
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)  # Get recommended movie names and posters

    # Display the recommended movies in a grid format
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.header(names[0])  # Movie 1 title
        st.image(posters[0])  # Movie 1 poster

    with col2:
        st.header(names[1])  # Movie 2 title
        st.image(posters[1])  # Movie 2 poster

    with col3:
        st.header(names[2])  # Movie 3 title
        st.image(posters[2])  # Movie 3 poster

    with col4:
        st.header(names[3])  # Movie 4 title
        st.image(posters[3])  # Movie 4 poster

    with col5:
        st.header(names[4])  # Movie 5 title
        st.image(posters[4])  # Movie 5 poster



#understand line by line
