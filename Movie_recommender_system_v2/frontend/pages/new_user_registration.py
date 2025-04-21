import streamlit as st
from pymongo import MongoClient
import requests
import time
import os
API_HOST = os.getenv("API_HOST",'localhost')

def switch_page(page_name: str):
    from streamlit import _RerunData, _RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")
    
    page_name = standardize_name(page_name)

    pages = get_pages("landing_page.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise _RerunException(
                _RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")

st.title("New user registration")
def get_unique_genre_using_set():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['moviedatabase']
    movie_collection = db['movies_database']
    unique_genre= []
    for document in movie_collection.find({}):
        genre_string = document["Genre"]
        genre_list = genre_string.split(",")
        for genre in genre_list:
            unique_genre.append(genre)
    unique_genre = set(unique_genre)
    return unique_genre

username = st.text_input("Username")
password = st.text_input("Password")

#st.subheader("Preferred genre") #Code must be written to limit the check box to 3
genre_list = ['Action', 'Adventure', 'Sci-Fi', 'Mystery', 'Horror', 
              'Thriller', 'Animation', 'Comedy', 'Family', 'Fantasy', 'Drama', 
              'Music', 'Biography', 'Romance', 'History', 'Crime', 
              'Western', 'War', 'Musical', 'Sport', 'Drame']

selected_genre = st.multiselect("Preferred_genre",genre_list,max_selections=3)
genre_str = ""
for genre in selected_genre:
    if len(genre_str) == 0:
        genre_str = genre
    else:
        genre_str = genre_str + "," +genre
#Search by title and watched movie list so that watched_movie list could be 
#added or something with API can be done to add a default list in pymongo

cancel,register = st.columns(2)
with cancel:
    if st.button("Cancel"):
        st.switch_page("landing_page.py")

with register:
    if st.button("Register"):
        url = f"http://{API_HOST}:8000/add_user"
        data = {"username":username,"password":password,"preferred_genres":genre_str}
        user_name = requests.put(url,json=data)
        st.write(f"{username} has been registered successfully")
        time.sleep(3)
        st.switch_page("landing_page.py")