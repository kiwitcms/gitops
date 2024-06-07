# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under GNU Affero General Public License v3 or later (AGPLv3+)
# https://www.gnu.org/licenses/agpl-3.0.html

FROM alpine:3.20 as runtime-base

RUN apk --no-cache upgrade && \
    apk --no-cache add github-cli python3 && \
    rm -rf /var/cache/apk/*


FROM runtime-base as builder

RUN apk --no-cache add gcc libffi-dev musl-dev py3-pip python3-dev && \
    rm -rf /var/cache/apk/* && \
    /usr/bin/python3 -m venv /opt/venv && \
    chown -R 1001 /opt/*

ENV PATH=/opt/venv/bin:${PATH} \
    VIRTUAL_ENV=/opt/venv

COPY --chown=1001:root ./app/ /opt/app
RUN find /opt/app/ -type f -name "*.pyc" -delete && \
    pip install --requirement /opt/app/requirements.txt --no-cache-dir


FROM runtime-base
ENV PATH=/opt/venv/bin:${PATH} \
    VIRTUAL_ENV=/opt/venv

COPY --from=builder --chown=1001:root /opt/ /opt

HEALTHCHECK CMD true
USER 1001
ENTRYPOINT ["/opt/app/entrypoint"]
