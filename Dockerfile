# syntax=docker/dockerfile:1

# use python 3.13.2-slim as the base image
FROM python:3.13.2-slim

# set working directory
WORKDIR /app

# prevents python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
# keeps python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering
    PYTHONUNBUFFERED=1

# create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    botuser

# copy only requirements and install first (uses caching)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

# copy the rest of the project files
COPY . .

# switch to the non-privileged user to run the application
USER botuser

# run the application
CMD ["python", "bot.py"]
