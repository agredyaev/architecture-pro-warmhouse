# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Install newman globally
RUN npm install -g newman

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Set the working directory
WORKDIR /app

# Install Python libraries in a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install grpcio-tools pika pytest requests

# Copy proto files and generate python code
COPY proto/ /app/proto/
RUN python3 -m grpc_tools.protoc -I=/app/proto --python_out=. --grpc_python_out=. /app/proto/device/device.proto

# Add the current directory to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Copy the Postman collection and integration tests into the container
COPY smarthome-api.postman_collection.json .
COPY integration /app/integration

# The command to run tests will be provided by docker-compose
ENTRYPOINT ["/bin/sh", "-c"]