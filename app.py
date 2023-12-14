import streamlit as st
import requests

# Configuration de l'API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Initialisation de l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Simple chat")

# Affichage des messages de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée de l'utilisateur
if prompt := st.chat_input("What is up?"):
    # Ajout du message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Obtention de la réponse de l'assistant
    response = query({"inputs": prompt})
    if response and isinstance(response, list) and len(response) > 0 and 'generated_text' in response[0]:
        assistant_response = response[0]['generated_text']
    else:
        assistant_response = "Désolé, je ne peux pas répondre en ce moment."

    # Ajout de la réponse de l'assistant à l'historique
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
