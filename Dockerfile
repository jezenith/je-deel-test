# First stage: Python build stage
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Second stage: Application run stage
FROM python:3.9-slim as app

WORKDIR /app

# Create a group and user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy from builder stage
COPY --from=builder /root/.local /root/.local
COPY . .

# Change ownership of app directory to appuser
RUN chown -R appuser:appuser /app

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

# Apply database migrations
RUN python -c "from app import create_db; create_db()"

# Switch to non-root user
USER appuser

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:5001/health || exit 1

# Start the application
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]
