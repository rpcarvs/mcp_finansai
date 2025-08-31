FROM python:3.13-slim

RUN pip install uv supervisor --no-cache

WORKDIR /app
COPY . /app
RUN mv supervisord.conf /etc/supervisord.conf

RUN uv sync --no-cache && \
    pip cache purge && \
    uv cache clean

EXPOSE 9001

ENTRYPOINT ["supervisord"]