from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from resumatch.parser import parse, ParseError
from resumatch.features import extract_features
from resumatch.ranker import Ranker
from resumatch.explain import score_tier, build_explanation

_MODEL_PATH = Path(__file__).resolve().parent.parent / "ranker.joblib"

try:
    _RANKER = Ranker.load(str(_MODEL_PATH))
except Exception:
    _RANKER = None


class Candidate(BaseModel):
    filename: str
    score: float
    tier: str
    explanation: str
    matched_skills: list[str]
    missing_skills: list[str]
    experience_years: float
    semantic_similarity: float
    skill_overlap: float


class ScoreResponse(BaseModel):
    candidates: list[Candidate]
    warnings: list[str]


app = FastAPI(title="ResuMatch")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "ranker_loaded": _RANKER is not None}


@app.post("/score", response_model=ScoreResponse)
async def score(jd_text: str = Form(...), resumes: list[UploadFile] = File(default=[])):
    if not jd_text.strip():
        raise HTTPException(status_code=400, detail="jd_text must not be empty")
    if not resumes:
        raise HTTPException(status_code=400, detail="at least one resume is required")
    if _RANKER is None:
        raise HTTPException(status_code=503, detail="ranker not loaded; run scripts.train")

    candidates: list[Candidate] = []
    warnings: list[str] = []
    for f in resumes:
        data = await f.read()
        try:
            text = parse(f.filename, data)
        except ParseError as e:
            warnings.append(f"Skipped {f.filename}: {e}")
            continue
        detail = extract_features(jd_text, text)
        s = _RANKER.score(detail.vector)
        candidates.append(Candidate(
            filename=f.filename,
            score=s,
            tier=score_tier(s),
            explanation=build_explanation(
                s, detail.semantic_similarity, detail.matched_skills,
                detail.missing_skills, detail.experience_years,
            ),
            matched_skills=sorted(detail.matched_skills),
            missing_skills=sorted(detail.missing_skills),
            experience_years=detail.experience_years,
            semantic_similarity=round(detail.semantic_similarity, 3),
            skill_overlap=round(detail.skill_overlap, 3),
        ))

    candidates.sort(key=lambda c: c.score, reverse=True)
    return ScoreResponse(candidates=candidates, warnings=warnings)
