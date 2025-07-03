import streamlit as st


def render_banner(t, st_session_state):
    if st_session_state["selected_page"] in [t["home"], t["data"], t["predict"]]:
        banner_msg = ""
        if st_session_state["country"] == "France":
            banner_msg = "🇫🇷 Les données affichées couvrent l'ensemble du territoire français."
        elif st_session_state["country"] == "Switzerland":
            banner_msg = "🇨🇭 Les données affichées couvrent l'ensemble du territoire suisse."
        elif st_session_state["country"] == "US":
            banner_msg = "🇺🇸 Les données affichées couvrent l'ensemble du territoire américain."
        if banner_msg:
            st.markdown(f"""
                <h1 style='color:#1976d2; text-align:center; font-size:2.2rem; font-weight:bold; margin-bottom: 2.5rem; margin-top:0.5em;'>
                    {banner_msg}
                </h1>
            """, unsafe_allow_html=True)
    # Bandeau RGPD pro, fixe en bas de page
    st.markdown(
        """
        <style>
        .rgpd-banner {
            position: fixed;
            left: 0; right: 0; bottom: 0;
            width: 100vw;
            background: #23242a;
            color: #fff;
            text-align: center;
            padding: 0.7em 0 0.5em 0;
            font-size: 1rem;
            z-index: 1000;
            border-top: 2px solid #1976d2;
            box-shadow: 0 -2px 12px #0003;
        }
        .rgpd-banner a { color: #1976d2; text-decoration: underline; }
        </style>
        <div class='rgpd-banner'>
            🔒 Cette plateforme respecte le RGPD : vos données sont protégées, anonymisées et ne sont jamais partagées sans consentement. <a href='#' target='_blank'>En savoir plus</a>
        </div>
        """,
        unsafe_allow_html=True
    )
