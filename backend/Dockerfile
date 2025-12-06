FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set Python path to include the current directory
ENV PYTHONPATH=/app
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Run the application
# Use shell form to ensure variable expansion if needed, but exec form is preferred.
# We explicitly bind to 0.0.0.0 and use the PORT env var.
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"
