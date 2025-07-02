import pandas as pd
from sqlalchemy.orm import Session
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'covid_cleaned.csv')

def import_data_from_csv(db: Session):
    try:
        df = pd.read_csv(CSV_PATH)

        df['date'] = pd.to_datetime(df['date'])
        df['cases'] = pd.to_numeric(df['cases'], errors='coerce').fillna(0).astype(int)
        df['deaths'] = pd.to_numeric(df['deaths'], errors='coerce').fillna(0).astype(int)
        df['recovered'] = pd.to_numeric(df['recovered'], errors='coerce').fillna(0).astype(int)

        df = df.sort_values(by=['country', 'date'])

        df['new_cases'] = df.groupby('country')['cases'].diff().fillna(0).astype(int)
        df['new_deaths'] = df.groupby('country')['deaths'].diff().fillna(0).astype(int)
        df['new_recovered'] = df.groupby('country')['recovered'].diff().fillna(0).astype(int)

        df['new_cases'] = df['new_cases'].apply(lambda x: max(0, x))
        df['new_deaths'] = df['new_deaths'].apply(lambda x: max(0, x))
        df['new_recovered'] = df['new_recovered'].apply(lambda x: max(0, x))

        db.query(Data).delete()
        db.commit()

        for _, row in df.iterrows():
            data_record = Data(
                country=row['country'],
                date=row['date'],
                confirmed=row['cases'],
                deaths=row['deaths'],
                recovered=row['recovered'],
                new_cases=row['new_cases'],
                new_deaths=row['new_deaths'],
                new_recovered=row['new_recovered']
            )
            db.add(data_record)
        
        db.commit()
        return {"status": "success", "message": f"{len(df)} records imported successfully."}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)} 