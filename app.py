import streamlit as st
import requests

# Configuration de l'API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    # Ajout de l'instruction spéciale à chaque requête
    instruction = "[INST] You are a general purpose model. Gently answer to human questions in a synthetic way [/INST]"
    modified_payload = {"inputs": instruction + " " + payload["inputs"]}
    response = requests.post(API_URL, headers=headers, json=modified_payload)
    return response.json()

st.title("Simple chat")

# Initialisation de l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Conteneur pour la mise à jour dynamique de la réponse
container = st.container()

# Acceptation de l'entrée de l'utilisateur
prompt = st.chat_input("What is up?")
if prompt:
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

    # Mise à jour de l'affichage avec la nouvelle réponse
    with container:
        for message in st.session_state.messages[-2:]:  # Affiche le dernier message de l'utilisateur et la réponse de l'assistant
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
