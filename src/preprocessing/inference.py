import pandas as pd
import mlflow


class Inference:

    def __init__(
        self, input_data, model_name="sk-learn-logistic-reg-model", model_version=1
    ):
        self.data = self._load_data(input_data)
        self.model = self._load_model(model_name, model_version)

    def _load_data(self, file):
        if isinstance(file, pd.DataFrame):
            return file.copy()
        else:
            return pd.read_csv(file)

    def _load_model(self, model_name, model_version):
        model_uri = f"models:/{model_name}/{model_version}"
        return mlflow.sklearn.load_model(model_uri)

    def predict(self):
        # model já tem pipeline, só chamar predict direto
        return pd.Series(self.model.predict(self.data))
