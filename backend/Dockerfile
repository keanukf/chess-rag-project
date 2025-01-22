# Use Miniconda as the base image
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /backend

# Copy the application code
COPY . .

# Create the Conda environment
RUN conda env create -f environment.yml

# Activate the Conda environment for subsequent RUN instructions
SHELL ["conda", "run", "-n", "chessbot", "/bin/bash", "-c"]

# Set Flask environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=main.py

# Expose the Flask port
EXPOSE 8080

# Use ENTRYPOINT to activate conda first, then CMD to run the app
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "chessbot"]
CMD ["python", "-m", "main"]