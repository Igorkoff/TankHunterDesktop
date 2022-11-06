"""
The Gunicorn Config File.
"""
import multiprocessing

# WSGI application path. This finds wsgi.py in the project directory.
wsgi_app = "awm2023_tutorial.wsgi"

# The socket to bind, in this case port 8002.
# A string of the form: HOST, HOST:PORT, unix:PATH, fd://FD.
bind = "0.0.0.0:8002"

# The number of worker processes for handling requests.
# A positive integer generally in the 2-4 x NUM_CORES in the computer range.
# You can vary this a bit to find the best for your particular application's work load.
workers = multiprocessing.cpu_count() * 2 + 1

# The number of worker threads for handling requests. Run each worker with the specified number of threads.
# A positive integer generally in the 2-4 x NUM_CORES range.
# You can vary this a bit to find the best for your particular application's work load.
threads = multiprocessing.cpu_count() * 2

# Write the access log to stdout.
accesslog = "-"
