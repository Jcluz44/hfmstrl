import streamlit as st
import requests
import time

# Configuration de l'API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    # Ajout de l'instruction spéciale à chaque requête
    instruction = "[INST] You are a general purpose model. Gently answer to human questions in a synthetic way. Use french language. [/INST]"
    modified_payload = {"inputs": instruction + " " + payload["inputs"]}
    response = requests.post(API_URL, headers=headers, json=modified_payload)
    return response.json()

def clean_response(text):
    # Suppression de l'instruction et de tout texte avant la réponse réelle
    start_index = text.find("Model answer")
    if start_index != -1:
        # Suppression de tout le texte avant et y compris "Model answer"
        return text[start_index + len("Model answer"):].strip()
    else:
        return text

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
prompt = st.chat_input("Comment puis-je t'aider ?")
if prompt:
    # Ajout du message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Simuler un temps de réflexion
    time.sleep(2)  # Ajoute un délai de 2 secondes pour simuler la réflexion

    # Obtention de la réponse de l'assistant
    response = query({"inputs": prompt})
    if response and isinstance(response, list) and len(response) > 0 and 'generated_text' in response[0]:
        raw_response = response[0]['generated_text']
        assistant_response = clean_response(raw_response)
    else:
        assistant_response = "Désolé, je ne peux pas répondre en ce moment."

    # Ajout de la réponse de l'assistant à l'historique
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    # Mise à jour de l'affichage avec la nouvelle réponse
    with container:
        for message in st.session_state.messages[-2:]:  # Affiche le dernier message de l'utilisateur et la réponse de l'assistant
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
