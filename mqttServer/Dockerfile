# Use an official Python runtime as a parent image
FROM python:3.9

# Install Mosquitto
RUN apt-get update && apt-get install -y mosquitto mosquitto-clients

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY ./config/requirements.txt ./

# Install dependencies
RUN pip install paho-mqtt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Mosquitto and FastAPI ports
EXPOSE 8004

# Start Mosquitto broker and the FastAPI application
CMD ["sh", "-c", "mosquitto -d && uvicorn subscribe:app --host 0.0.0.0 --port 8004"]