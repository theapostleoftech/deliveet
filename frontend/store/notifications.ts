import { create } from "zustand";
import { Notification } from "@/types";

interface NotificationStore {
  notifications: Notification[];
  unreadCount: number;
  addNotification: (notification: Notification) => void;
  markAsRead: (id: string) => void;
  removeNotification: (id: string) => void;
  clearAll: () => void;
  setNotifications: (notifications: Notification[]) => void;
}

export const useNotificationStore = create<NotificationStore>((set, get) => ({
  notifications: [],
  unreadCount: 0,

  addNotification: (notification: Notification) => {
    set(state => ({
      notifications: [notification, ...state.notifications],
      unreadCount: !notification.is_read ? state.unreadCount + 1 : state.unreadCount,
    }));
  },

  markAsRead: (id: string) => {
    set(state => ({
      notifications: state.notifications.map(n =>
        n.id === id ? { ...n, is_read: true } : n
      ),
      unreadCount: Math.max(0, state.unreadCount - 1),
    }));
  },

  removeNotification: (id: string) => {
    set(state => ({
      notifications: state.notifications.filter(n => n.id !== id),
    }));
  },

  clearAll: () => {
    set({
      notifications: [],
      unreadCount: 0,
    });
  },

  setNotifications: (notifications: Notification[]) => {
    const unreadCount = notifications.filter(n => !n.is_read).length;
    set({ notifications, unreadCount });
  },
}));
