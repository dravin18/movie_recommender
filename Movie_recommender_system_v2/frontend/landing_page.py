import streamlit as st
import requests
import os
os.environ["token"] = "dummy_token"
os.environ["username"] = "dummy_username"
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

st.title("Akaike Movie Recommender System")
st.markdown('<style>.stMarkdown > div { border: 2px solid #000; }</style>', unsafe_allow_html=True)
existing_user,new_user = st.columns(2)

with existing_user:
    st.text("Existing user ? Login")
    username = st.text_input("Username")
    os.environ["username"] = username
    password = st.text_input("Password")

    if st.button("Login"):
        url = f"http://{API_HOST}:8000/user_login"
        data = {"username":username,"password":password}
        token_data = requests.post(url,data=data)
        token_data = token_data.json()
        os.environ["token"] = token_data["access_token"]
        print(token_data)
        print(type(token_data))
        st.switch_page("pages/home_page.py")

with new_user:
    st.text("New user ?")
    if st.button("Register"):
        st.write("When this button is pressed new user registration page will open")
        st.switch_page("pages/new_user_registration.py")