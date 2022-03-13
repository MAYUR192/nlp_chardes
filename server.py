#!/usr/bin/env python

import sys
import os

""" Register BluePrint here"""

os.environ['prod_env'] =  sys.argv[1]

os.environ['url_param'] =  sys.argv[2]


from app import app
app.run(host='0.0.0.0', debug=True, port=5001, threaded=True)  # Start the server