import streamlit as st
import requests
import os
import pandas as pd
from bson import ObjectId
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

#A method to convert strings from pandas dataframe to ObjectId
def str_to_bson_object_id(input_dict: dict,schema_return_key: str):
    list_updated = []
    for strings in input_dict[schema_return_key]["_id"]:
        print(strings)
        list_updated.append(ObjectId(strings))
    input_dict[schema_return_key]["_id"] = list_updated
    return input_dict

st.title("Home page")
st.subheader("Search for movies")
search_text = st.text_input("type the title here")
if search_text:
        headers = {"Authorization": f"Bearer {os.environ["token"]}"}
        url = f"http://{API_HOST}:8000/search_movies"
        data = {"short_title":search_text}
        dict_movies = requests.post(url,json=data,headers=headers)
        dict_movies = dict_movies.json()
        try:
            pandas_movies = pd.DataFrame(dict_movies["searched_movies"])
            st.dataframe(pandas_movies)
        except:
             st.write(dict_movies['detail'])
#Frontend and integration code for watch_movie
#Frontend and integration code for rate_the_movie
st.divider()
st.subheader("Movie recommendations")
headers = {"Authorization": f"Bearer {os.environ["token"]}"}
data = {"username":os.environ["username"]}
url = f"http://{API_HOST}:8000/get_recommendations"
dict_movies = requests.post(url,headers=headers,json =data)
dict_movies = dict_movies.json()
pandas_movies = pd.DataFrame(dict_movies['recommendations'])
st.dataframe(pandas_movies)

st.divider()
st.subheader("Top Rated Movies")
headers = {"Authorization": f"Bearer {os.environ["token"]}"}
url = f"http://{API_HOST}:8000/get_top_rated_movies"
dict_movies = requests.get(url,headers=headers)
dict_movies = dict_movies.json()
print_result = pd.DataFrame(dict_movies['top_rated_movies'])
st.dataframe(print_result)

st.divider()
if st.button("Do you want to add a movie to the collection?"):
     st.switch_page("pages/new_movie_addition.py")

if st.button("Logout"):
     os.environ["token"] = "logged_out"
     st.switch_page("landing_page.py")