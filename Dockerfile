# Use a Python base image with conda
FROM continuumio/anaconda3

# Set the working directory
WORKDIR /app

# Set the API_KEY environment variable
ENV API_KEY="my-api-key"

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Create a conda environment and activate it
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# # Define an entrypoint command to run the tests
ENTRYPOINT ["python", "-m", "unittest", "discover"]
