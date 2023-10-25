# Python runtime as parent image
FROM python:3.9-slim-buster

# Set working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install packages in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application into the container at /app
COPY . /app

# Expose dev web port 
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "main.py"]