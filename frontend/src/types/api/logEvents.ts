/**
 * Log Event types and Timeline related interfaces
 */

export interface LogEvent {
  id: string;
  timestamp: string;
  type: string;
  author: string;
  witness: string;
  channel?: string | null;
  origin?: string | null;
  data: Record<string, any>;
  consequence?: Record<string, any> | null;
  meta?: Record<string, any> | null;
}

export interface TimelineQueryResponse {
  events: LogEvent[];
  total_count: number;
  limit: number;
  skip: number;
}
