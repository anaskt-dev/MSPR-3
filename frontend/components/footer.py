import streamlit as st


def render_footer():
    st.markdown(
        """
        <style>
        .epsi-footer {
            width: 100vw;
            margin-left: calc(-50vw + 50%);
            background: #181a20;
            color: #e3e3e3;
            text-align: center;
            padding: 1.1em 0 0.7em 0;
            font-size: 1.08rem;
            border-top: 2px solid #1976d2;
            box-shadow: 0 -2px 12px #0003;
        }
        .epsi-footer a { color: #1976d2; text-decoration: underline; }
        .epsi-footer img { vertical-align: middle; margin-right: 0.5em; }
        </style>
        <div class='epsi-footer'>
            <a href='https://www.epsi.fr/' target='_blank'>
                <img src='https://www.epsi.fr/wp-content/uploads/2021/09/logo-epsi-blanc.png' alt='Logo EPSI' width='70' style='display:inline-block;vertical-align:middle;'>
            </a>
            <span>Projet EPSI E6.2 – 2025 | <a href='https://www.epsi.fr/' target='_blank'>epsi.fr</a> &nbsp;|&nbsp; made by PandemIA</span>
        </div>
        """,
        unsafe_allow_html=True
    )
