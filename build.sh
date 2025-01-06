#!/bin/bash

PYTHON_VERSIONS=("3.9" "3.10" "3.11", "3.12")

for version in "${PYTHON_VERSIONS[@]}"; do
  echo "Building image for Python $version..."
  docker build --build-arg PYTHON_VERSION=$version -t imaging-server-kit:$version .
done

echo "Building image for Python 3.9, GPU-compatible..."
docker build -t imaging-server-kit:gpu --file Dockerfile-GPU .