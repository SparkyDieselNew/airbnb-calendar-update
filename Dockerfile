# Use an official Python runtime as a parent image
#FROM python:3.6.4-alpine3.7
FROM python:3.6.4-slim


# Install any needed packages specified in requirements.txt
WORKDIR /tmp/
COPY /docker/additional_packages.txt .
RUN pip install -r additional_packages.txt
RUN pip install --upgrade google-api-python-client

# Create and set the working directory
RUN mkdir -p /src/my_app
WORKDIR /src/my_app

# Make ports available to the world outside this container
EXPOSE 9999
