FROM python:3.11.9-slim-bullseye as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app_root

COPY ./requirements-prod.txt ./requirements.txt

# build-essential for RPi.GPIO
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential netcat \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


FROM python:3.11.9-slim-bullseye
WORKDIR /app_root
COPY --from=builder /bin /bin
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY ./entrypoint.sh ./
COPY ./proj ./proj

RUN apt-get update && apt-get install -y netcat

# RUN useradd -m myuser
# USER myuser

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--pythonpath", "./proj", "proj.wsgi", "--bind", "0.0.0.0:8000"]