import streamlit as st
from components.footer import render_footer

# Squelette de la page Statistiques avancées


def render_statistiques():
    st.title("Statistiques avancées par région")
    st.write("Analysez l'évolution de la pandémie par région.")

    # Sélecteur de pays (à adapter selon les données disponibles)
    st.selectbox("Pays", ["France", "US", "Switzerland"])

    # Sélecteur de région (sera alimenté dynamiquement)
    st.selectbox("Région", ["Toutes", "Région 1", "Région 2", "Région 3"])

    # Placeholder pour les graphiques
    st.info("Les graphiques par région seront affichés ici.")

    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    render_footer()
