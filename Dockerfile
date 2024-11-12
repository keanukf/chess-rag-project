# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install system-level dependencies (add any additional necessary packages here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy only the requirements file initially to leverage Docker caching
COPY requirements.txt .

# Upgrade pip and install dependencies separately to cache them effectively
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --default-timeout=300 -i https://pypi.org/simple -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variable for Flask
ENV FLASK_ENV=production
ENV FLASK_APP=app/main.py

# Expose port 8080 for Google Cloud Run
EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
