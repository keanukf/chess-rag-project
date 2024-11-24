# Stage 1: Build stage
FROM python:3.12-slim AS builder

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy only the requirements file initially to leverage Docker caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --default-timeout=300 -r requirements.txt

# Stage 2: Production stage
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the rest of the application code into the container
COPY . .

# Set environment variable for Flask
ENV FLASK_ENV=production
ENV FLASK_APP=app/main.py

# Expose port 8080 for Google Cloud Run
EXPOSE 8080

CMD ["python", "-m", "app.main"]