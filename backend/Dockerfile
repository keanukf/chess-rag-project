FROM continuumio/miniconda3

# Set working directory
WORKDIR /backend

# Copy the environment file and create the Conda environment
COPY environment.yml environment.yml
RUN conda env create -f environment.yml

# Activate the Conda environment and ensure it's active for subsequent steps
SHELL ["conda", "run", "-n", "chessbot", "/bin/bash", "-c"]

# Set Flask environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=main.py

# Expose the Flask port
EXPOSE 8080

# Copy the application code from the root directory to the container
COPY . .

# Set the environment variable for the database
ENV DATABASE_URL=sqlite:///data/chess_rag.db

# Final command to run the Flask app using the Conda environment
CMD ["conda", "run", "-n", "chessbot", "python", "-m", "main"]