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
        # Vérifie si la réponse est sous forme de liste ou de dictionnaire
        if isinstance(response, list):
            # Prendre le premier élément si la réponse est une liste
            response_text = response[0].get('generated_text', "Pas de réponse générée.")
        elif isinstance(response, dict):
            # Directement accéder à 'generated_text' si la réponse est un dictionnaire
            response_text = response.get('generated_text', "Pas de réponse générée.")
        else:
            response_text = "Format de réponse inattendu."

        # Nettoyage et affichage de la réponse
        clean_text = clean_response(response_text)
        st.text_area("Réponse", value=clean_text, height=150)
    else:
        st.write("Aucune réponse reçue de l'API.")
