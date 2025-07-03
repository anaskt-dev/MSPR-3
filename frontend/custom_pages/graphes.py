import streamlit as st
import os
from components.footer import render_footer
from PIL import Image


def render_graphes(t):
    # Liste des images et explications associées
    images_info = [
        ("comparaison-modeles.png", "Comparaison visuelle des performances des modèles IA sur les données Covid-19. Permet d'identifier le modèle le plus précis pour la prédiction."),
        ("Comparaison.png", "Comparaison globale des résultats de prédiction sur l'ensemble des modèles testés."),
        ("Comparaison-SMAPE.png", "Comparaison des scores SMAPE (Symmetric Mean Absolute Percentage Error) pour évaluer la précision relative des modèles."),
        ("Comparaison-RMSE.png", "Comparaison des scores RMSE (Root Mean Squared Error) pour mesurer l'écart-type des erreurs de prédiction."),
        ("Comparaison-MAE.png", "Comparaison des scores MAE (Mean Absolute Error) pour évaluer l'erreur moyenne absolue des modèles."),
        ("prévisions-du-taux.png", "Visualisation des prévisions du taux d'évolution de la pandémie sur la période étudiée."),
        ("cumulés.png", "Graphique des cas cumulés pour suivre l'évolution totale des cas au fil du temps."),
        ("top-20.png", "Top 20 des pays les plus impactés par la pandémie selon les données analysées."),
        ("diagramme-des-données-manquantes.png", "Diagramme illustrant la répartition des données manquantes dans le jeu de données Covid-19."),
    ]

    st.markdown("""
        <h2 style='color:#1976d2; text-align:center;'>Visualisation des graphes & résultats IA</h2>
        <p style='text-align:center; color:#aaa;'>Retrouvez ici l'ensemble des visualisations générées par l'IA et l'analyse des données Covid-19.</p>
    """, unsafe_allow_html=True)

    # Affichage en grille 2 colonnes
    for i in range(0, len(images_info), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(images_info):
                img, desc = images_info[i + j]
                img_path = os.path.join(os.path.dirname(__file__), '..', 'image_models', img)
                if os.path.exists(img_path):
                    image = Image.open(img_path)
                    with cols[j]:
                        st.image(image, use_column_width=True, caption=desc)
                        st.markdown(f"<div style='color:#bbb; font-size:1.05rem; margin-bottom:2.5em;'>{desc}</div>", unsafe_allow_html=True)
                else:
                    with cols[j]:
                        st.warning(f"Image manquante : {img_path}")

    # Ajout de la vidéo
    video_path = os.path.join(os.path.dirname(__file__), '..', 'image_models', 'telecharger.mp4')
    if os.path.exists(video_path):
        st.markdown("""
            <h3 style='color:#1976d2; text-align:center; margin-top:2em;'>Présentation vidéo</h3>
            <p style='text-align:center; color:#aaa;'>Découvrez la vidéo de démonstration de l'application PandemIA et de ses fonctionnalités IA.</p>
        """, unsafe_allow_html=True)
        st.video(video_path)
    else:
        st.warning("Vidéo manquante : telecharger.mp4")

    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    render_footer()
