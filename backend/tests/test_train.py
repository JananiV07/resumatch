import numpy as np
from scripts.train import synth_label, build_dataset, train_model
from resumatch.ranker import Ranker


def test_synth_label_rules():
    assert synth_label(0.8, 1.0, 0.5) == 1
    assert synth_label(0.1, 0.0, 0.0) == 0


def test_build_dataset_shape():
    X, y = build_dataset(n=200, seed=0)
    assert X.shape == (200, 3)
    assert set(np.unique(y)).issubset({0, 1})
    assert 0 < y.mean() < 1


def test_train_model_returns_ranker(tmp_path):
    path = tmp_path / "ranker.joblib"
    ranker, metrics = train_model(n=400, seed=0, out_path=str(path))
    assert isinstance(ranker, Ranker)
    assert metrics["roc_auc"] > 0.8
    assert path.exists()
