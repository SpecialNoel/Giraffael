# syntax=docker/dockerfile:1

# server.Dockerfile
# The Dockerfile used to define Docker Image for server-related stuffs

# - References on Dockerfile commands:
# ARG: specifies build-time variables to be used
# CMD: specifies the default commands
# COPY: copies files and directories
# ENV: sets environmental variables
# EXPOSE: describes which ports this application is listening on
# FROM: creates a new build stage from a base image
# RUN: executes build commands
# USER: set user and group ID

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

WORKDIR /server

RUN echo "PWD:" && pwd && echo "FILES:" && ls -la

COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/src ./src

RUN echo "PWD:" && pwd && echo "FILES:" && ls -la

# Switch to the non-privileged user to run the application.
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
