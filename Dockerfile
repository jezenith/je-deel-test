# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster as build

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Add user that will run the app
RUN addgroup --system app && adduser --system --group app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get clean

# Switch to app user
USER app

# Install application dependencies
COPY --chown=app:app requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy local code to the container image
COPY --chown=app:app . .

# Use multi-stage build to create a lean production image
FROM python:3.8-slim-buster as final

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and switch to a new user
RUN addgroup --system app && adduser --system --group app

# Copy requirements from builder image
COPY --from=build /home/app/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH

# Copy application from builder image
WORKDIR /app
COPY --from=build --chown=app:app /app /app

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Switch to app user
USER app

# Run the application
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5001"]
