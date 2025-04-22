FROM ubuntu:22.04

RUN apt-get update && apt-get install -y git bash

WORKDIR /app
COPY . .

# Grab the latest Git tag (if available)
RUN echo "VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo 'v0.0.0')" > /app/version.env

# Final run command
CMD bash -c ". /app/version.env && echo Running version: \$VERSION"
