import joblib
import numpy as np


class Ranker:
    """Wraps a fitted scikit-learn classifier; maps features -> 0-100 score."""

    def __init__(self, model):
        self.model = model

    def score(self, features: list[float]) -> float:
        x = np.asarray(features, dtype=float).reshape(1, -1)
        prob = float(self.model.predict_proba(x)[0][1])
        return round(prob * 100.0, 1)

    def save(self, path: str) -> None:
        joblib.dump(self.model, path)

    @classmethod
    def load(cls, path: str) -> "Ranker":
        return cls(joblib.load(path))
