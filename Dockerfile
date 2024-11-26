# Use the official Python image.
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the port Gunicorn will use
EXPOSE 8080

# Start the app using Gunicorn
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
