FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/
ADD . /app
WORKDIR /app
RUN uv sync --locked
CMD ["uv", "run", "main.py"]
