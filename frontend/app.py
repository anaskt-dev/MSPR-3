import streamlit as st
from auth import login, register, get_token, logout, get_with_auth, post_with_auth  # Fonctions d'authentification et d'interaction avec l'API.
from components.sidebar import render_sidebar
from custom_pages.home import render_home
from custom_pages.data import render_data
from custom_pages.predict import render_predict
from custom_pages.login import render_login
from translations import translations
from custom_pages.graphes import render_graphes

# --- Initialisation de st.session_state ---
# Ces variables maintiennent l'état de l'application à travers les différentes exécutions du script.
if "country" not in st.session_state:
    st.session_state["country"] = "France"  # Définit le pays par défaut lors du premier chargement de la session.
if "lang" not in st.session_state:
    st.session_state["lang"] = "Français"  # Définit la langue par défaut de l'interface.

# --- CONFIGURATION DU THÈME ET DE LA PAGE ---
st.set_page_config(page_title="MSPR IA Pandémies", layout="wide")  # Configure le titre de l'onglet du navigateur et le layout large de l'application.

st.markdown("""
    <style>
    .stApp, body {
        background-color: #181a20 !important;
        color: #e3e3e3 !important;
    }
    .stButton>button, .stTextInput>div>input, .stSelectbox>div>div>div>input, .stDataFrame, .stForm, .stExpander, .stTabs, .stMetric, .stMarkdown, .stAlert, .stSidebar, .stSidebarContent {
        background-color: #23242a !important;
        color: #e3e3e3 !important;
        border-radius: 8px;
    }
    .stTextInput>div>input, .stSelectbox>div>div>div>input {
        border: 1px solid #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Affiche le message de couverture des données pour le pays sélectionné, tout en haut de la page, centré, très gros, bleu, en gras, comme le titre principal
banner_msg = ""
if st.session_state["country"] == "France":
    banner_msg = "🇫🇷 Les données affichées couvrent l'ensemble du territoire français."
elif st.session_state["country"] == "Switzerland":
    banner_msg = "🇨🇭 Les données affichées couvrent l'ensemble du territoire suisse."
elif st.session_state["country"] == "US":
    banner_msg = "🇺🇸 Les données affichées couvrent l'ensemble du territoire américain."

if banner_msg:
    st.markdown(f'''
        <h1 style="color:#1976d2; text-align:center; font-size:2.8rem; font-weight:bold; margin-bottom: 2.5rem;">{banner_msg}</h1>
    ''', unsafe_allow_html=True)

# --- RÉCUPÉRATION DE L'UTILISATEUR CONNECTÉ (si besoin) ---
user = st.session_state.get("user", None)
if get_token() and not user:
    user_data = get_with_auth("/me")
    if user_data:
        st.session_state["user"] = user_data
        user = st.session_state["user"]

# --- AFFICHAGE DE LA SIDEBAR ---
with st.sidebar:
    selected = render_sidebar(user)

# --- ROUTAGE DES PAGES EN FONCTION DE LA SÉLECTION DU MENU ---
if selected == translations[st.session_state["lang"]]["home"]:
    t = translations[st.session_state["lang"]]
    render_home(t, get_with_auth)
elif selected == translations[st.session_state["lang"]]["login"]:
    t = translations[st.session_state["lang"]]
    render_login(t, login, register, get_token, logout, get_with_auth, post_with_auth)
elif selected == translations[st.session_state["lang"]]["data"]:
    t = translations[st.session_state["lang"]]
    render_data(t, get_token, get_with_auth)
elif selected == translations[st.session_state["lang"]]["predict"]:
    t = translations[st.session_state["lang"]]
    render_predict(t, get_token, get_with_auth, post_with_auth)
elif selected == translations[st.session_state["lang"]]["graphes"]:
    t = translations[st.session_state["lang"]]
    render_graphes(t)
# ... autres pages si besoin ...

if __name__ == "__main__":
    pass
