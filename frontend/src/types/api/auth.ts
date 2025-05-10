/**
 * Authentication and User types
 */

export interface UserProfileAPI {
  first_name?: string | null;
  last_name?: string | null;
  avatar_url?: string | null;
  phone?: string | null;
  preferences?: Record<string, any>;
}

export interface UserMeResponse {
  id: string;
  username: string;
  email: string;
  roles: string[];
  profile: UserProfileAPI | null;
  is_active: boolean;
}

export interface AuthTokenResponse {
  access_token: string;
  token_type: string;
}
