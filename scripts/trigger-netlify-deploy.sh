#!/bin/bash

# Netlify Build Webhook Trigger Script
# This script triggers a new Netlify build and deployment using a build hook

# Replace with your actual Netlify build hook ID
# You can create this in the Netlify dashboard: Site settings > Build & deploy > Build hooks
NETLIFY_BUILD_HOOK_ID="YOUR_BUILD_HOOK_ID"

# Trigger the build
echo "Triggering Netlify build..."
curl -X POST -d {} https://api.netlify.com/build_hooks/$NETLIFY_BUILD_HOOK_ID

echo ""
echo "Build triggered! Check your Netlify dashboard for status."
echo "https://app.netlify.com/sites/agentos-platform-3via9/deploys"
