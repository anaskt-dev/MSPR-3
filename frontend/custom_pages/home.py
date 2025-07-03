import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry_convert as pc
from components.footer import render_footer


def render_home(t, get_with_auth):
    st.markdown("""
    <style>
    .hero-full {
        width: 100vw;
        margin-left: calc(-50vw + 50%);
        background: #181a20;
        border-radius: 0 0 32px 32px;
        box-shadow: 0 4px 24px #0002;
        padding: 3.5em 0 2.5em 0;
        text-align: center;
    }
    .atouts-row {
        display: flex;
        justify-content: center;
        gap: 2.5em;
        flex-wrap: wrap;
        margin: 0 auto 2.5em auto;
        max-width: 1200px;
    }
    .atout {
        min-width: 180px;
        max-width: 220px;
        margin: 1em auto;
        text-align: center;
    }
    .atout-title {
        font-weight: 700;
        color: #1976d2;
        margin-bottom: 0.2em;
    }
    .atout-desc {
        color: #e3e3e3;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; margin-top: 30px; margin-bottom: 0;'>"
                f"<h1 style='color:#1976d2; font-size:3.2rem; font-weight:900; margin-bottom:0.2em; letter-spacing:1px;'>PandemIA</h1>"
                f"<h2 style='color:#43a047; font-size:2.1rem; font-weight:700; margin-top:0; margin-bottom:0.7em; letter-spacing:0.5px;'>"
                f"{t['subtitle']}"
                f"</h2>"
                f"<p style='font-size:1.35rem; color:#e3e3e3; max-width:950px; margin:auto; margin-bottom:1.5em; font-weight:500;'>"
                f"Une plateforme intelligente pour suivre, analyser et prédire l'évolution de la pandémie Covid-19 dans le monde."
                f"</p>"
                f"<div style='display:flex; justify-content:center; gap:2.5em; flex-wrap:wrap; margin-bottom:2.5em; max-width:1100px; margin-left:auto; margin-right:auto;'>"
                f"<div style='min-width:220px; max-width:260px; background:#23242a; border-radius:16px; padding:1.2em 1em; box-shadow:0 2px 12px #0002; text-align:center;'>"
                f"<div style='font-size:2.2rem;'>🤖</div>"
                f"<div style='font-size:1.18rem; color:#1976d2; font-weight:700; margin-bottom:0.2em;'>Prédictions IA</div>"
                f"<div style='color:#bdbdbd; font-size:1.05rem;'>Anticipez l'évolution des cas grâce à des modèles avancés (Prophet, LSTM).</div>"
                f"</div>"
                f"<div style='min-width:220px; max-width:260px; background:#23242a; border-radius:16px; padding:1.2em 1em; box-shadow:0 2px 12px #0002; text-align:center;'>"
                f"<div style='font-size:2.2rem;'>🌍</div>"
                f"<div style='font-size:1.18rem; color:#1976d2; font-weight:700; margin-bottom:0.2em;'>Données mondiales</div>"
                f"<div style='color:#bdbdbd; font-size:1.05rem;'>Visualisez les taux de cas, décès et guérisons par pays et continent.</div>"
                f"</div>"
                f"<div style='min-width:220px; max-width:260px; background:#23242a; border-radius:16px; padding:1.2em 1em; box-shadow:0 2px 12px #0002; text-align:center;'>"
                f"<div style='font-size:2.2rem;'>🛡️</div>"
                f"<div style='font-size:1.18rem; color:#1976d2; font-weight:700; margin-bottom:0.2em;'>Support décisionnel</div>"
                f"<div style='color:#bdbdbd; font-size:1.05rem;'>Aidez les décideurs à prendre les bonnes mesures grâce à des analyses interactives.</div>"
                f"</div>"
                f"</div>"
                f"</div>", unsafe_allow_html=True)
    st.markdown("---")

    global_data = get_with_auth("/data")
    if global_data:
        df_global = pd.DataFrame(global_data)
        df_global["date"] = pd.to_datetime(df_global["date"])
        total_cases = int(df_global["confirmed"].sum())
        total_deaths = int(df_global["deaths"].sum())
        total_recovered = int(df_global["recovered"].sum())
        num_countries = df_global["country"].nunique()
        last_date = df_global["date"].max()
        new_cases = int(df_global[df_global["date"] == last_date]["new_cases"].sum())
        st.markdown("<div style='text-align:center; margin-bottom: 1.5rem;'>"
                    "<h2 style='color:#1976d2;'>Statistiques mondiales Covid-19</h2>"
                    "<p style='color:#888; font-size:1.1rem;'>Vue d'ensemble de tous les pays suivis</p></div>", unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric(t["confirmed"], f"{total_cases:,}")
        col2.metric(t["deaths"], f"{total_deaths:,}")
        col3.metric(t["recovered"], f"{total_recovered:,}")
        col4.metric(t["new_cases"] + f" ({t['date']})", f"{new_cases:,}")
        col5.metric(t["countries_tracked"], num_countries)
        st.markdown("---")

        # --- Analyse interactive des données COVID-19 avec regroupement par continent ---
        def get_continent(country_name):
            try:
                country_code = pc.country_name_to_country_alpha2(country_name)
                continent_code = pc.country_alpha2_to_continent_code(country_code)
                continent_name = {
                    'AF': 'Afrique',
                    'AS': 'Asie',
                    'EU': 'Europe',
                    'NA': 'Amérique du Nord',
                    'SA': 'Amérique du Sud',
                    'OC': 'Océanie',
                    'AN': 'Antarctique'
                }.get(continent_code, 'Autre')
                return continent_name
            except Exception:
                return 'Autre'
        df_global["continent"] = df_global["country"].apply(get_continent)

    st.markdown("""
        <h3 style='color:#1976d2; font-size:1.5rem; font-weight:700; text-align:center; margin-top:2em;'>Analyse interactive des données COVID-19</h3>
    """, unsafe_allow_html=True)

    if global_data:
        categories = ['continent']
        valeurs = ['confirmed', 'deaths', 'recovered']
        cat = st.selectbox("Catégorie :", categories, index=0, key="covid_cat")
        val = st.selectbox("Valeur :", valeurs, index=0, key="covid_val")
        fig = px.pie(df_global, values=val, names=cat, hole=.3, title=f"Répartition de {val} par {cat}")
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            legend=dict(font=dict(color='white')),
        )
        st.plotly_chart(fig, use_container_width=True)
        # --- Carte interactive ECharts supprimée ---
        # (Aucune carte affichée ici)
    else:
        st.info(t["no_data"])

    st.markdown(f"<div style='text-align:center; margin-top: 30px;'>"
                f"<h2 style='color:#1976d2; font-size:2rem;'>{t['who']}</h2>"
                f"</div>", unsafe_allow_html=True)
    st.write(f"<p style='font-size:1.1rem; text-align:center;'>{t['team_desc']}</p>", unsafe_allow_html=True)

    # --- Section équipe ---
    st.markdown("""
    <div style='display:flex; justify-content:center; gap:2.5em; flex-wrap:wrap; margin-bottom:2em;'>
        <div style='text-align:center; min-width:180px; max-width:220px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='90' alt='Avatar Anas' style='border-radius:50%; border:3px solid #1976d2; box-shadow:0 2px 8px #0002; margin-bottom:0.7em;'/>
            <div style='font-size:1.15rem; font-weight:bold; color:#1976d2;'>Anas</div>
            <div style='font-size:1.05rem; color:#e3e3e3; margin-bottom:0.2em;'>🧠 Développeur IA</div>
        </div>
        <div style='text-align:center; min-width:180px; max-width:220px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='90' alt='Avatar Laura' style='border-radius:50%; border:3px solid #1976d2; box-shadow:0 2px 8px #0002; margin-bottom:0.7em;'/>
            <div style='font-size:1.15rem; font-weight:bold; color:#1976d2;'>Laura</div>
            <div style='font-size:1.05rem; color:#e3e3e3; margin-bottom:0.2em;'>💻🛠️ Développeur fullstack & Devops</div>
        </div>
        <div style='text-align:center; min-width:180px; max-width:220px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='90' alt='Avatar Akram' style='border-radius:50%; border:3px solid #1976d2; box-shadow:0 2px 8px #0002; margin-bottom:0.7em;'/>
            <div style='font-size:1.15rem; font-weight:bold; color:#1976d2;'>Akram</div>
            <div style='font-size:1.05rem; color:#e3e3e3; margin-bottom:0.2em;'>🛠️ Développeur Devops</div>
        </div>
        <div style='text-align:center; min-width:180px; max-width:220px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png' width='90' alt='Avatar Romance' style='border-radius:50%; border:3px solid #1976d2; box-shadow:0 2px 8px #0002; margin-bottom:0.7em;'/>
            <div style='font-size:1.15rem; font-weight:bold; color:#1976d2;'>Romance</div>
            <div style='font-size:1.05rem; color:#e3e3e3; margin-bottom:0.2em;'>💻 Développeur fullstack</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Section Documentation & Accessibilité
    with st.expander('📄 Documentation & Accessibilité', expanded=False):
        st.markdown('''
        ### Accessibilité & Conformité
        - **Contrastes élevés** et thème sombre pour une meilleure lisibilité.
        - **Polices lisibles** et tailles adaptées.
        - **Navigation clavier** possible sur tous les menus et formulaires.
        - **Descriptions textuelles** pour les images et avatars.
        - **RGPD** : aucune donnée personnelle n'est stockée sans consentement.
        - **Conformité WCAG** : l'application vise le niveau AA (contrastes, navigation, alternatives textuelles, etc.).
        ### Mode d'emploi rapide
        1. Naviguez via la barre latérale pour accéder aux différentes pages.
        2. Sélectionnez votre pays et votre langue.
        3. Consultez les données, visualisations et prédictions IA.
        4. Utilisez le bouton de documentation pour plus d'infos techniques.
        ''')

    # Section Contexte, Objectifs et Livrables (déplacée en bas)
    st.markdown('''
    <div style='background:#23242a; border-radius:18px; padding:2em 2em 1.5em 2em; margin-bottom:2em; box-shadow:0 2px 12px #0002;'>
        <h2 style='color:#1976d2; font-size:2rem; font-weight:800; margin-bottom:0.5em;'>Contexte & Objectifs</h2>
        <p style='font-size:1.15rem; color:#e3e3e3; margin-bottom:1.2em;'>
            Ce projet s'inscrit dans le cadre du bloc E6.2 de l'EPSI et vise à développer une plateforme professionnelle de suivi et de prédiction de la pandémie Covid-19, accessible et conforme aux standards internationaux (OMS, WCAG).
        </p>
        <ul style='font-size:1.08rem; color:#bdbdbd; margin-bottom:1.2em;'>
            <li><b>API IA</b> : Prédiction de l'évolution de la pandémie avec Prophet & LSTM</li>
            <li><b>Dashboard interactif</b> : Visualisations modernes, filtrage par pays/continent</li>
            <li><b>Accessibilité</b> : Thème sombre, navigation clavier, contrastes, descriptions</li>
            <li><b>Conformité RGPD</b> : Protection et anonymisation des données</li>
        </ul>
        <h3 style='color:#43a047; font-size:1.3rem; font-weight:700; margin-bottom:0.3em;'>Livrables attendus</h3>
        <ul style='font-size:1.05rem; color:#bdbdbd;'>
            <li>API FastAPI (modèles IA, endpoints sécurisés)</li>
            <li>Frontend Streamlit (UI moderne, visualisations, accessibilité)</li>
            <li>Documentation technique & accessibilité</li>
            <li>Tableau de bord interactif</li>
            <li>Conformité WCAG & RGPD</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    render_footer()
