#!/bin/sh

# Wait for backend to be ready (optional, for development)
echo "Starting frontend development server..."
exec yarn dev --host 0.0.0.0
