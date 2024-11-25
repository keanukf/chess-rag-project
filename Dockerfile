FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy environment.yml from the root directory to the app folder in the container
COPY environment.yml /app/environment.yml

# Create the Conda environment
RUN conda env create -f /app/environment.yml

# Activate the Conda environment and ensure it’s active for subsequent steps
SHELL ["conda", "run", "-n", "chess-rag-env", "/bin/bash", "-c"]

# Set Flask environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=app/main.py

# Expose the Flask port
EXPOSE 8080

# Copy the application code from the root directory to the container
COPY . /app

# Final command to run the Flask app using the Conda environment
CMD ["conda", "run", "-n", "chess-rag-env", "python", "-m", "app.main"]