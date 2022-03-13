#!/usr/bin/env python

import sys
import os

from app import app
app.run(host='0.0.0.0', debug=True, port=5001, threaded=True)  # Start the server