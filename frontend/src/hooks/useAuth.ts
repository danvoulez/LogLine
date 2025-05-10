import { useContext } from 'react';
import { AuthContext } from '@context/AuthContext';
import { type AuthContextType } from '@/types/state/auth';
import { login as apiLogin, getCurrentUser } from '@utils/api';
import { validateLoginForm, type LoginRequest } from '@utils/validation';

/**
 * Enhanced type-safe useAuth hook
 * Provides authentication functionality and type checking
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  // Enhanced login function with validation
  const enhancedLogin = async (username: string, password: string): Promise<void> => {
    try {
      // Validate the login request
      const validatedRequest = validateLoginForm({ username, password });
      
      // Call the original context login function
      await context.login(validatedRequest.username, validatedRequest.password);
    } catch (error) {
      // Rethrow with more descriptive error
      if (error instanceof Error) {
        throw new Error(`Login failed: ${error.message}`);
      }
      throw error;
    }
  };
  
  // Return the correct shape that matches AuthContextType
  return {
    isAuthenticated: context.isAuthenticated,
    user: context.user,
    token: context.token,
    isLoading: context.isLoading,
    login: enhancedLogin,
    logout: context.logout,
    fetchCurrentUser: context.fetchCurrentUser
  };
};