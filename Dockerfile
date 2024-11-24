FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install flask
EXPOSE 8080
CMD ["python", "app.py"]




# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port used by Flask (default is 8080)
EXPOSE 8080

# Set the entry point to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
