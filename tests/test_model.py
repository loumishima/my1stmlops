import pytest
from src.preprocessing.training import ModelTrainer


@pytest.fixture
def model():
    return ModelTrainer("data/personality_dataset.csv")


def test_pipeline(model):
    result = model.run_pipeline(saveModel=False)

    assert isinstance(result, float)
