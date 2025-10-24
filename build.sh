#!/usr/bin/env bash
# exit on error
set -o errexit

# Check if we're running on Render
if [[ "${RENDER}" == "true" ]]; then
  echo "Running on Render - executing build steps"
  # Install dependencies
  pip install -r requirements.txt

  # Collect static files
  python manage.py collectstatic --no-input

  # Run database migrations
  python manage.py migrate

  # Populate sample data
  python manage.py populate_data
else
  echo "Running locally - skipping build steps"
  # For local development, we don't need to run these commands
  # They should be run manually when needed
fi