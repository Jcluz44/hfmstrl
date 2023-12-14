import requests
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.title("Chatbot")

user_input = st.text_input("You: ", "Can you please let us know more details about your")

if st.button("Send"):
    output = query({
        "inputs": user_input
    })
    st.write("Chatbot: ", output[0]['generated_text'])
