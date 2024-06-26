# Base
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

WORKDIR /app
COPY . /app

# Use Gunicorn to run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "qbdl_gui:app"]
