FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/app/app:/app/shared"

WORKDIR /app

COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/base.txt

COPY . .

WORKDIR /app/app

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]