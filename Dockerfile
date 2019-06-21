ARG DOCKER_VERSION=18.09.5
FROM docker:${DOCKER_VERSION} AS docker-cli

FROM alpine

COPY --from=docker-cli  /usr/local/bin/docker   /usr/local/bin/docker
COPY robot-entrypoint.sh /usr/local/bin/

RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    \
    echo "**** install robotframework and dependencies ****" && \
    python3 -m pip install robotframework && \
    pip3 install docker  &&  \
    pip3 install pytz  

ENTRYPOINT ["sh", "/usr/local/bin/robot-entrypoint.sh"]