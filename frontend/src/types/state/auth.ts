/**
 * Authentication state management types
 */
import { UserMeResponse } from '../api/auth';

// Define auth state interface
export interface AuthState {
  user: UserMeResponse | null;
  isLoading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  token: string | null;
}

// Define auth action types with discriminated union
export type AuthAction = 
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: UserMeResponse }
  | { type: 'LOGIN_FAILURE'; error: string }
  | { type: 'LOGOUT' }
  | { type: 'CLEAR_ERROR' };

// Auth context type - aligned with the actual implementation in AuthContext.tsx
export interface AuthContextType {
  isAuthenticated: boolean;
  user: UserMeResponse | null;
  token: string | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  fetchCurrentUser: () => Promise<void>;
}
