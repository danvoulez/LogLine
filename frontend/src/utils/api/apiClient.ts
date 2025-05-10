/**
 * Type-safe API client using Zod validation
 */
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { 
  validateLogEvent, 
  validateTimelineQueryResponse,
  validateUserMeResponse,
  validateAuthTokenResponse,
  validateAcionarLogEventActionPayload
} from '../validation';

// Create a base axios instance
const baseURL = process.env.REACT_APP_BACKEND_BASE_URL || 'http://localhost:8001/api/v1';

const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
});

// Add request interceptor for auth
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('authToken');
    }
    return Promise.reject(error);
  }
);

// Generic wrapper for type-safe API requests
async function apiRequest<T, V>(
  method: 'get' | 'post' | 'put' | 'delete', 
  url: string, 
  validator: (data: unknown) => T,
  data?: V,
  config?: AxiosRequestConfig
): Promise<T> {
  try {
    let response: AxiosResponse;
    
    if (method === 'get') {
      response = await api.get(url, config);
    } else if (method === 'post') {
      response = await api.post(url, data, config);
    } else if (method === 'put') {
      response = await api.put(url, data, config);
    } else if (method === 'delete') {
      response = await api.delete(url, config);
    } else {
      throw new Error(`Unsupported method: ${method}`);
    }
    
    // Validate response data
    return validator(response.data);
  } catch (error) {
    // Handle validation errors separately
    if (error instanceof Error && error.name === 'ZodError') {
      console.error('API response validation error:', error);
      throw new Error(`API response validation failed: ${error.message}`);
    }
    throw error;
  }
}

// Auth API calls
export async function login(username: string, password: string) {
  return apiRequest(
    'post',
    '/auth/token',
    validateAuthTokenResponse,
    { username, password }
  );
}

export async function getCurrentUser() {
  return apiRequest(
    'get',
    '/users/me',
    validateUserMeResponse
  );
}

// LogEvent API calls
export async function getLogEvent(id: string) {
  return apiRequest(
    'get',
    `/log-events/${id}`,
    validateLogEvent
  );
}

export async function getTimeline(limit = 10, skip = 0, filters?: Record<string, any>) {
  return apiRequest(
    'get',
    '/timeline',
    validateTimelineQueryResponse,
    undefined,
    { params: { limit, skip, ...filters } }
  );
}

// Acionamento API calls
export async function acionarLogEvent(payload: ReturnType<typeof validateAcionarLogEventActionPayload>) {
  return apiRequest(
    'post',
    '/actions/acionar',
    validateLogEvent,
    payload
  );
}

// Export the base API for other uses
export default api;
