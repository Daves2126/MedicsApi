# Stage 1: Build the virtual environment
FROM python:3.13.6-alpine3.22 as builder

RUN pip install uv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv pip install --no-cache --requirement pyproject.toml

# Stage 2: Runtime
FROM python:3.13.6-alpine3.22

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
