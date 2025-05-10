// --- User & Auth ---
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

// --- LogEvent & Timeline ---
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

// --- CurrentState Models (Example for Inventory) ---
export interface CurrentStateInventoryItem {
  id: string;
  name?: string | null;
  sku?: string | null;
  current_stock: number;
  category?: string | null;
  unit_of_measure?: string | null;
  low_stock_threshold?: number | null;
  last_received_date?: string | null;
  last_sale_date?: string | null;
  average_cost_str?: string | null;
  selling_price_str?: string | null;
  image_url?: string | null;
  is_active: boolean;
  tags?: string[];
  last_log_event_id?: string | null;
  last_updated_at: string;
}

// --- WebSocket Messages ---
export interface WebSocketMessage {
  type: string;
  payload: any;
  timestamp_utc: string;
}

export interface NewLogEventV2Message extends WebSocketMessage {
  type: "new_log_event_v2";
  payload: LogEvent;
}

// --- Acionamento Types ---
export type ACIONAMENTO_TYPE_LITERAL =
  | "confirmar_fato"
  | "negar_fato"
  | "acionar_testemunha"
  | "propor_ajuste"
  | "denunciar_ma_fe"
  | "solicitar_consequencia";

export interface AcionarLogEventActionAPIPayload {
  target_log_id: string;
  acionamento_type: ACIONAMENTO_TYPE_LITERAL;
  motivo?: string | null;
  dados_adicionais?: Record<string, any> | null;
  testemunha_acionada_id?: string | null;
}

export interface LogAcionadoData {
  target_log_id: string;
  acionamento_type: ACIONAMENTO_TYPE_LITERAL;
  motivo?: string | null;
  dados_adicionais?: Record<string, any> | null;
  testemunha_acionada_id?: string | null;
  _raw_user_input_payload?: Record<string, any> | null;
  _llm_full_interpretation?: Record<string, any> | null;
}

export interface LogAcionamentoInfo {
  log_acionado_event_id: string;
  acionamento_type: ACIONAMENTO_TYPE_LITERAL;
  author_acionamento: string;
  timestamp_acionamento: string;
  motivo?: string | null;
  status_resolucao_acionamento?: string;
}