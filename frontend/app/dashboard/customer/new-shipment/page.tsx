"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { useAuthStore } from "@/store/auth";
import { useShipmentStore } from "@/store/shipment";
import { ProtectedRoute } from "@/components/common/ProtectedRoute";
import { Navbar } from "@/components/common/Navbar";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";
import { Alert } from "@/components/ui/Alert";

interface ShipmentFormData {
  receiver_name: string;
  receiver_phone: string;
  receiver_email: string;
  delivery_address_street: string;
  delivery_address_city: string;
  delivery_address_state: string;
  delivery_address_zipcode: string;
  description: string;
  weight: number;
  special_instructions: string;
}

export default function NewShipmentPage() {
  const router = useRouter();
  const { register, handleSubmit, formState: { errors } } = useForm<ShipmentFormData>();
  const { createShipment, isLoading, error, clearError } = useShipmentStore();

  const onSubmit = async (data: ShipmentFormData) => {
    try {
      const shipmentData = {
        receiver_name: data.receiver_name,
        receiver_phone: data.receiver_phone,
        receiver_email: data.receiver_email,
        delivery_address: {
          street: data.delivery_address_street,
          city: data.delivery_address_city,
          state: data.delivery_address_state,
          zipcode: data.delivery_address_zipcode,
          country: "Nigeria",
          latitude: 0,
          longitude: 0,
        },
        description: data.description,
        weight: data.weight,
        special_instructions: data.special_instructions,
      };

      await createShipment(shipmentData);
      router.push("/dashboard/customer");
    } catch (err) {
      // Error is already set in store
    }
  };

  return (
    <ProtectedRoute requiredRole="customer">
      <Navbar />
      <main className="bg-light min-h-screen">
        <div className="container-fluid py-8">
          <div className="max-w-2xl">
            <div className="mb-8">
              <h1 className="text-display text-dark">Send a Package</h1>
              <p className="text-body text-gray-600 mt-2">Fill in the details below to book a delivery</p>
            </div>

            {error && (
              <Alert
                type="error"
                message={error}
                onClose={clearError}
                className="mb-6"
              />
            )}

            <Card className="space-y-6">
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {/* Recipient Info */}
                <div>
                  <h3 className="text-subheading text-dark mb-4">Recipient Information</h3>
                  <div className="space-y-4">
                    <Input
                      label="Recipient Name"
                      placeholder="John Doe"
                      {...register("receiver_name", { required: "Name is required" })}
                      error={errors.receiver_name?.message}
                    />
                    <Input
                      label="Phone Number"
                      type="tel"
                      placeholder="+234..."
                      {...register("receiver_phone", { required: "Phone is required" })}
                      error={errors.receiver_phone?.message}
                    />
                    <Input
                      label="Email Address"
                      type="email"
                      placeholder="john@example.com"
                      {...register("receiver_email", { required: "Email is required" })}
                      error={errors.receiver_email?.message}
                    />
                  </div>
                </div>

                {/* Delivery Address */}
                <div>
                  <h3 className="text-subheading text-dark mb-4">Delivery Address</h3>
                  <div className="space-y-4">
                    <Input
                      label="Street Address"
                      placeholder="123 Main Street"
                      {...register("delivery_address_street", { required: "Street is required" })}
                      error={errors.delivery_address_street?.message}
                    />
                    <div className="grid grid-cols-2 gap-4">
                      <Input
                        label="City"
                        placeholder="Lagos"
                        {...register("delivery_address_city", { required: "City is required" })}
                        error={errors.delivery_address_city?.message}
                      />
                      <Input
                        label="State"
                        placeholder="Lagos"
                        {...register("delivery_address_state", { required: "State is required" })}
                        error={errors.delivery_address_state?.message}
                      />
                    </div>
                    <Input
                      label="ZIP Code"
                      placeholder="12345"
                      {...register("delivery_address_zipcode", { required: "ZIP code is required" })}
                      error={errors.delivery_address_zipcode?.message}
                    />
                  </div>
                </div>

                {/* Package Info */}
                <div>
                  <h3 className="text-subheading text-dark mb-4">Package Information</h3>
                  <div className="space-y-4">
                    <Input
                      label="Description"
                      placeholder="What are you sending?"
                      {...register("description", { required: "Description is required" })}
                      error={errors.description?.message}
                    />
                    <Input
                      label="Weight (kg)"
                      type="number"
                      placeholder="2.5"
                      {...register("weight", { required: "Weight is required" })}
                      error={errors.weight?.message}
                    />
                    <Input
                      label="Special Instructions"
                      placeholder="Fragile, Handle with care..."
                      {...register("special_instructions")}
                      error={errors.special_instructions?.message}
                    />
                  </div>
                </div>

                <div className="flex gap-4 pt-6">
                  <Button
                    type="submit"
                    variant="primary"
                    size="lg"
                    className="flex-1"
                    isLoading={isLoading}
                  >
                    Continue to Payment
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    size="lg"
                    className="flex-1"
                    onClick={() => router.back()}
                  >
                    Cancel
                  </Button>
                </div>
              </form>
            </Card>
          </div>
        </div>
      </main>
    </ProtectedRoute>
  );
}
