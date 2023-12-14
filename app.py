import streamlit as st
import random
import time
import requests

# Configuration de l'API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.title("Simple chat")

# Initialisation de l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Acceptation de l'entrée de l'utilisateur
if prompt := st.chat_input("What is up?"):
    # Ajout du message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Obtention de la réponse de l'assistant
    response = query({"inputs": prompt})
    if response and isinstance(response, list) and len(response) > 0 and 'generated_text' in response[0]:
        assistant_response = response[0]['generated_text']
    else:
        assistant_response = "Désolé, je ne peux pas répondre en ce moment."

    # Simulation de la réponse de l'assistant avec un délai
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Ajout de la réponse de l'assistant à l'historique
    st.session_state.messages.append({"role": "assistant", "content": full_response})
