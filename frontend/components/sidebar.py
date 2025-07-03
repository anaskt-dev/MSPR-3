from translations import translations
import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar(user=None):
    # Définit l'objet de traduction (dictionnaire 't') basé sur la langue actuellement sélectionnée dans la session.
    t = translations[st.session_state["lang"]]

    # --- LOGO ---
    st.markdown(
        """
        <div style='text-align:center; margin-bottom:1.5rem;'>
            <img src='logo-pandemia.png' width='100' style='margin:auto;display:block;'/>
        </div>
        """, unsafe_allow_html=True
    )
    # --- PROFIL UTILISATEUR ---
    if user:
        st.markdown(
            f"""
            <div style='text-align:center; margin-bottom:1rem;'>
                <div style='font-size:1.1rem; color:#1976d2;'><b>{user['username']}</b></div>
                <div style='font-size:0.9rem; color:#888;'>{user['email']}</div>
            </div>
            """, unsafe_allow_html=True
        )

    # --- SÉLECTION DU PAYS ---
        country_selected_sidebar = st.selectbox(t["country"],
                                                ["France", "Switzerland", "US"],
                                                index=["France", "Switzerland", "US"].index(st.session_state["country"]) if st.session_state["country"] in ["France", "Switzerland", "US"] else 0,
                                                key="sidebar_country_select")
        st.session_state["country"] = country_selected_sidebar

    # --- LOGIQUE DE SÉLECTION DE LA LANGUE BASÉE SUR LE PAYS ---
    if st.session_state["country"] == "Switzerland":
        lang_options = ["Français", "Italien", "Allemand"]
        current_lang_in_swiss = st.session_state.get("lang", "Français")
        if current_lang_in_swiss not in lang_options:
            current_lang_in_swiss = lang_options[0]
        lang_from_selector = st.selectbox(
            t["choose_lang"],
            lang_options,
            index=lang_options.index(current_lang_in_swiss),
            key="language_selector"
        )
        st.session_state["lang"] = lang_from_selector
    else:
        if st.session_state["country"] == "France":
            st.session_state["lang"] = "Français"
        elif st.session_state["country"] == "US":
            st.session_state["lang"] = "Anglais"
    # Sécurisation : si la langue n'existe pas dans translations, fallback sur 'Français'
    if st.session_state["lang"] not in translations:
        st.session_state["lang"] = "Français"
    t = translations[st.session_state["lang"]]

    # --- MENU DE NAVIGATION PRINCIPAL ---
    options = [t["home"], t["login"]]
    country = st.session_state["country"].strip().lower()
    if country == "france":
        options.append(t["data"])
    elif country == "us":
        options.extend([t["data"], t["predict"]])
    elif country == "switzerland":
        options.append(t["predict"])
    # Ajout de la page Graphes pour tous
    options.append(t["graphes"])

    icons = ["house", "box-arrow-in-right"]
    if t["data"] in options:
        icons.append("bar-chart")
    if t["predict"] in options:
        icons.append("robot")
    icons.append("graph-up")

    current_selected_page = st.session_state.get("selected_page", t["home"])
    if current_selected_page not in options:
        current_selected_page = t["home"]

    selected = option_menu(
        menu_title=None,
        options=options,
        icons=icons,
        menu_icon="cast",
        default_index=options.index(current_selected_page),
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#23242a"},
            "icon": {"color": "#1976d2", "font-size": "24px"},
            "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#e3f2fd", },
            "nav-link-selected": {"background-color": "#1976d2", "color": "white"},
        }
    )
    st.session_state["selected_page"] = selected
    return selected
