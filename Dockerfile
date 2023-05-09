# Base image
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev gettext-dev

# Set working directory
WORKDIR /app

# Copy project requirements file
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY . .

# Set startup command
CMD ["sh", "-c", "python manage.py migrate && python manage.py compilemessages"]
