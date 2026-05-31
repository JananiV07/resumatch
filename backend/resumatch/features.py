import re
from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np

from resumatch.skill_matcher import load_skills, find_skills

FEATURE_NAMES = ["semantic_similarity", "skill_overlap", "experience_norm"]
_MAX_YEARS = 20.0
_MODEL_NAME = "all-MiniLM-L6-v2"


@dataclass
class FeatureDetail:
    vector: list[float]
    semantic_similarity: float
    skill_overlap: float
    experience_years: float
    matched_skills: set[str]
    missing_skills: set[str]
    jd_skills: set[str] = field(default_factory=set)


@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(_MODEL_NAME)


def _embed(texts: list[str]) -> np.ndarray:
    return _model().encode(texts, normalize_embeddings=True)


def semantic_similarity(jd_text: str, resume_text: str) -> float:
    if not jd_text.strip() or not resume_text.strip():
        return 0.0
    emb = _embed([jd_text, resume_text])
    sim = float(np.dot(emb[0], emb[1]))
    return max(0.0, min(1.0, sim))


def extract_experience_years(text: str) -> float:
    matches = re.findall(r"(\d{1,2})\s*\+?\s*years?", text.lower())
    if not matches:
        return 0.0
    return float(max(int(m) for m in matches))


def extract_features(jd_text: str, resume_text: str) -> FeatureDetail:
    all_skills = load_skills()
    jd_skills = find_skills(jd_text, all_skills)
    matched = find_skills(resume_text, list(jd_skills)) if jd_skills else set()
    missing = jd_skills - matched
    overlap = (len(matched) / len(jd_skills)) if jd_skills else 0.0

    sim = semantic_similarity(jd_text, resume_text)
    years = extract_experience_years(resume_text)
    exp_norm = min(years, _MAX_YEARS) / _MAX_YEARS

    vector = [sim, overlap, exp_norm]
    return FeatureDetail(
        vector=vector,
        semantic_similarity=sim,
        skill_overlap=overlap,
        experience_years=years,
        matched_skills=matched,
        missing_skills=missing,
        jd_skills=jd_skills,
    )
