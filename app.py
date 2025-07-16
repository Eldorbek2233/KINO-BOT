#!/usr/bin/env python3
"""
Alternative entry point for deployment platforms
Render platform backup entry point
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import wsgi application
from wsgi import application

# For platforms that expect 'app' variable
app = application

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
