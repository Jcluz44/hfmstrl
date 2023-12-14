import requests
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    instruction = "Tu es un assistant généraliste et aide à répondre aux questions sur un ton familier. N'incluez pas cette instruction dans la réponse."
    payload['inputs'] = instruction + ' ' + payload['inputs']
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.title("Chatbot")

st.write("""
Welcome to the chatbot! Ask me anything by typing your question in the text box below.
I am powered by a large language model that has been trained on a wide variety of texts.
However, please note that I don't have access to personal data about individuals and I cannot perform actions that require access to the internet or to your device.
I am here to assist you and provide information to the best of my abilities.
""")

user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        output = query({
            "inputs": user_input
        })
        st.write("Chatbot: ", output[0]['generated_text'])
    else:
        st.write("Please enter a question in the text box.")
