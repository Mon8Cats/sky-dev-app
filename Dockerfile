# Use the slim version of Python
FROM python:3.10-slim

# Set the working directory
WORKDIR /app


# Install dependencies required for psycopg2 and Cloud SQL Auth Proxy
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && apt-get clean

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port Flask will listen on
EXPOSE 8080

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

