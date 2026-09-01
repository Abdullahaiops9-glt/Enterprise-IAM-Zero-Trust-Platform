FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the risk engine API script into the container
COPY app.py .

# Expose port 8000 for the risk engine service
EXPOSE 8000

# Start the risk engine API when the container launches
CMD ["python3", "app.py"]
