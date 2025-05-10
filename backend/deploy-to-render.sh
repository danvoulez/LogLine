#!/bin/bash

# Render deployment script
# This script deploys the backend to Render.com using their API

# Check if RENDER_API_KEY is set
if [ -z "$RENDER_API_KEY" ]; then
  echo "Error: RENDER_API_KEY environment variable is not set"
  echo "Please set it with: export RENDER_API_KEY=your_api_key"
  exit 1
fi

# Set the repository details
REPO_URL="https://github.com/danvoulez/LogLine.git"
REPO_BRANCH="main"
SERVICE_NAME="agentos-backend"

# Create a deploy request
echo "Creating deploy request for $SERVICE_NAME..."
RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"clearCache\": \"do_not_clear\", \"serviceId\": \"$SERVICE_NAME\"}" \
  https://api.render.com/v1/services/$SERVICE_NAME/deploys)

# Check the deployment status
DEPLOY_ID=$(echo $RESPONSE | jq -r '.id')

if [ "$DEPLOY_ID" == "null" ]; then
  echo "Error: Failed to create deployment"
  echo "Response: $RESPONSE"
  exit 1
fi

echo "Deployment created with ID: $DEPLOY_ID"
echo "Monitor your deployment at: https://dashboard.render.com/"

# Poll deployment status
echo "Checking deployment status..."
STATUS="in_progress"

while [ "$STATUS" == "in_progress" ] || [ "$STATUS" == "created" ]; do
  sleep 10
  DEPLOY_INFO=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
    https://api.render.com/v1/services/$SERVICE_NAME/deploys/$DEPLOY_ID)
  
  STATUS=$(echo $DEPLOY_INFO | jq -r '.status')
  echo "Deployment status: $STATUS"
done

if [ "$STATUS" == "live" ]; then
  echo "Deployment successful!"
else
  echo "Deployment failed with status: $STATUS"
  exit 1
fi
