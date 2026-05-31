import io
import pytest
from fastapi.testclient import TestClient
import resumatch.api as api
from resumatch.features import FeatureDetail
from resumatch.parser import ParseError


class _FakeRanker:
    def score(self, features):
        return round(features[0] * 100, 1)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(api, "_RANKER", _FakeRanker())

    def fake_parse(filename, data):
        if filename == "bad.pdf":
            raise ParseError("corrupt")
        return data.decode("utf-8")

    def fake_extract(jd, resume):
        sim = float(resume.split("sim=")[1]) if "sim=" in resume else 0.0
        return FeatureDetail(
            vector=[sim, 0.0, 0.0], semantic_similarity=sim, skill_overlap=0.0,
            experience_years=0.0, matched_skills=set(), missing_skills=set(),
            jd_skills=set(),
        )

    monkeypatch.setattr(api, "parse", fake_parse)
    monkeypatch.setattr(api, "extract_features", fake_extract)
    return TestClient(api.app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ranker_loaded"] is True


def test_score_ranks_by_score_desc(client):
    files = [
        ("resumes", ("a.txt", io.BytesIO(b"sim=0.3"), "text/plain")),
        ("resumes", ("b.txt", io.BytesIO(b"sim=0.9"), "text/plain")),
    ]
    r = client.post("/score", data={"jd_text": "python role"}, files=files)
    assert r.status_code == 200
    body = r.json()
    ranks = [c["filename"] for c in body["candidates"]]
    assert ranks == ["b.txt", "a.txt"]
    assert body["candidates"][0]["score"] == 90.0
    assert body["candidates"][0]["tier"]
    assert "match" in body["candidates"][0]["explanation"].lower()


def test_score_collects_warnings_for_bad_file(client):
    files = [
        ("resumes", ("good.txt", io.BytesIO(b"sim=0.5"), "text/plain")),
        ("resumes", ("bad.pdf", io.BytesIO(b"x"), "application/pdf")),
    ]
    r = client.post("/score", data={"jd_text": "python role"}, files=files)
    assert r.status_code == 200
    body = r.json()
    assert len(body["candidates"]) == 1
    assert any("bad.pdf" in w for w in body["warnings"])


def test_empty_jd_returns_400(client):
    files = [("resumes", ("a.txt", io.BytesIO(b"sim=0.5"), "text/plain"))]
    r = client.post("/score", data={"jd_text": "   "}, files=files)
    assert r.status_code == 400


def test_no_resumes_returns_400(client):
    r = client.post("/score", data={"jd_text": "python"}, files=[])
    assert r.status_code == 400
