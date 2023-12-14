import streamlit as st
import requests

# Configuration de l'API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
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
        # Extraction du texte généré à partir de la réponse JSON
        if isinstance(response, list) and len(response) > 0 and 'generated_text' in response[0]:
            generated_text = response[0]['generated_text']
            st.text_area("Réponse", value=generated_text, height=150)
        else:
            st.write("La réponse n'est pas dans le format attendu.")
    else:
        st.write("Aucune réponse reçue de l'API.")
