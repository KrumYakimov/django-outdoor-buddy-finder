import multiprocessing


workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8000"
timeout = 120
loglevel = "info"
accesslog = "-"
errorlog = "-"
preload_app = True
