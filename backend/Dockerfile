# ResuMatch backend — FastAPI + ML pipeline
FROM python:3.11-slim

WORKDIR /app
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/app/.hf_cache

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Train the ranker and pre-cache the embedding model into the image
# so the first request doesn't trigger a download.
RUN python -m scripts.train \
 && python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

EXPOSE 8000
CMD ["uvicorn", "resumatch.api:app", "--host", "0.0.0.0", "--port", "8000"]
