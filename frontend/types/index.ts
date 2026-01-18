// API Types
export interface APIResponse<T> {
  success: boolean;
  data: T;
  message: string;
  errors?: Record<string, string[]>;
  timestamp: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Authentication Types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  password2: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  role: "customer" | "courier";
}

export interface TokenResponse {
  access: string;
  refresh: string;
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  avatar: string | null;
  is_verified: boolean;
  role: "customer" | "courier";
  created_at: string;
  updated_at: string;
}

export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

// Shipment Types
export enum ShipmentStatus {
  PENDING = "pending",
  ACCEPTED = "accepted",
  IN_TRANSIT = "in_transit",
  DELIVERED = "delivered",
  CANCELLED = "cancelled",
}

export interface Address {
  street: string;
  city: string;
  state: string;
  zipcode: string;
  latitude: number;
  longitude: number;
  country: string;
}

export interface Shipment {
  id: string;
  customer_id: string;
  receiver_name: string;
  receiver_phone: string;
  receiver_email: string;
  pickup_address: Address;
  delivery_address: Address;
  description: string;
  weight: number;
  dimensions: string;
  special_instructions: string;
  status: ShipmentStatus;
  estimated_delivery: string;
  created_at: string;
  updated_at: string;
  price: number;
}

// Delivery Types
export interface Delivery {
  id: string;
  shipment_id: string;
  courier_id: string;
  current_location: {
    latitude: number;
    longitude: number;
  };
  status: ShipmentStatus;
  started_at: string | null;
  completed_at: string | null;
  estimated_delivery_time: string;
}

// Courier Types
export interface Courier {
  id: string;
  user: User;
  is_available: boolean;
  current_location: {
    latitude: number;
    longitude: number;
  };
  rating: number;
  total_deliveries: number;
  verified_at: string | null;
  documents_verified: boolean;
}

// Customer Types
export interface Customer {
  id: string;
  user: User;
  total_shipments: number;
  total_spent: number;
  rating: number;
}

// Wallet Types
export interface Wallet {
  id: string;
  user_id: string;
  balance: number;
  currency: string;
  last_transaction: string;
  created_at: string;
}

// Transaction Types
export enum TransactionType {
  DEBIT = "debit",
  CREDIT = "credit",
}

export enum TransactionStatus {
  PENDING = "pending",
  COMPLETED = "completed",
  FAILED = "failed",
  REFUNDED = "refunded",
}

export interface Transaction {
  id: string;
  wallet_id: string;
  type: TransactionType;
  amount: number;
  status: TransactionStatus;
  reference: string;
  description: string;
  created_at: string;
}

// Notification Types
export interface Notification {
  id: string;
  user_id: string;
  title: string;
  message: string;
  is_read: boolean;
  related_object: string;
  created_at: string;
}

// Rating Types
export interface Rating {
  id: string;
  user_id: string;
  rated_user_id: string;
  shipment_id: string;
  rating: number;
  comment: string;
  created_at: string;
}

// Real-time WebSocket Types
export interface WebSocketMessage {
  type: string;
  data: Record<string, any>;
  timestamp: string;
}

export interface LocationUpdate {
  user_id: string;
  latitude: number;
  longitude: number;
  timestamp: string;
}

export interface DeliveryUpdate {
  delivery_id: string;
  status: ShipmentStatus;
  location: {
    latitude: number;
    longitude: number;
  };
  estimated_arrival: string;
}
