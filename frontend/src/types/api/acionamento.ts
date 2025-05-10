/**
 * Acionamento related types and interfaces
 */

// Define const object with all possible values to ensure type safety
export const AcionamentoTypes = {
  CONFIRMAR_FATO: 'confirmar_fato',
  NEGAR_FATO: 'negar_fato',
  ACIONAR_TESTEMUNHA: 'acionar_testemunha',
  PROPOR_AJUSTE: 'propor_ajuste',
  DENUNCIAR_MA_FE: 'denunciar_ma_fe',
  SOLICITAR_CONSEQUENCIA: 'solicitar_consequencia'
} as const;

// Create a type from the values of the const object
export type AcionamentoType = typeof AcionamentoTypes[keyof typeof AcionamentoTypes];

// For backward compatibility with existing code
export type ACIONAMENTO_TYPE_LITERAL = AcionamentoType;

export interface AcionarLogEventActionAPIPayload {
  target_log_id: string;
  acionamento_type: AcionamentoType;
  motivo?: string | null;
  dados_adicionais?: Record<string, any> | null;
  testemunha_acionada_id?: string | null;
}

export interface LogAcionadoData {
  target_log_id: string;
  acionamento_type: AcionamentoType;
  motivo?: string | null;
  dados_adicionais?: Record<string, any> | null;
  testemunha_acionada_id?: string | null;
  _raw_user_input_payload?: Record<string, any> | null;
  _llm_full_interpretation?: Record<string, any> | null;
}

export interface LogAcionamentoInfo {
  log_acionado_event_id: string;
  acionamento_type: AcionamentoType;
  author_acionamento: string;
  timestamp_acionamento: string;
  motivo?: string | null;
  status_resolucao_acionamento?: string;
}
