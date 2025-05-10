/**
 * Zod schema validation for LogEvent
 */
import { z } from 'zod';

// Record schema helper for objects with unknown structure
const recordSchema = z.record(z.unknown());

// LogEvent schema
export const logEventSchema = z.object({
  id: z.string(),
  timestamp: z.string().datetime(),
  type: z.string(),
  author: z.string(),
  witness: z.string(),
  channel: z.string().nullable().optional(),
  origin: z.string().nullable().optional(),
  data: recordSchema,
  consequence: recordSchema.nullable().optional(),
  meta: recordSchema.nullable().optional(),
});

// Timeline query response schema
export const timelineQueryResponseSchema = z.object({
  events: z.array(logEventSchema),
  total_count: z.number().int().nonnegative(),
  limit: z.number().int().positive(),
  skip: z.number().int().nonnegative(),
});

// Type inference from schemas
export type LogEvent = z.infer<typeof logEventSchema>;
export type TimelineQueryResponse = z.infer<typeof timelineQueryResponseSchema>;

// Validation functions
export const validateLogEvent = (data: unknown): LogEvent => {
  return logEventSchema.parse(data);
};

export const validateTimelineQueryResponse = (data: unknown): TimelineQueryResponse => {
  return timelineQueryResponseSchema.parse(data);
};

// Safe parse functions that don't throw
export const safeParseLogEvent = (data: unknown): { success: boolean; data?: LogEvent; error?: z.ZodError } => {
  const result = logEventSchema.safeParse(data);
  if (result.success) {
    return { success: true, data: result.data };
  } else {
    return { success: false, error: result.error };
  }
};
