# Start from the lightest image for Python3
# FROM python:3-alpine
FROM python:3.6.9-alpine3.9

# Set the working directory to container's root /
WORKDIR /app

# Fix for installing ffmpeg dependencies
RUN apk add build-base

# Install the requirements for the Python app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Dependency for the camera stream
RUN apk add --update ffmpeg

# Dependency for beeping before recording the camera
RUN apk add --update beep

# SEE ENVIRONMENT VARIABLES IN docker-compose.yml

# Copy the folder to the surrounding
COPY . .

# Expose the port where the webhook is listening
EXPOSE 80

# Run the script
CMD ["python", "./bot.py"]
