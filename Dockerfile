# Use a slim Python base image (adjust version if needed)
FROM python:3.10-slim

# Install ffmpeg (adapt package manager for your OS if needed)
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Set working directory
WORKDIR /app/

# Install Python dependencies (assuming 'requirements.txt' is modified to address 'tgcalls')
RUN pip install --no-cache-dir -U -r requirements.txt

# Multi-stage build (optional for production):

# Stage 1: Install dependencies
FROM python:3.10-slim AS builder
WORKDIR /app/
COPY requirements.txt .
RUN pip install --no-cache-dir -U -r requirements.txt

# Stage 2: Copy application (smaller image)
FROM builder
COPY . .

# Entrypoint (adjust based on your project's startup script)
CMD ["bash", "start"]