FROM --platform=$TARGETPLATFORM python:3.11.9-slim-bullseye as builder

# ARG TARGETPLATFORM
# ARG BUILDPLATFORM
# RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM"

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app_root

COPY ./requirements-prod.txt ./requirements.txt

## Install OS dependencies
# build-essential is needed for RPi.GPIO
# libpq-dev, python3-dev is for psycopg2-binary only in Raspberry Pi 1B
## --no-install-recommends,
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


FROM --platform=$TARGETPLATFORM python:3.11.9-slim-bullseye
WORKDIR /app_root
COPY --from=builder /bin /bin
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY ./entrypoint.sh ./
COPY ./proj ./proj

RUN apt-get update && apt-get install -y netcat libpq-dev\
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--pythonpath", "./proj", "proj.wsgi", "--bind", "0.0.0.0:8000"]