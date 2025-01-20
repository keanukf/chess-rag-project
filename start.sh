#!/bin/bash

# Start the backend
python -m backend.main &

# Navigate to the frontend directory
cd frontend

# Start the frontend
npm run dev