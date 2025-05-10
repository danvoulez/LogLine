/**
 * Form-related component props and types
 */

// Input field types
export type InputType = 'text' | 'number' | 'email' | 'password' | 'date' | 'datetime-local' | 'tel';

// Basic input props
export interface InputProps {
  name: string;
  label?: string;
  type?: InputType;
  value: string | number;
  onChange: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  required?: boolean;
  error?: string;
  className?: string;
}

// Select component props
export interface SelectProps<T extends string | number> {
  name: string;
  label?: string;
  options: Array<{value: T; label: string}>;
  value: T;
  onChange: (value: T) => void;
  placeholder?: string;
  disabled?: boolean;
  required?: boolean;
  error?: string;
  className?: string;
}

// Checkbox props
export interface CheckboxProps {
  name: string;
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
  className?: string;
}

// Form field props with discriminated union for different field types
export type FormFieldProps = 
  | ({ fieldType: 'input' } & InputProps)
  | ({ fieldType: 'select' } & SelectProps<string | number>)
  | ({ fieldType: 'checkbox' } & CheckboxProps);

// Dynamic form definition
export interface FormConfig {
  fields: FormFieldProps[];
  onSubmit: (values: Record<string, any>) => void;
  submitButtonText?: string;
  cancelButtonText?: string;
  onCancel?: () => void;
}
