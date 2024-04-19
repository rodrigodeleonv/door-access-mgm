FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app_root

RUN apt-get update && apt-get install -y build-essential

COPY ./requirements-prod.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./proj ./proj

CMD ["gunicorn", "--pythonpath", "./proj proj.wsgi", "--bind", "0.0.0.0:8000"]
EXPOSE 8000