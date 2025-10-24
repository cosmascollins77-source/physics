#!/usr/bin/env bash
# exit on error
set -o errexit

# Check if we're running on Render
if [[ "${RENDER}" == "true" ]]; then
  echo "Running on Render - executing build steps"
  
  # Install dependencies
  echo "Installing dependencies..."
  pip install -r requirements.txt
  
  # Run database migrations
  echo "Running database migrations..."
  python manage.py migrate --no-input
  
  # Collect static files
  echo "Collecting static files..."
  python manage.py collectstatic --no-input -c
  
  # Populate sample data
  echo "Populating sample data..."
  python manage.py populate_data
  
  echo "Build completed successfully!"
else
  echo "Running locally - skipping build steps"
  # For local development, we don't need to run these commands
  # They should be run manually when needed
fi