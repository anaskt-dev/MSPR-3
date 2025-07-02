import streamlit as st
import requests
import os

# Configuration de l'URL de l'API selon le contexte d'exécution
# En Docker Compose, le backend est accessible via 'backend:8000'
# En local, il faut utiliser 'localhost:8000'
if os.getenv('DOCKER_ENV'):
    API_URL = "http://backend:8000/api"
else:
    API_URL = "http://localhost:8000/api"

# Connexion utilisateur

def login(username, password):
    data = {"username": username, "password": password}
    try:
        response = requests.post(f"{API_URL}/login", data=data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            st.session_state["token"] = token
            # Récupérer les infos utilisateur
            user = get_with_auth("/me")
            if user:
                st.session_state["user"] = user
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Erreur de connexion: {e}")
        return False

# Inscription utilisateur

def register(username, email, password, country, is_admin=False):
    # Validation côté frontend
    if not username or not email or not password or not country:
        return False, "Tous les champs sont obligatoires."
    if "@" not in email or "." not in email:
        return False, "L'email n'est pas valide."
    if len(password) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caractères."
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "country": country
    }
    try:
        response = requests.post(f"{API_URL}/register", json=payload)
        if response.status_code == 200:
            return True, "Inscription réussie"
        else:
            try:
                error_msg = response.json().get("detail", "Erreur lors de l'inscription")
            except Exception:
                error_msg = "Erreur lors de l'inscription"
            return False, error_msg
    except Exception as e:
        return False, f"Erreur d'inscription: {e}"

# Récupérer le token JWT

def get_token():
    return st.session_state.get("token")

# Déconnexion

def logout():
    st.session_state.pop("user", None)
    st.session_state.pop("token", None)

# GET avec authentification

def get_with_auth(path, params=None):
    token = get_token()
    if not token:
        st.error("Vous devez être connecté pour accéder à cette ressource.")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}{path}", headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            try:
                error_msg = response.json().get("detail", f"Erreur API ({response.status_code})")
            except Exception:
                error_msg = f"Erreur API ({response.status_code})"
            st.error(error_msg)
            return None
    except Exception as e:
        st.error(f"Erreur API: {e}")
        return None

# POST avec authentification

def post_with_auth(path, payload):
    token = get_token()
    if not token:
        st.error("Vous devez être connecté pour accéder à cette ressource.")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{API_URL}{path}", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            try:
                error_msg = response.json().get("detail", f"Erreur API ({response.status_code})")
            except Exception:
                error_msg = f"Erreur API ({response.status_code})"
            st.error(error_msg)
            return None
    except Exception as e:
        st.error(f"Erreur API: {e}")
        return None 