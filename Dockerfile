# Use the Miniconda base image
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /app

# Copy the environment.yml file into the container
COPY environment.yml .

# Install Python 3.12 and create the conda environment
RUN conda install -y python=3.12 && \
    conda env create -f environment.yml

# Activate the environment and set it as the default
SHELL ["conda", "run", "-n", "rag-test", "/bin/bash", "-c"]

# Copy the rest of your application code into the container
COPY . .

# Command to run your application
CMD ["conda", "run", "-n", "rag-test", "python", "-m", "app.main"]