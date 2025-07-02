
# covid_model.py

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os

def load_data(path, country="France"):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df_country = df[df["country"] == country].copy()
    df_country["target"] = df_country["deaths"].shift(-1)
    df_model = df_country.dropna()
    return df_model

def preprocess_and_train(df_model):
    num_features = ['deaths', 'recovered', 'active', 'cases']
    cat_features = ['day_of_week', 'is_weekend']

    X = df_model[num_features + cat_features]
    y = df_model["target"]

    preprocessor = ColumnTransformer([
        ('num', MinMaxScaler(), num_features),
        ('cat', OneHotEncoder(), cat_features)
    ])

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=42))
    ])

    param_grid = {
        'regressor__n_estimators': [50, 100],
        'regressor__max_depth': [5, 10, None],
    }

    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring='neg_mean_absolute_error',
        cv=3,
        verbose=2,
        n_jobs=-1
    )

    grid_search.fit(X, y)

    print("âœ… Best parameters:", grid_search.best_params_)

    y_pred = grid_search.predict(X)
    mae = mean_absolute_error(y, y_pred)
    rmse = mean_squared_error(y, y_pred, squared=False)
    print(f"ðŸ“Š MAE: {mae:.2f}, RMSE: {rmse:.2f}")

    return grid_search.best_estimator_

def save_model(model, filename="covid_rf_model.pkl"):
    joblib.dump(model, filename)
    print(f"âœ… ModÃ¨le sauvegardÃ© dans {filename}")

if __name__ == "__main__":
    # Adapter le chemin selon votre organisation
    data_path = "./Data/covid_cleaned.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Fichier non trouvÃ© : {data_path}")

    df_model = load_data(data_path)
    model = preprocess_and_train(df_model)
    save_model(model)
