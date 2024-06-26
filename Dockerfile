# Base image
FROM python:3.12-alpine

# Install gcc and other necessary build tools
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Set up working directory
WORKDIR /app
COPY . /app

# Gunicorn configuration
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers=4", "--worker-class=gevent", "qbdl_gui:app"]
