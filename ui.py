import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use localhost instead of 'api' for the host
api_host = "localhost"
api_port = 8080

# Streamlit UI elements
st.title("Email Rag")

question = st.text_input(
    "Search about your mails",
    placeholder="What data are you looking for?"
)

if question:
    url = f'http://{api_host}:{api_port}/'
    data = {"query": question}

    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            st.write("### Answer")
            st.write(response.json())
        else:
            st.error(f"Failed to send data to Pathway API. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error(f"Failed to connect to the API. Make sure the API is running on {api_host}:{api_port}")