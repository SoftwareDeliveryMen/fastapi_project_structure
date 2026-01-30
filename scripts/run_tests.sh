#!/bin/bash

echo "Running tests..."

# Run pytest with coverage
pytest tests/ \
    --cov=app \
    --cov-report=html \
    --cov-report=term-missing \
    -v

echo "Coverage report generated in htmlcov/index.html"