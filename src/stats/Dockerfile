FROM alpine:3.6

RUN apk add --no-cache python py-psycopg2 py-requests py-pip && \
    pip install prometheus_client && \
    apk del py-pip

COPY src/stats /stats
COPY src/pyinfraboxutils /pyinfraboxutils

ENV PYTHONPATH=/

CMD python stats/stats.py
