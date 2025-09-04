# Stage 1: Base build stage
FROM python:3.13-slim AS builder

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Stage 2: Production stage
FROM builder AS production

WORKDIR /app

RUN python manage.py collectstatic --noinput

RUN useradd -m -r appuser && \
   chown -R appuser /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

USER appuser

CMD ["gunicorn", "spk.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3"]