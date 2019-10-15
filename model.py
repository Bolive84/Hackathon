import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import catboost as cb
from sklearn.pipeline import make_pipeline

import pickle

df = pd.read_csv("/home/nthock/Documents/DSI/notes/hackathon/ted/ted_main.csv")

features = ['description','duration','languages','published_date','tags','title']
target = 'views'

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
