import streamlit as st
import requests

# Configuration de l'API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

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

        st.text_area("Réponse", value=response_text, height=150)
    else:
        st.write("Aucune réponse reçue de l'API.")
