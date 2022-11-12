import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

class User:
    # Данные в столбце timestamp в формате YYYY-MM-DD HH-MM-SS
    # Данные в столбце session_id уникальны в рамках одного пользователя


    def __init__(self, df):
        self.df = df


    def unique_session(self):
        df = self.df
        df = df.sort_values(['customer_id', 'timestamp'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        diff_timestamp = df.groupby(by='customer_id')['timestamp'].diff()
        new_session = (diff_timestamp.isnull()) | \
                      (diff_timestamp > '0 days 00:03:00')
        df['session_id'] = df.loc[new_session, ['customer_id', 'timestamp']] \
            .groupby('customer_id').rank(method='first')
        df['session_id'] = df['session_id'].fillna(method='ffill').astype('int')
        return df
