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
}

// Define auth action types with discriminated union
export type AuthAction = 
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: UserMeResponse }
  | { type: 'LOGIN_FAILURE'; error: string }
  | { type: 'LOGOUT' }
  | { type: 'CLEAR_ERROR' };

// Auth context type
export interface AuthContextType {
  state: AuthState;
  dispatch: React.Dispatch<AuthAction>;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}
