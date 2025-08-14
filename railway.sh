#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations and setup
python setup.py

# Start the application
python app.py
