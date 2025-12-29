# Builder stage: install the dependencies in a virtual environment
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# Runtime stage
FROM python:3.12-slim

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LOCAL_STORAGE_PATH=/home/app/data/uploads

# Create a group and user
RUN groupadd -g 10999 app && useradd -r -u 10999 -g app -d /home/app app

WORKDIR /home/app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app src ./src
COPY --chown=app:app main.py worker.py entrypoint.sh ./
RUN chmod +x entrypoint.sh && mkdir -p data/uploads && chown -R app:app data

# Run as the unprivileged user
USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=3)" || exit 1

# `api` (default) or `worker`
ENTRYPOINT ["./entrypoint.sh"]
CMD ["api"]
