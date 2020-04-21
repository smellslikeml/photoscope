import sys
sys.path.append('webapp/')
from utils import *
import config as cfg

app = True

if app:
    from photoscope.webapp.app import app
    app.secret_key = 'super secret key'
    app.run("0.0.0.0", port=5000)
