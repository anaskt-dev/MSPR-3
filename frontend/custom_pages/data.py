import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from components.footer import render_footer


def render_data(t, get_token, get_with_auth):
    st.markdown(f"<h2 style='font-size:2.2rem;'>{t['data_title']}</h2>", unsafe_allow_html=True)
    token = get_token()
    if not token:
        st.warning(t["connect_warn"])
    else:
        country_selected = st.session_state["country"]
        data = get_with_auth("/data", params={"country": country_selected})
        if data:
            df = pd.DataFrame(data)
            df["date"] = pd.to_datetime(df["date"])
            st.subheader("📈 " + t["value_dist"])
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=df["date"],
                y=df["confirmed"],
                name=t["confirmed"],
                marker=dict(color='cyan'),
                yaxis='y1'
            ))
            fig1.add_trace(go.Scatter(
                x=df["date"],
                y=(df["deaths"] / df["confirmed"] * 100).fillna(0),
                name=t["death_rate"],
                yaxis='y2',
                mode='lines',
                line=dict(color='pink')
            ))
            fig1.update_layout(
                xaxis=dict(title=t["date"]),
                yaxis=dict(title=t["confirmed"], side='left'),
                yaxis2=dict(title=t["death_rate"] + " (%)", overlaying='y', side='right'),
                bargap=0.1,
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white'),
                legend=dict(x=0.01, y=0.99)
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.subheader("📈 " + t["new_cases"] + " vs " + t["recovery_rate"])
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df["date"],
                y=df["new_cases"],
                name=t["new_cases"],
                marker=dict(color='cyan'),
                yaxis='y1'
            ))
            fig2.add_trace(go.Scatter(
                x=df["date"],
                y=(df["recovered"] / df["confirmed"] * 100).fillna(0),
                name=t["recovery_rate"],
                yaxis='y2',
                mode='lines',
                line=dict(color='pink')
            ))
            fig2.update_layout(
                xaxis=dict(title=t["date"]),
                yaxis=dict(title=t["new_cases"], side='left'),
                yaxis2=dict(title=t["recovery_rate"] + " (%)", overlaying='y', side='right'),
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white'),
                legend=dict(x=0.01, y=0.99)
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.subheader("📉 " + t["cases_overview"])
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=df["date"],
                y=df["confirmed"],
                name=t["confirmed"],
                line=dict(color='magenta')
            ))
            fig3.add_trace(go.Scatter(
                x=df["date"],
                y=df["deaths"],
                name=t["deaths"],
                yaxis='y2',
                line=dict(color='pink')
            ))
            fig3.update_layout(
                xaxis=dict(title=t["date"]),
                yaxis=dict(title=t["confirmed"]),
                yaxis2=dict(title=t["deaths"], overlaying='y', side='right'),
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white')
            )
            st.plotly_chart(fig3, use_container_width=True)
            st.subheader("📊 " + t["metrics_overview"])
            col1, col2, col3 = st.columns(3)
            with col1:
                total_confirmed = int(df["confirmed"].sum())
                st.metric(label=t["total_confirmed"], value=f"{total_confirmed:,}")
                fig4 = go.Figure(go.Scatter(
                    x=df["date"],
                    y=df["confirmed"].cumsum(),
                    line=dict(color='lightgreen')
                ))
                fig4.update_layout(
                    height=250,
                    paper_bgcolor='black',
                    plot_bgcolor='black',
                    font=dict(color='white')
                )
                st.plotly_chart(fig4, use_container_width=True)
            with col2:
                total_deaths = int(df["deaths"].sum())
                st.metric(label=t["total_deaths"], value=f"{total_deaths:,}")
                fig5 = go.Figure(go.Scatter(
                    x=df["date"],
                    y=df["deaths"].cumsum(),
                    line=dict(color='lightyellow')
                ))
                fig5.update_layout(
                    height=250,
                    paper_bgcolor='black',
                    plot_bgcolor='black',
                    font=dict(color='white')
                )
                st.plotly_chart(fig5, use_container_width=True)
            with col3:
                total_recovered = int(df["recovered"].sum())
                st.metric(label=t["total_recovered"], value=f"{total_recovered:,}")
                fig6 = go.Figure(go.Scatter(
                    x=df["date"],
                    y=df["recovered"].cumsum(),
                    line=dict(color='lightblue')
                ))
                fig6.update_layout(
                    height=250,
                    paper_bgcolor='black',
                    plot_bgcolor='black',
                    font=dict(color='white')
                )
                st.plotly_chart(fig6, use_container_width=True)
        else:
            st.error(t["data_error"])
    st.markdown(f"<div style='text-align:right; color:#1976d2; font-size:1.1rem;'><b>{t['country']} : {st.session_state['country']}</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    render_footer()


def render_data_old(t, st_session_state, get_with_auth):
    st.title(t["data_title"])
    if not st.session_state.get("user"):
        st.warning(t["connect_warn"])
        return
    # Récupérer dynamiquement la liste des pays
    COUNTRIES_URL = "http://backend:8000/api/countries"
    try:
        countries_resp = requests.get(COUNTRIES_URL)
        countries_resp.raise_for_status()
        countries = countries_resp.json()
        countries = sorted(list(set(countries)))
    except Exception as e:
        st.error(f"Erreur lors du chargement des pays : {e}")
        countries = ["France"]
    # Sélecteur de pays
    default_country = st_session_state.get("country", "France")
    pays = st.selectbox("Pays", ["Tous"] + countries, index=(["Tous"] + countries).index(default_country) if default_country in countries else 0)
    st.session_state["country"] = pays if pays != "Tous" else countries[0]
    # Récupérer les données du backend
    try:
        params = {}
        if pays != "Tous":
            params["country"] = pays
        data = get_with_auth("/data", params=params)
        if not data or len(data) == 0:
            st.error(t["data_error"])
            return
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        if pays != "Tous":
            df = df[df["country"] == pays]
        if df.empty or "confirmed" not in df.columns:
            st.warning("Aucune donnée disponible pour ce pays.")
            return
        # Cartes de métriques
        st.markdown("<h3 style='color:#1976d2;'>Chiffres clés</h3>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(t["confirmed"], f"{df['confirmed'].sum():,}")
        col2.metric(t["deaths"], f"{df['deaths'].sum():,}")
        col3.metric(t["recovered"], f"{df['recovered'].sum():,}")
        col4.metric(t["new_cases"], f"{df['new_cases'].sum():,}")
        st.markdown("---")
        # Graphique 1 : Cas confirmés et décès (barres + ligne)
        st.subheader(f"{t['confirmed']} & {t['deaths']} ({pays})")
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=df["date"], y=df["confirmed"], name=t["confirmed"], marker_color='cyan'))
        fig1.add_trace(go.Scatter(x=df["date"], y=df["deaths"], name=t["deaths"], mode='lines', line=dict(color='red')))
        fig1.update_layout(barmode='group', xaxis_title=t["date"], yaxis_title=t["confirmed"], plot_bgcolor='#181a20', paper_bgcolor='#181a20', font=dict(color='white'))
        st.plotly_chart(fig1, use_container_width=True)
        # Graphique 2 : Nouveaux cas et taux de guérison
        st.subheader(f"{t['new_cases']} & {t['recovery_rate']} ({pays})")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=df["date"], y=df["new_cases"], name=t["new_cases"], marker_color='orange'))
        recovery_rate = (df["recovered"] / df["confirmed"]).fillna(0) * 100
        fig2.add_trace(go.Scatter(x=df["date"], y=recovery_rate, name=t["recovery_rate"], mode='lines', line=dict(color='green')))
        fig2.update_layout(barmode='group', xaxis_title=t["date"], yaxis_title=t["new_cases"], plot_bgcolor='#181a20', paper_bgcolor='#181a20', font=dict(color='white'))
        st.plotly_chart(fig2, use_container_width=True)
        # Graphique 3 : Vue d'ensemble des cas
        st.subheader(t["cases_overview"])
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df["date"], y=df["confirmed"].cumsum(), name=t["confirmed"], line=dict(color='magenta')))
        fig3.add_trace(go.Scatter(x=df["date"], y=df["deaths"].cumsum(), name=t["deaths"], line=dict(color='pink')))
        fig3.update_layout(xaxis_title=t["date"], yaxis_title=t["confirmed"], plot_bgcolor='#181a20', paper_bgcolor='#181a20', font=dict(color='white'))
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("---")
        # Tableau interactif
        st.subheader(t["table"])
        st.dataframe(df, use_container_width=True)
        st.write(f"{t['entries']} : {len(df)}")
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
