import pytest
from resumatch.skill_matcher import load_skills, find_skills
from resumatch.features import (
    extract_features,
    FeatureDetail,
    FEATURE_NAMES,
    extract_experience_years,
)


def test_load_skills_returns_list():
    skills = load_skills()
    assert "python" in skills
    assert len(skills) > 20


def test_find_skills_exact():
    found = find_skills("Experienced in Python and Docker.", ["python", "docker", "go"])
    assert found == {"python", "docker"}


def test_find_skills_case_insensitive_and_wordboundary():
    found = find_skills("We are going to use React heavily.", ["go", "react"])
    assert found == {"react"}


def test_find_skills_fuzzy_typo():
    found = find_skills("Deployed on kubernets clusters.", ["kubernetes"])
    assert found == {"kubernetes"}


def test_extract_experience_years():
    assert extract_experience_years("I have 7 years of experience") == 7.0
    assert extract_experience_years("3+ years in backend") == 3.0
    assert extract_experience_years("no numbers here") == 0.0


def test_extract_features_shape_and_detail():
    jd = "Looking for a Python engineer with Docker and 5 years experience."
    resume = "Python developer, used Docker daily, 6 years of experience."
    detail = extract_features(jd, resume)
    assert isinstance(detail, FeatureDetail)
    assert len(detail.vector) == len(FEATURE_NAMES)
    assert 0.0 <= detail.vector[0] <= 1.0
    assert detail.skill_overlap == 1.0
    assert detail.matched_skills == {"python", "docker"}
    assert detail.missing_skills == set()
    assert detail.experience_years == 6.0


def test_extract_features_partial_overlap():
    jd = "Need Python, Kubernetes, and AWS."
    resume = "I know Python only."
    detail = extract_features(jd, resume)
    assert detail.skill_overlap == pytest.approx(1 / 3, abs=0.01)
    assert "python" in detail.matched_skills
    assert {"kubernetes", "aws"} <= detail.missing_skills
