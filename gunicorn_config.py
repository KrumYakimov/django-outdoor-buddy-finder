# gunicorn_config.py

import multiprocessing

# Number of worker processes (recommended formula)
workers = multiprocessing.cpu_count() * 2 + 1

# Bind to all interfaces on port 8000
bind = "0.0.0.0:8000"

# Worker timeout in seconds
timeout = 120

# Logging level
loglevel = "info"

# Enable access log
accesslog = "-"

# Enable error log
errorlog = "-"

# Preload the application to save memory
preload_app = True
