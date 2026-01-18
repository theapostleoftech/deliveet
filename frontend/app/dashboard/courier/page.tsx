"use client";

import React from "react";
import { useAuthStore } from "@/store/auth";
import { useDeliveryStore } from "@/store/shipment";
import { ProtectedRoute } from "@/components/common/ProtectedRoute";
import { Navbar } from "@/components/common/Navbar";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

export default function CourierDashboard() {
  const { user } = useAuthStore();
  const { deliveries, fetchDeliveries, isLoading } = useDeliveryStore();

  React.useEffect(() => {
    fetchDeliveries();
  }, []);

  return (
    <ProtectedRoute requiredRole="courier">
      <Navbar />
      <main className="bg-light min-h-screen">
        <div className="container-fluid py-8">
          {/* Header */}
          <div className="flex-between mb-8">
            <div>
              <h1 className="text-display text-dark">
                Welcome, {user?.first_name}!
              </h1>
              <p className="text-body text-gray-600 mt-2">Manage your deliveries and earnings</p>
            </div>
            <Button variant="primary" size="lg">
              Go Online
            </Button>
          </div>

          {/* Stats */}
          <div className="grid md:grid-cols-4 gap-4 mb-8">
            {[
              { label: "Total Deliveries", value: "245", icon: "📦" },
              { label: "Completed Today", value: "8", icon: "✅" },
              { label: "In Progress", value: "2", icon: "🚚" },
              { label: "Earnings Today", value: "₦12,500", icon: "💰" },
            ].map((stat, idx) => (
              <Card key={idx}>
                <div className="flex-between">
                  <div>
                    <p className="text-small text-gray-600 mb-1">{stat.label}</p>
                    <p className="text-heading text-dark">{stat.value}</p>
                  </div>
                  <div className="text-4xl">{stat.icon}</div>
                </div>
              </Card>
            ))}
          </div>

          {/* Available Deliveries */}
          <div className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <Card>
                <h2 className="text-subheading text-dark mb-6">Available Deliveries</h2>
                {isLoading ? (
                  <div className="space-y-4">
                    {[1, 2, 3].map(i => (
                      <div key={i} className="h-24 bg-light rounded-lg animate-pulse"></div>
                    ))}
                  </div>
                ) : (
                  <div className="space-y-4">
                    {[1, 2, 3].map(i => (
                      <div
                        key={i}
                        className="p-4 border border-light rounded-lg hover:border-primary-200 hover:bg-primary-50 transition-all"
                      >
                        <div className="flex-between mb-3">
                          <div>
                            <p className="text-body font-medium text-dark">
                              Delivery to Lagos
                            </p>
                            <p className="text-small text-gray-500 mt-1">
                              5.2 km away • Package weight: 2kg
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="text-subheading font-bold text-primary-500">
                              ₦2,500
                            </p>
                          </div>
                        </div>
                        <Button variant="primary" size="sm" className="w-full">
                          Accept Delivery
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            </div>

            {/* Current Delivery Map */}
            <Card>
              <h2 className="text-subheading text-dark mb-4">Current Delivery</h2>
              <div className="h-64 bg-light rounded-lg flex items-center justify-center">
                <p className="text-gray-500">No active delivery</p>
              </div>
              <div className="mt-4 space-y-3">
                <div className="flex-between">
                  <span className="text-small text-gray-600">Pickup Time</span>
                  <span className="text-small font-medium">--:--</span>
                </div>
                <div className="flex-between">
                  <span className="text-small text-gray-600">Delivery Time</span>
                  <span className="text-small font-medium">--:--</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </main>
    </ProtectedRoute>
  );
}
