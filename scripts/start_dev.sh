#!/bin/bash

echo "Starting development server..."

# Load environment variables
export $(cat .env | xargs)

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000