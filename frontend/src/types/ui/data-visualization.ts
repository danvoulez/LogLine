/**
 * Data visualization component props and types
 */
import { LogEvent } from '../api/logEvents';

// KeyValueBlock component props
export interface KeyValueBlockProps {
  data: Record<string, any>;
  title?: string;
  collapsible?: boolean;
  initiallyExpanded?: boolean;
  className?: string;
}

// DataTable component props
export interface DataTableProps<T extends Record<string, any>> {
  data: T[];
  columns: Array<{
    key: keyof T;
    header: string;
    render?: (value: any, row: T) => React.ReactNode;
    sortable?: boolean;
    width?: string | number;
  }>;
  onRowClick?: (row: T) => void;
  sortColumn?: keyof T;
  sortDirection?: 'asc' | 'desc';
  onSortChange?: (column: keyof T, direction: 'asc' | 'desc') => void;
  loading?: boolean;
  emptyMessage?: string;
  className?: string;
}

// CardList component props
export interface CardListProps<T extends Record<string, any>> {
  items: T[];
  renderCard: (item: T, index: number) => React.ReactNode;
  loading?: boolean;
  emptyMessage?: string;
  className?: string;
}

// LogEventCard component props
export interface LogEventCardProps {
  logEvent: LogEvent;
  onClick?: (logEvent: LogEvent) => void;
  selected?: boolean;
  compact?: boolean;
  highlightFields?: string[];
  className?: string;
}

// Type for the rendering heuristics hook
export interface RenderHeuristicsOptions {
  maxItems?: number;
  maxDepth?: number;
  expandObjectsWithFewProps?: boolean;
  renderNullAndUndefined?: boolean;
}
