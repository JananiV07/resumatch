from resumatch.explain import score_tier, build_explanation


def test_score_tier_bands():
    assert score_tier(90) == "Strong match"
    assert score_tier(60) == "Moderate match"
    assert score_tier(30) == "Weak match"
    assert score_tier(5) == "Poor match"


def test_explanation_full_match():
    text = build_explanation(99.0, 0.84, {"python", "docker"}, set(), 6)
    assert "Strong match (99/100)." in text
    assert "highly relevant" in text
    assert "All 2 required skills are present" in text
    assert "6 years of experience" in text


def test_explanation_partial_and_missing():
    text = build_explanation(40.0, 0.4, {"python"}, {"aws", "kubernetes"}, 0)
    assert "Weak match (40/100)." in text
    assert "somewhat relevant" in text
    assert "1 of 3 required skills present" in text
    assert "missing aws, kubernetes" in text
    assert "No explicit years of experience" in text


def test_explanation_no_jd_skills():
    text = build_explanation(50.0, 0.3, set(), set(), 2)
    assert "No specific skills were identified" in text
    assert "low semantic relevance" in text
