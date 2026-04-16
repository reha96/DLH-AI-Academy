#!/bin/bash
# Make sure script is executable
chmod +x web.sh 2>/dev/null || true

# Start gunicorn with production settings
# gunicorn main:app --bind 0.0.0.0:$PORT --workers 2 --threads 4
