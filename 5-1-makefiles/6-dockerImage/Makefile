# Image name and tag
IMAGE = hello-docker
TAG = latest

# Full image reference
FULL_IMAGE = $(IMAGE):$(TAG)

# Phony targets
.PHONY: all build run clean

# Default target
all: build

# Build the Docker image
build:
	docker build -t $(FULL_IMAGE) .

# Run the container
run:
	docker run --rm $(FULL_IMAGE)

# Remove the image
clean:
	docker image rm $(FULL_IMAGE)

