import pytest
import ml_model
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

def test_predict_with_prophet_basic():
    # Données factices simulant un historique minimal
    df = pd.DataFrame({
        'ds': pd.date_range('2020-01-01', periods=10),
        'cases': range(10)
    })
    df['cases_log'] = df['cases'].apply(lambda x: 0 if x == 0 else x)

    # Mock du modèle Prophet
    fake_forecast = pd.DataFrame({
        'yhat': [1.0, 2.0, 3.0]
    })
    fake_model = MagicMock()
    fake_model.make_future_dataframe.return_value = df[['ds']].copy()
    fake_model.predict.return_value = fake_forecast

    with patch('ml_model.load_prophet', return_value=fake_model):
        result = ml_model.predict_with_prophet(df, days=3)
        assert len(result) == 3
        assert 'yhat' in result.columns 