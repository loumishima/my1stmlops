import pytest
import pandas as pd
from src.preprocessing.training import ModelTrainer
from src.preprocessing.inference import Inference


@pytest.fixture
def model():
    return ModelTrainer("data/personality_dataset.csv")


def test_pipeline(model):
    # Deve falhar se dados tiverem NAs
    with pytest.raises(ValueError):
        model.run_pipeline(save_model=False)


def test_success_pipeline(model):
    model.data = model.data.dropna()
    score = model.run_pipeline(save_model=True)
    assert isinstance(score, float)


def test_inference():
    inf = Inference("data/personality_dataset.csv", model_version=3)
    inf.data.dropna(inplace=True)
    preds = inf.predict()
    assert isinstance(preds, pd.Series)
