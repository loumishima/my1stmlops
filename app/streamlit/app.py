import streamlit as st
import requests
import os

API_URL = os.environ.get("API_URL")

st.title("Streamlit Frontend")

if st.button("Call API"):
    response = requests.get(API_URL)
    st.write(response.json())
