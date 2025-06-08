import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    RobustScaler,
    FunctionTransformer,
    LabelEncoder,
)
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import KNNImputer
from sklearn.linear_model import LogisticRegression
import mlflow
import mlflow.sklearn


class ModelTrainer:

    def __init__(self, input_data, model=None, use_mlflow=True):
        self.data = self._load_data(input_data)
        self.model = model if model else LogisticRegression()
        self.use_mlflow = use_mlflow
        self.label = "Personality"

        self.numeric_columns = self.data.select_dtypes(
            include="number"
        ).columns.tolist()
        self.categoric_columns = self.data.select_dtypes(
            include="object"
        ).columns.tolist()
        if self.label in self.categoric_columns:
            self.categoric_columns.remove(self.label)

    def _load_data(self, file):
        if isinstance(file, pd.DataFrame):
            return file.copy()
        else:
            return pd.read_csv(file)

    def _split_label_and_features(self, data):
        return data.drop(columns=self.label), data[self.label]

    def _numeric_preprocessing(self):
        return Pipeline(
            [("imputer", KNNImputer(n_neighbors=3)), ("scaler", RobustScaler())]
        )

    def _categoric_preprocessing(self):
        return Pipeline(
            [("onehot", OneHotEncoder(handle_unknown="ignore", drop="if_binary"))]
        )

    def _validate_no_nas(self, X):
        if X.isnull().any().any():
            raise ValueError("Dados contêm valores nulos.")
        return X

    def _label_preprocessing(self, y):
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        self.label_encoder = le  # salvar para possível uso depois
        return y_encoded

    def _build_pipeline(self):
        numeric_pipe = self._numeric_preprocessing()
        categoric_pipe = self._categoric_preprocessing()

        feature_processing = ColumnTransformer(
            transformers=[
                ("categorical", categoric_pipe, self.categoric_columns),
                ("numeric", numeric_pipe, make_column_selector(dtype_include="number")),
            ],
            remainder="drop",
            sparse_threshold=0,
        )

        # O FunctionTransformer para validar NaNs antes do processamento, mas não altera dados
        preprocessing = Pipeline(
            [
                ("validate_no_nas", FunctionTransformer(self._validate_no_nas)),
                ("feature_processing", feature_processing),
            ]
        )

        full_pipeline = Pipeline(
            [("preprocessing", preprocessing), ("model", self.model)]
        )

        return full_pipeline

    def _split_data(self, X, y, test_size=0.3, random_state=42):
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    def _save_model(self, pipeline, X_train):
        with mlflow.start_run(run_name="treino-logistic"):
            mlflow.sklearn.log_model(
                sk_model=pipeline,
                artifact_path="full_pipeline",
                input_example=X_train.head(5),
                registered_model_name="sk-learn-logistic-reg-model",
            )

    def run_pipeline(self, save_model=False):
        X, y = self._split_label_and_features(self.data)
        pipeline = self._build_pipeline()
        y_encoded = self._label_preprocessing(y)

        X_train, X_test, y_train, y_test = self._split_data(X, y_encoded)
        pipeline.fit(X_train, y_train)
        score = pipeline.score(X_test, y_test)

        if save_model and self.use_mlflow:
            self._save_model(pipeline, X_train)

        return score
