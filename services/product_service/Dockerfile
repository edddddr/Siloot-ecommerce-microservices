FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/ ./requirements/
# RUN pip install --no-cache-dir -r requirements/base.txt
# Change this line in your Dockerfiles:
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements/base.txt

COPY . .

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8001"]