/**
 * Inventory and CurrentState related types
 */

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
