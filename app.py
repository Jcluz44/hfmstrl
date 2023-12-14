import streamlit as st
import requests
import json

# Configuration de l'API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    # Ajout de l'instruction spéciale à chaque requête
    instruction = "[INST] Tu es un assistant généraliste, tu réponds familièrement aux demandes, et en français [/INST]"
    modified_payload = {"inputs": instruction + payload["inputs"]}
    response = requests.post(API_URL, headers=headers, json=modified_payload)
    return response.json()

st.title('Chatbot Mistral AI')

# Initialisation de l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Acceptation de l'entrée de l'utilisateur
user_input = st.text_input("Posez votre question:", key="user_input")

# Gestion de la soumission de l'utilisateur
if st.button("Envoyer"):
    if user_input:
        # Ajout du message de l'utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Envoi de la requête à l'API et réception de la réponse
        response = query({"inputs": user_input})
        if response:
            # Extraction de la réponse
            response_text = response[0].get('generated_text', "Pas de réponse générée.") if isinstance(response, list) else response.get('generated_text', "Pas de réponse générée.")
            # Ajout de la réponse de l'assistant à l'historique
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            # Affichage du JSON brut pour le débogage
            st.json(response)
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Désolé, je ne peux pas répondre en ce moment."})

        # Réinitialisation du champ de saisie
        st.session_state.user_input = ""

# Affichage des messages de l'historique
for message in st.session_state.messages:
    with st.container():
        st.text_area(f"{message['role'].capitalize()} dit:", value=message["content"], height=75)
