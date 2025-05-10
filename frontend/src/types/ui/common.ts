/**
 * Common UI component props
 */

// Common sizes used across the application
export type Size = 'sm' | 'md' | 'lg' | 'xl';

// Common variant types
export type Variant = 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info';

// Button props with consistent naming and structure
export interface ButtonProps {
  variant?: Variant;
  size?: Size;
  onClick?: () => void;
  disabled?: boolean;
  fullWidth?: boolean;
  children: React.ReactNode;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}

// Card component props with discriminated union for different variants
export type CardProps = 
  | { variant: 'standard'; title: string; content: React.ReactNode }
  | { variant: 'image'; title: string; imageUrl: string; alt?: string }
  | { variant: 'action'; title: string; actionText: string; onAction: () => void };

// Common layout components
export interface ContainerProps {
  children: React.ReactNode;
  maxWidth?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'full';
  className?: string;
}

// Modal props
export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  size?: Size;
}
