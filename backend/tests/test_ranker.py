import numpy as np
from sklearn.linear_model import LogisticRegression
from resumatch.ranker import Ranker


def _toy_model():
    X = np.array([[0.1, 0.0, 0.0], [0.2, 0.1, 0.1], [0.8, 0.9, 0.8], [0.9, 1.0, 0.9]])
    y = np.array([0, 0, 1, 1])
    return LogisticRegression().fit(X, y)


def test_score_in_range_and_monotonic():
    r = Ranker(_toy_model())
    low = r.score([0.1, 0.0, 0.0])
    high = r.score([0.9, 1.0, 0.9])
    assert 0.0 <= low <= 100.0
    assert 0.0 <= high <= 100.0
    assert high > low


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "ranker.joblib"
    Ranker(_toy_model()).save(str(path))
    loaded = Ranker.load(str(path))
    s = loaded.score([0.5, 0.5, 0.5])
    assert 0.0 <= s <= 100.0
