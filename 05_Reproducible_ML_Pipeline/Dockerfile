# Reproducible environment for Deliverable 05 (same Python and library versions as results/).
FROM python:3.13.13-slim

ENV PYTHONHASHSEED=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stranger test: rebuild the data from the pinned Hub revision, check its MD5,
# re-run all seeds and compare against the committed results.
CMD ["python", "src/verify_reproduction.py", "--full"]
