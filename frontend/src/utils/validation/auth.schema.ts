/**
 * Zod schema validation for Auth types
 */
import { z } from 'zod';

// User profile schema
export const userProfileSchema = z.object({
  first_name: z.string().nullable().optional(),
  last_name: z.string().nullable().optional(),
  avatar_url: z.string().url().nullable().optional(),
  phone: z.string().nullable().optional(),
  preferences: z.record(z.unknown()).optional(),
});

// User response schema
export const userMeResponseSchema = z.object({
  id: z.string(),
  username: z.string(),
  email: z.string().email(),
  roles: z.array(z.string()),
  profile: userProfileSchema.nullable(),
  is_active: z.boolean(),
});

// Auth token response schema
export const authTokenResponseSchema = z.object({
  access_token: z.string(),
  token_type: z.string(),
});

// Login request schema
export const loginRequestSchema = z.object({
  username: z.string().min(3),
  password: z.string().min(6),
});

// Type inference from schemas
export type UserProfile = z.infer<typeof userProfileSchema>;
export type UserMeResponse = z.infer<typeof userMeResponseSchema>;
export type AuthTokenResponse = z.infer<typeof authTokenResponseSchema>;
export type LoginRequest = z.infer<typeof loginRequestSchema>;

// Validation functions
export const validateUserMeResponse = (data: unknown): UserMeResponse => {
  return userMeResponseSchema.parse(data);
};

export const validateAuthTokenResponse = (data: unknown): AuthTokenResponse => {
  return authTokenResponseSchema.parse(data);
};

// Form validation
export const validateLoginForm = (data: unknown): LoginRequest => {
  return loginRequestSchema.parse(data);
};
