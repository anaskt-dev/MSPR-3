import streamlit as st
from components.footer import render_footer

def render_login(t, login, register, get_token, logout, get_with_auth, post_with_auth):
    st.markdown(f"<h2 style='font-size:2.2rem;'>{t['login_title']}</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs([t["login"], t["register_tab"]])
    with tab1:
        username = st.text_input(t["username"])
        password = st.text_input(t["password"], type="password")
        if st.button(t["login_btn"]):
            if login(username, password):
                st.session_state["logged_in"] = True
                st.experimental_rerun()
    with tab2:
        with st.expander(t["register_tab"]):
            with st.form("register_form"):
                reg_username = st.text_input(t["username"], key="reg_user")
                reg_email = st.text_input(t["email"], key="reg_email")
                reg_password = st.text_input(t["password"], type="password", key="reg_pass")
                reg_country = st.selectbox(t["country"], options=st.session_state.get("available_countries", ["France"]), key="reg_country")
                submitted = st.form_submit_button(t["register_btn"])
                if submitted:
                    success, message = register(reg_username, reg_email, reg_password, reg_country)
                    if success:
                        st.success(t["register_success"])
                    else:
                        st.error(f'{t["register_error"]}: {message}')
    if get_token():
        if st.button(t["logout"]):
            logout()
            st.success(t["disconnect"])
            st.experimental_rerun()
    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    render_footer() 