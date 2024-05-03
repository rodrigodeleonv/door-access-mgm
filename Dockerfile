FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app_root

# RUN mkdir -p /var/door-access-mgm/static/
COPY ./static /static
COPY ./requirements-prod.txt ./requirements.txt
COPY ./entrypoint.sh ./

RUN apt-get update && apt-get install -y build-essential netcat

RUN pip install --no-cache-dir -r requirements.txt

COPY ./proj ./proj

# Give problems with GPIO in build phase
# RUN python proj/manage.py collectstatic --noinput

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--pythonpath", "./proj", "proj.wsgi", "--bind", "0.0.0.0:8000"]
EXPOSE 8000