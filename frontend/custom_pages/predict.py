import streamlit as st
import pandas as pd
from datetime import date, datetime
from components.footer import render_footer

def render_predict(t, get_token, get_with_auth, post_with_auth):
    st.markdown(f"<h2 style='font-size:2.2rem;'>{t['predict_title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:1.1rem; color:#888;'>{t['ai_pred_desc']}</p>", unsafe_allow_html=True)
    
    # Informations sur la prédiction historique
    st.info("📅 **Prédiction historique COVID-19** : Ce modèle a été entraîné sur les données de 2020. Choisissez une date de référence historique pour simuler une prédiction réaliste.")
    
    token = get_token()
    if not token:
        st.warning(t["predict_warn"])
    else:
        # Récupérer la liste des pays via l'endpoint dédié
        countries_list = get_with_auth("/countries")
        available_countries = sorted(countries_list) if countries_list else []
        if available_countries:
            with st.container(border=True):
                with st.form("prediction_form"):
                    st.subheader("🎯 Paramètres de prédiction")
                    # Sélection du pays
                    country_predict = st.selectbox(t["country"], available_countries, key="predict_country_select")
                    # Date de référence historique (2020)
                    st.markdown("**📅 Date de référence historique**")
                    st.markdown("*Choisissez une date en 2020 à partir de laquelle faire la prédiction*")
                    default_historical_date = date(2020, 7, 1)
                    reference_date = st.date_input(
                        "Date de référence (2020)", 
                        value=default_historical_date,
                        min_value=date(2020, 1, 1),
                        max_value=date(2020, 12, 31),
                        key="reference_date_input"
                    )
                    days_to_predict = st.slider(
                        "Nombre de jours à prédire", 
                        min_value=1, 
                        max_value=30, 
                        value=7,
                        help="Nombre de jours à prédire à partir de la date de référence"
                    )
                    model_choice = st.selectbox("Modèle IA", ["prophet"], key="model_select")
                    submitted = st.form_submit_button("🚀 Lancer la prédiction", use_container_width=True)
            if submitted:
                with st.spinner("🔮 Prédiction en cours..."):
                    reference_date_str = reference_date.isoformat() if reference_date else None
                    prediction_payload = {
                        "country": country_predict,
                        "days": days_to_predict,
                        "prediction_type": "cases",
                        "model": model_choice,
                        "reference_date": reference_date_str
                    }
                    result = post_with_auth("/predict", prediction_payload)
                if result:
                    st.success("✅ Prédiction terminée !")
                    st.subheader("📊 Résultats de la prédiction")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Pays", country_predict)
                    with col2:
                        st.metric("Date de référence", reference_date.strftime("%d/%m/%Y"))
                    with col3:
                        st.metric("Jours prédits", days_to_predict)
                    st.markdown("**📈 Prédictions détaillées :**")
                    predictions_data = []
                    for i, pred in enumerate(result.get("predictions", []), 1):
                        pred_date = datetime.fromisoformat(pred['date'].replace('Z', '+00:00')).date()
                        predictions_data.append({
                            "Jour": i,
                            "Date prédite": pred_date.strftime("%d/%m/%Y"),
                            "Taux de mortalité (%)": f"{pred['predicted_value']:.2f}".replace('.', ',')
                        })
                    if predictions_data:
                        df_predictions = pd.DataFrame(predictions_data)
                        st.dataframe(df_predictions, use_container_width=True)
                        try:
                            import plotly.express as px
                            fig = px.line(
                                df_predictions, 
                                x="Date prédite", 
                                y="Taux de mortalité (%)",
                                title=f"Évolution prédite des cas COVID-19 - {country_predict}",
                                markers=True
                            )
                            fig.update_layout(
                                xaxis_title="Date", 
                                yaxis_title="Taux de mortalité (%)",
                                plot_bgcolor='black',
                                paper_bgcolor='black',
                                font=dict(color='white'),
                                legend=dict(font=dict(color='white')),
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        except ImportError:
                            st.info("📊 Graphique non disponible (plotly non installé)")
                    else:
                        st.error("❌ Erreur lors de la prédiction")
                else:
                    st.error(t["data_error"])
    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    render_footer() 