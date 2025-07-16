#!/bin/bash

echo "Creating Redash database..."
docker-compose run --rm server create_db

echo "Starting Redash services..."
docker-compose up -d

echo "Redash deployment complete. Access at http://localhost:5000"
