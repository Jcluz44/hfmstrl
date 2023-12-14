import streamlit as st
import requests

# Configuration de l'API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    # Ajout de l'instruction spéciale à la requête
    instruction = "[INST] Tu es un assistant généraliste et aide à répondre aux questions sur un ton familier. [/INST]"
    modified_payload = {"inputs": instruction + payload["inputs"]}
    response = requests.post(API_URL, headers=headers, json=modified_payload)
    return response.json()

def clean_response(text):
    # Suppression de l'instruction de la réponse
    instruction = "[INST] Tu es un assistant généraliste et aide à répondre aux questions sur un ton familier. [/INST]"
    return text.replace(instruction, "").strip()

# Création de l'interface Streamlit
st.title('Chat avec Mistral AI')

# Champ de saisie pour l'utilisateur
user_input = st.text_input("Posez votre question:")

if user_input:
    # Envoi de la requête à l'API
    response = query({"inputs": user_input})

    # Vérification et affichage de la réponse
    if response:
        # S'assurer que la réponse est un dictionnaire et contient la clé 'generated_text'
        if isinstance(response, dict) and 'generated_text' in response:
            clean_text = clean_response(response['generated_text'])
            st.text_area("Réponse", value=clean_text, height=150)
        else:
            st.write("La réponse n'est pas dans le format attendu.")
    else:
        st.write("Aucune réponse reçue de l'API.")
