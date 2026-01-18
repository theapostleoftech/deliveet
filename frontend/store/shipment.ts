import { create } from "zustand";
import { Shipment, Delivery } from "@/types";
import { apiClient } from "@/lib/api-client";

interface ShipmentStore {
  shipments: Shipment[];
  currentShipment: Shipment | null;
  isLoading: boolean;
  error: string | null;
  fetchShipments: (page?: number) => Promise<void>;
  fetchShipment: (id: string) => Promise<void>;
  createShipment: (data: any) => Promise<Shipment>;
  updateShipment: (id: string, data: any) => Promise<Shipment>;
  deleteShipment: (id: string) => Promise<void>;
  clearError: () => void;
}

export const useShipmentStore = create<ShipmentStore>((set, get) => ({
  shipments: [],
  currentShipment: null,
  isLoading: false,
  error: null,

  fetchShipments: async (page = 1) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get("/shipments/", {
        params: { page, page_size: 20 },
      });
      set({ shipments: response.data.results, isLoading: false });
    } catch (error: any) {
      const message = error.response?.data?.message || "Failed to fetch shipments";
      set({ error: message, isLoading: false });
    }
  },

  fetchShipment: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get(`/shipments/${id}/`);
      set({ currentShipment: response.data.data, isLoading: false });
    } catch (error: any) {
      const message = error.response?.data?.message || "Failed to fetch shipment";
      set({ error: message, isLoading: false });
    }
  },

  createShipment: async (data: any) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post("/shipments/", data);
      const shipment = response.data.data;
      set(state => ({
        shipments: [shipment, ...state.shipments],
        isLoading: false,
      }));
      return shipment;
    } catch (error: any) {
      const message = error.response?.data?.message || "Failed to create shipment";
      set({ error: message, isLoading: false });
      throw error;
    }
  },

  updateShipment: async (id: string, data: any) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.put(`/shipments/${id}/`, data);
      const shipment = response.data.data;
      set(state => ({
        shipments: state.shipments.map(s => (s.id === id ? shipment : s)),
        currentShipment: state.currentShipment?.id === id ? shipment : state.currentShipment,
        isLoading: false,
      }));
      return shipment;
    } catch (error: any) {
      const message = error.response?.data?.message || "Failed to update shipment";
      set({ error: message, isLoading: false });
      throw error;
    }
  },

  deleteShipment: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      await apiClient.delete(`/shipments/${id}/`);
      set(state => ({
        shipments: state.shipments.filter(s => s.id !== id),
        currentShipment: state.currentShipment?.id === id ? null : state.currentShipment,
        isLoading: false,
      }));
    } catch (error: any) {
      const message = error.response?.data?.message || "Failed to delete shipment";
      set({ error: message, isLoading: false });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));

interface DeliveryStore {
  deliveries: Delivery[];
  currentDelivery: Delivery | null;
  isLoading: boolean;
  error: string | null;
  fetchDeliveries: (page?: number) => Promise<void>;
  fetchDelivery: (id: string) => Promise<void>;
  updateDeliveryStatus: (id: string, status: string) => Promise<void>;
  clearError: () => void;
}

export const useDeliveryStore = create<DeliveryStore>((set, get) => ({
  deliveries: [],
  currentDelivery: null,
  isLoading: false,
  error: null,

  fetchDeliveries: async (page = 1) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get("/deliveries/", {
        params: { page, page_size: 20 },
      });
      set({ deliveries: response.data.results, isLoading: false });
    } catch (error: any) {
      const message = error.response?.data?.message || "Failed to fetch deliveries";
      set({ error: message, isLoading: false });
    }
  },

  fetchDelivery: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get(`/deliveries/${id}/`);
      set({ currentDelivery: response.data.data, isLoading: false });
    } catch (error: any) {
      const message = error.response?.data?.message || "Failed to fetch delivery";
      set({ error: message, isLoading: false });
    }
  },

  updateDeliveryStatus: async (id: string, status: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.patch(`/deliveries/${id}/`, { status });
      set(state => ({
        deliveries: state.deliveries.map(d =>
          d.id === id ? { ...d, status: response.data.data.status } : d
        ),
        currentDelivery:
          state.currentDelivery?.id === id
            ? { ...state.currentDelivery, status: response.data.data.status }
            : state.currentDelivery,
        isLoading: false,
      }));
    } catch (error: any) {
      const message = error.response?.data?.message || "Failed to update delivery";
      set({ error: message, isLoading: false });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));
