# Stage 1: Base build stage
FROM python:3.13-slim AS builder

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt /app/

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     pkg-config \
#     default-libmysqlclient-dev \
#     python3-dev \
#     # Clean up apt cache to keep image size small
#     && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app

RUN mkdir -p /app/staticfiles && chown -R appuser /app/staticfiles
RUN mkdir -p /app/media && chown -R appuser /app/media

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY --chown=appuser:appuser . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

USER appuser

EXPOSE 8080

# CMD ["gunicorn", "spk.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]