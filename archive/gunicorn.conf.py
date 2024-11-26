# gunicorn.conf.py

# Server socket
bind = "0.0.0.0:8080"

# Workers and threads
workers = 4  # Number of worker processes
threads = 2  # Number of threads per worker

# Logging
loglevel = "info"  # Log level
accesslog = "-"  # Log access to stdout
errorlog = "-"  # Log errors to stdout

# Timeout
timeout = 30  # Seconds before worker timeout
