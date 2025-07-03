import numpy as np
import pandas as pd
import pickle

# Chemin du modèle Prophet
PROPHET_PATH = '/app/models_and_results/prophet_model.pkl'
prophet_model = None


# Chargement du modèle Prophet
def load_prophet():
    global prophet_model
    if prophet_model is None:
        with open(PROPHET_PATH, 'rb') as f:
            prophet_model = pickle.load(f)
    return prophet_model


# Prédiction avec Prophet
def predict_with_prophet(df, days):
    model = load_prophet()

    # Préparer les données pour Prophet
    if 'ds' not in df.columns:
        if 'date' in df.columns:
            df = df.rename(columns={'date': 'ds'})
        else:
            raise ValueError("DataFrame must contain 'date' or 'ds' column")

    # Créer 'cases_log' à partir de 'cases' ou 'confirmed'
    if 'cases_log' not in df.columns:
        if 'cases' in df.columns:
            df['cases_log'] = np.log1p(df['cases'])
        elif 'confirmed' in df.columns:
            df['cases_log'] = np.log1p(df['confirmed'])
        else:
            raise ValueError("""
                             DataFrame must contain 'cases' or
                             'confirmed' column
                             """)

    # S'assurer que les types de données sont corrects
    df['ds'] = pd.to_datetime(df['ds'])
    df['cases_log'] = pd.to_numeric(df['cases_log'], errors='coerce')

    # Vérifier qu'il n'y a pas de NaN
    # dans cases_log pour les données historiques
    if df['cases_log'].isna().any():
        print("Warning: NaN values found in cases_log, filling with 0")
        df['cases_log'] = df['cases_log'].fillna(0)

    print("df[['ds', 'cases_log']].head():\n", df[['ds', 'cases_log']].head())
    print("df[['ds', 'cases_log']].tail():\n", df[['ds', 'cases_log']].tail())

    # Créer le DataFrame futur
    future = model.make_future_dataframe(periods=days)
    future['ds'] = pd.to_datetime(future['ds'])

    # Merger les données historiques avec le futur
    future = future.merge(df[['ds', 'cases_log']], on='ds', how='left')

    # Pour les dates futures, projeter les valeurs de cases_log
    # Utiliser la dernière valeur connue ou une tendance simple
    last_known_value = df['cases_log'].iloc[-1]
    if pd.isna(last_known_value):
        last_known_value = 0

    # Remplir les NaN avec la dernière valeur connue
    future['cases_log'] = future['cases_log'].fillna(last_known_value)

    print(f"future.head(10):\n{future.head(10)}")
    print(f"future.tail(10):\n{future.tail(10)}")

    # Vérifier qu'il n'y a pas de NaN avant la prédiction
    if future['cases_log'].isna().any():
        print("Error: Still have NaN values in cases_log")
        print("NaN positions:", future[future['cases_log'].isna()])
        raise ValueError("Cannot have NaN values in regressor for Prophet")

    forecast = model.predict(future)
    return forecast.tail(days)


# Dispatch unique (ne garde que Prophet)
def predict_dispatch(model_name, df, days):
    return predict_with_prophet(df, days)
