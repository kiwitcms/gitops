FROM alpine:3.19

RUN apk --no-cache upgrade && \
    apk --no-cache add github-cli py3-pip && \
    rm -rf /var/cache/apk/*
RUN /usr/bin/python3 -m venv /opt/venv && \
    mkdir /opt/app && \
    chown -R 1001 /opt/*
COPY --chown=1001:root ./app/* /opt/app/

ENV PATH=/opt/venv/bin:${PATH} \
    VIRTUAL_ENV=/opt/venv
HEALTHCHECK CMD true
USER 1001

RUN pip install --requirement /opt/app/requirements.txt --no-cache-dir

ENTRYPOINT ["/opt/app/entrypoint"]
