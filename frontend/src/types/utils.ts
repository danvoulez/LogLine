/**
 * Utility types for enhanced type safety
 */

// Make all properties required (remove optionality)
export type RequiredProps<T> = {
  [P in keyof T]-?: T[P];
};

// Make all properties optional
export type OptionalProps<T> = {
  [P in keyof T]?: T[P];
};

// Make all properties non-nullable (remove null and undefined)
export type NonNullableProps<T> = {
  [P in keyof T]: NonNullable<T[P]>;
};

// Deep partial for nested objects
export type DeepPartial<T> = T extends object ? {
  [P in keyof T]?: DeepPartial<T[P]>;
} : T;

// Pick properties of specific type
export type PickByType<T, ValueType> = {
  [Key in keyof T as T[Key] extends ValueType ? Key : never]: T[Key]
};

// Omit properties of specific type
export type OmitByType<T, ValueType> = {
  [Key in keyof T as T[Key] extends ValueType ? never : Key]: T[Key]
};

// Record with specific keys
export type RecordWithKeys<K extends string | number | symbol, T> = {
  [P in K]: T;
};

// Create a type that ensures at least one property from the original type is present
export type AtLeastOne<T, Keys extends keyof T = keyof T> = 
  Pick<T, Exclude<keyof T, Keys>> 
  & {
    [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>>
  }[Keys];

// Create a type for function parameters
export type FunctionParams<T extends (...args: any[]) => any> = 
  T extends (...args: infer P) => any ? P : never;

// Create a type for function return type
export type FunctionReturn<T extends (...args: any[]) => any> = 
  T extends (...args: any[]) => infer R ? R : never;

// Create a type for async function return type
export type AsyncReturnType<T extends (...args: any[]) => Promise<any>> = 
  T extends (...args: any[]) => Promise<infer R> ? R : never;
