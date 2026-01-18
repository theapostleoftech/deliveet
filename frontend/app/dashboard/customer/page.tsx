"use client";

import React from "react";
import Link from "next/link";
import { useAuthStore } from "@/store/auth";
import { useShipmentStore } from "@/store/shipment";
import { ProtectedRoute } from "@/components/common/ProtectedRoute";
import { Navbar } from "@/components/common/Navbar";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

export default function CustomerDashboard() {
  const { user } = useAuthStore();
  const { shipments, fetchShipments, isLoading } = useShipmentStore();

  React.useEffect(() => {
    fetchShipments();
  }, []);

  return (
    <ProtectedRoute requiredRole="customer">
      <Navbar />
      <main className="bg-light min-h-screen">
        <div className="container-fluid py-8">
          {/* Header */}
          <div className="flex-between mb-8">
            <div>
              <h1 className="text-display text-dark">
                Welcome back, {user?.first_name}!
              </h1>
              <p className="text-body text-gray-600 mt-2">Manage your shipments and track deliveries</p>
            </div>
            <Button variant="primary" size="lg">
              <Link href="/dashboard/customer/new-shipment">
                Send Package
              </Link>
            </Button>
          </div>

          {/* Stats */}
          <div className="grid md:grid-cols-4 gap-4 mb-8">
            {[
              { label: "Total Shipments", value: "12", icon: "📦" },
              { label: "In Transit", value: "2", icon: "🚚" },
              { label: "Completed", value: "10", icon: "✅" },
              { label: "Wallet Balance", value: "₦5,000", icon: "💰" },
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

          {/* Recent Shipments */}
          <Card>
            <div className="flex-between mb-6">
              <h2 className="text-subheading text-dark">Recent Shipments</h2>
              <Link href="/dashboard/customer/shipments" className="text-primary-500 hover:text-primary-600">
                View All
              </Link>
            </div>

            {isLoading ? (
              <div className="space-y-4">
                {[1, 2, 3].map(i => (
                  <div key={i} className="h-16 bg-light rounded-lg animate-pulse"></div>
                ))}
              </div>
            ) : shipments.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-body text-gray-600 mb-4">No shipments yet</p>
                <Button variant="primary" onClick={() => window.location.href = "/dashboard/customer/new-shipment"}>
                  Send Your First Package
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {shipments.slice(0, 5).map(shipment => (
                  <div
                    key={shipment.id}
                    className="flex-between p-4 border border-light rounded-lg hover:border-primary-200 hover:bg-primary-50 transition-all cursor-pointer"
                  >
                    <div>
                      <p className="text-body font-medium text-dark">
                        {shipment.receiver_name}
                      </p>
                      <p className="text-small text-gray-500">
                        {shipment.delivery_address.city}
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="badge badge-primary">{shipment.status}</span>
                      <p className="text-small text-gray-600 mt-1">₦{shipment.price}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>
      </main>
    </ProtectedRoute>
  );
}
