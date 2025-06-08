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

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


class ModelTrainer:

    def __init__(self, input, model=None, use_mlflow=True):
        self.data = self._load_data(input)
        self.model = model if model else LogisticRegression()
        self.use_mlflow = use_mlflow
        self.label = "Personality"

        self.numeric_columns = self.data.select_dtypes(
            include="number"
        ).columns.to_list()

        self.categoric_columns = self.data.select_dtypes(
            include="object"
        ).columns.to_list()
        self.categoric_columns.remove(self.label)

    def _load_data(self, file):
        return pd.read_csv(file)

    def _split_label_and_features(self, data: pd.DataFrame):
        label = data[[self.label]]
        features = data.drop(columns=self.label)

        return features, label

    def _numeric_preprocessing(self):
        return Pipeline(
            steps=[
                ("fill_na", KNNImputer(n_neighbors=3)),
                ("scale_num", RobustScaler()),
            ]
        )

    def _categoric_preprocessing(self):
        return Pipeline(
            steps=[
                ("one_hot", OneHotEncoder(drop="if_binary")),
            ]
        )

    def _label_preprocessing(self, label: pd.Series):
        le = LabelEncoder()
        return le.fit_transform(label)

    def _feature_preprocessing(self, data):

        numeric_preprocessor = self._numeric_preprocessing()
        categoric_preprocessor = self._categoric_preprocessing()

        feature_preprocessing = ColumnTransformer(
            transformers=[
                ("cat", categoric_preprocessor, self.categoric_columns),
                (
                    "num",
                    numeric_preprocessor,
                    make_column_selector(dtype_include="number"),
                ),
            ]
        )

        return feature_preprocessing.fit_transform(data)

    def _preprocess(self):

        def remove_categorical_nas(X: pd.DataFrame, columns) -> pd.DataFrame:
            return X.dropna(subset=columns)

        preprocessing = Pipeline(
            steps=[
                (
                    "drop_cat_nas",
                    FunctionTransformer(
                        remove_categorical_nas,
                        kw_args={"columns": self.categoric_columns},
                    ),
                ),
            ]
        )

        return preprocessing.fit_transform(self.data)

    def _split_data(self, features, label, test_size=0.3):
        return train_test_split(features, label, test_size=test_size)

    def _train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def _evaluate(self, X_test, y_test):
        return self.model.score(X_test, y_test)

    def _save_model():
        pass

    def run_pipeline(self, saveModel=False):
        clean_data = self._preprocess()

        features, label = self._split_label_and_features(clean_data)

        clean_label = self._label_preprocessing(label)
        clean_features = self._feature_preprocessing(features)

        X_train, X_test, y_train, y_test = self._split_data(clean_features, clean_label)

        self._train(X_train, y_train)
        score = self._evaluate(X_test, y_test)

        if saveModel:
            self._save_model()

        return score
