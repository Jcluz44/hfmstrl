import streamlit as st
import requests
import json

# Remplacez 'your_api_token_here' par votre token Hugging Face
API_TOKEN = 'your_api_token_here'

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Interface Streamlit
st.title('Hugging Face API Query Tool')

# Boîte de texte pour la requête utilisateur
user_input = st.text_input("Entrez votre requête ici", "Can you please let us know more details about your ")

# Bouton pour envoyer la requête
if st.button('Envoyer la requête'):
    output = query({"inputs": user_input})
    
    # Vérifier si la réponse contient du code
    if isinstance(output, dict) and "code" in output:
        # Afficher le code
        st.code(output["code"], language="python")
    else:
        # Afficher la réponse JSON de manière élégante
        st.json(output)
