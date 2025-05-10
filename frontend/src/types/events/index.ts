/**
 * Event types for domain events
 */

// Base event interface
export interface DomainEvent<T extends string, P> {
  type: T;
  payload: P;
  timestamp: string;
  id: string;
}

// System events
export type SystemEventType = 'system:initialized' | 'system:error' | 'system:warning';

export interface SystemEvent extends DomainEvent<SystemEventType, {
  message: string;
  source?: string;
  data?: unknown;
}> {}

// User events
export type UserEventType = 'user:login' | 'user:logout' | 'user:action' | 'user:preference_changed';

export interface UserEvent extends DomainEvent<UserEventType, {
  userId: string;
  action?: string;
  data?: unknown;
}> {}

// Application events union type
export type ApplicationEvent = SystemEvent | UserEvent;

// Event handler type
export type EventHandler<E extends ApplicationEvent> = (event: E) => void;

// Event bus subscriber
export interface EventSubscription {
  unsubscribe: () => void;
}
