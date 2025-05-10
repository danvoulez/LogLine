# AgentOS Project

This repository contains both the backend and frontend components of the AgentOS system.

## Project Structure

- `/backend` - Backend services and APIs
- `/frontend` - Frontend applications and components
- `/docs` - Project documentation
- `/scripts` - Utility scripts
- `/deployment` - Deployment configurations

## Components

### Backend
- `app` - Main application code
- `logline` - Logging functionality
- `opa` - Open Policy Agent for authorization
- `tests` - Test files

### Frontend
- Modern React application structure
- Components for visualization and interaction

See individual directory README files for more detailed documentation.

## Deployment

This project is configured for deployment with:
- Frontend: Netlify (deployed at https://agentos-platform.windsurf.build)
- Backend: Render.com

### Frontend Deployment (Netlify)

1. The frontend has been deployed to Netlify at: https://agentos-platform.windsurf.build
2. Account: dan@danvoulez.com
3. To update the deployment, you can either:
   - Push changes to the connected repository
   - Run the deployment command again: `deploy_web_app`

### Backend Deployment (Render.com)

1. Log in to Render.com with dan@danvoulez.com
2. Create a new Web Service pointing to this repository
3. Configure the following settings:
   - Name: `agentos-backend`
   - Root Directory: `backend`
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.core.main:app --host 0.0.0.0 --port $PORT`
4. Add the required environment variables described in `backend/.env.sample`

### Connecting Frontend to Backend

After deploying the backend, update the frontend environment variable:
- In Netlify dashboard, go to Site settings > Environment variables
- Set `REACT_APP_BACKEND_BASE_URL` to your Render backend URL + `/api/v1`

See `DEPLOYMENT.md` for more detailed instructions.
