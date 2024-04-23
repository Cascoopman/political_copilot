# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables
# TODO: Add your GCP_PROJECT_NAME and GCP_INDEX_ENDPOINT
ENV PORT=8080
ENV GCP_PROJECT_NAME=//
ENV GCP_INDEX_ENDPOINT=//

# Set the working directory inside the container
WORKDIR /app

# Install the required Python packages
COPY requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY src/ .

# Run the FastAPI application when the container starts
CMD ["python", "backend.py"]