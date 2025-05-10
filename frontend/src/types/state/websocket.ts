/**
 * WebSocket state management types
 */
import { WebSocketMessage } from '../api/websocket';

// WebSocket connection status
export type WebSocketStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

// WebSocket state interface
export interface WebSocketState {
  status: WebSocketStatus;
  messages: WebSocketMessage[];
  error: string | null;
  lastMessageTimestamp: string | null;
}

// WebSocket actions
export type WebSocketAction = 
  | { type: 'WS_CONNECTING' }
  | { type: 'WS_CONNECTED' }
  | { type: 'WS_DISCONNECTED' }
  | { type: 'WS_ERROR'; error: string }
  | { type: 'WS_MESSAGE_RECEIVED'; message: WebSocketMessage }
  | { type: 'WS_CLEAR_MESSAGES' };

// WebSocket context type
export interface WebSocketContextType {
  state: WebSocketState;
  dispatch: React.Dispatch<WebSocketAction>;
  connect: () => void;
  disconnect: () => void;
  sendMessage: (type: string, payload: unknown) => void;
}
