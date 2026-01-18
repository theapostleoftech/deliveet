import { create } from "zustand";
import { persist } from "zustand/middleware";
import { AuthState, User, TokenResponse } from "@/types";
import { apiClient } from "@/lib/api-client";

interface AuthStore extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  setTokens: (tokens: TokenResponse) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      setTokens: (tokens: TokenResponse) => {
        apiClient.setTokens(tokens.access, tokens.refresh);
        set({
          accessToken: tokens.access,
          refreshToken: tokens.refresh,
          isAuthenticated: true,
        });
      },

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiClient.post<TokenResponse>("/auth/login/", {
            email,
            password,
          });

          const tokens = response.data;
          apiClient.setTokens(tokens.access, tokens.refresh);

          // Fetch user data
          const userResponse = await apiClient.get<{ data: User }>("/auth/user/");
          const user = userResponse.data.data;

          set({
            user,
            accessToken: tokens.access,
            refreshToken: tokens.refresh,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error: any) {
          const message = error.response?.data?.message || "Login failed";
          set({ error: message, isLoading: false });
          throw error;
        }
      },

      register: async (data: any) => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiClient.post<TokenResponse>("/auth/register/", data);
          const tokens = response.data;
          apiClient.setTokens(tokens.access, tokens.refresh);

          // Fetch user data
          const userResponse = await apiClient.get<{ data: User }>("/auth/user/");
          const user = userResponse.data.data;

          set({
            user,
            accessToken: tokens.access,
            refreshToken: tokens.refresh,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error: any) {
          const message = error.response?.data?.message || "Registration failed";
          set({ error: message, isLoading: false });
          throw error;
        }
      },

      logout: () => {
        apiClient.clearTokens();
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
          error: null,
        });
      },

      refreshUser: async () => {
        try {
          const response = await apiClient.get<{ data: User }>("/auth/user/");
          const user = response.data.data;
          set({ user });
        } catch (error) {
          set({ isAuthenticated: false });
          throw error;
        }
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: "auth-storage",
      partialize: state => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        user: state.user,
      }),
    }
  )
);
