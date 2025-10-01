# syntax=docker/dockerfile:1.9

# --- Base image: minimal Python runtime ---
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
# non-root user for safety
RUN useradd -m -u 10001 appuser

# --- Builder: produce a wheel (.whl) for the package ---
FROM base AS builder
RUN python -m pip install -U pip build wheel
COPY pyproject.toml README.md ./
COPY src/ src/
RUN python -m build --wheel -o /dist

# --- Test stage: install wheel + test deps, run pytest during build ---
FROM base AS test
RUN python -m pip install -U pip
COPY --from=builder /dist/ /tmp/dist/
RUN python -m pip install /tmp/dist/*.whl pytest pytest-cov
COPY tests/ tests/
# If tests fail, this layer fails and the build stops
RUN pytest -q

# --- Release image: lean runtime with entrypoint to CLI ---
FROM base AS release
COPY --from=builder /dist/ /tmp/dist/
RUN python -m pip install --no-cache-dir /tmp/dist/*.whl && rm -rf /root/.cache
USER appuser
# Default workdir where users will mount files
WORKDIR /work
# csv2json is provided by [project.scripts] in pyproject.toml
ENTRYPOINT ["csv2json"]
