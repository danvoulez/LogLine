/**
 * WebSocket message types and related interfaces
 */
import { LogEvent } from './logEvents';

export interface WebSocketMessage {
  type: string;
  payload: unknown;
  timestamp_utc: string;
}

export interface NewLogEventV2Message extends WebSocketMessage {
  type: "new_log_event_v2";
  payload: LogEvent;
}
