# AgentOS Deployment Guide

This guide provides instructions for deploying the AgentOS application, with the frontend on Netlify and the backend on Render.com.

## Account Information
- Both Netlify and Render.com accounts are registered under: `dan@danvoulez.com`

## Frontend Deployment (Netlify)

1. Log in to your Netlify account (dan@danvoulez.com)
2. From the Netlify dashboard, click "Add new site" > "Import an existing project"
3. Connect to your GitHub repository
4. Configure the build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/build`
5. Under "Advanced build settings", add the following environment variables:
   - `REACT_APP_BACKEND_BASE_URL`: URL of your backend on Render (to be obtained after backend deployment)
6. Click "Deploy site"

## Backend Deployment (Render.com)

1. Log in to your Render account (dan@danvoulez.com)
2. From the dashboard, click "New" > "Web Service"
3. Connect to your GitHub repository
4. Configure the service:
   - Name: `agentos-backend`
   - Root Directory: `backend`
   - Runtime: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.core.main:app --host 0.0.0.0 --port $PORT`
5. Add the following environment variables:
   - `MONGODB_URI`: Your MongoDB connection string (consider using Render's MongoDB service or MongoDB Atlas)
   - `OPA_URL`: OPA service URL (or consider using a managed policy service)
   - `JWT_SECRET_KEY`: A strong, random string for JWT token signing
   - `JWT_ALGORITHM`: HS256
   - `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: 60
   - `LOG_LEVEL`: info
   - `LLM_PROVIDER`: Your chosen LLM provider (or "mock" for testing)
6. Click "Create Web Service"

## Connecting Frontend and Backend

After both services are deployed:
1. Get the URL of your backend service from Render (e.g., `https://agentos-backend.onrender.com`)
2. Update the frontend environment variable on Netlify:
   - `REACT_APP_BACKEND_BASE_URL`: `https://agentos-backend.onrender.com/api/v1`
3. Trigger a new deployment of your frontend to apply the changes

## Additional Considerations

### Database
For MongoDB, you have several options:
- Use MongoDB Atlas (recommended for production)
- Use Render's MongoDB service
- Set up your own MongoDB instance

### OPA (Open Policy Agent)
You'll need to either:
- Deploy OPA separately on Render or another service
- Use a managed policy service
- Modify the application to use a different authorization approach

Remember to update the OPA_URL environment variable accordingly.
