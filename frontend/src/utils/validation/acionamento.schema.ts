/**
 * Zod schema validation for Acionamento types
 */
import { z } from 'zod';

// Define the acionamento type literals using zod enum
export const acionamentoTypeEnum = z.enum([
  'confirmar_fato',
  'negar_fato',
  'acionar_testemunha',
  'propor_ajuste',
  'denunciar_ma_fe',
  'solicitar_consequencia'
]);

// Payload schema
export const acionarLogEventActionPayloadSchema = z.object({
  target_log_id: z.string(),
  acionamento_type: acionamentoTypeEnum,
  motivo: z.string().nullable().optional(),
  dados_adicionais: z.record(z.unknown()).nullable().optional(),
  testemunha_acionada_id: z.string().nullable().optional(),
});

// Log acionado data schema
export const logAcionadoDataSchema = z.object({
  target_log_id: z.string(),
  acionamento_type: acionamentoTypeEnum,
  motivo: z.string().nullable().optional(),
  dados_adicionais: z.record(z.unknown()).nullable().optional(),
  testemunha_acionada_id: z.string().nullable().optional(),
  _raw_user_input_payload: z.record(z.unknown()).nullable().optional(),
  _llm_full_interpretation: z.record(z.unknown()).nullable().optional(),
});

// Acionamento info schema
export const logAcionamentoInfoSchema = z.object({
  log_acionado_event_id: z.string(),
  acionamento_type: acionamentoTypeEnum,
  author_acionamento: z.string(),
  timestamp_acionamento: z.string().datetime(),
  motivo: z.string().nullable().optional(),
  status_resolucao_acionamento: z.string().optional(),
});

// Type inference from schemas
export type AcionamentoType = z.infer<typeof acionamentoTypeEnum>;
export type AcionarLogEventActionPayload = z.infer<typeof acionarLogEventActionPayloadSchema>;
export type LogAcionadoData = z.infer<typeof logAcionadoDataSchema>;
export type LogAcionamentoInfo = z.infer<typeof logAcionamentoInfoSchema>;

// Validation functions
export const validateAcionarLogEventActionPayload = (data: unknown): AcionarLogEventActionPayload => {
  return acionarLogEventActionPayloadSchema.parse(data);
};

export const validateLogAcionadoData = (data: unknown): LogAcionadoData => {
  return logAcionadoDataSchema.parse(data);
};

export const validateLogAcionamentoInfo = (data: unknown): LogAcionamentoInfo => {
  return logAcionamentoInfoSchema.parse(data);
};
