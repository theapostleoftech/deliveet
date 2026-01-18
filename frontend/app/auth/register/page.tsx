"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { useAuthStore } from "@/store/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Alert } from "@/components/ui/Alert";
import Link from "next/link";

interface RegisterFormData {
  email: string;
  password: string;
  password2: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  role: "customer" | "courier";
}

export default function RegisterPage() {
  const router = useRouter();
  const { register: registerUser, isLoading, error, clearError } = useAuthStore();
  const { register, handleSubmit, formState: { errors }, watch } = useForm<RegisterFormData>({
    defaultValues: {
      role: "customer",
    },
  });

  const password = watch("password");

  const onSubmit = async (data: RegisterFormData) => {
    try {
      await registerUser(data);
      router.push("/dashboard/customer");
    } catch (err) {
      // Error is already set in store
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center p-4 py-8">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="text-center mb-8">
            <div className="inline-block h-12 w-12 rounded-lg bg-gradient-to-r from-primary-500 to-secondary-500 mb-4"></div>
            <h1 className="text-heading text-dark">Create Account</h1>
            <p className="text-small text-gray-500 mt-2">Join Deliveet today</p>
          </div>

          {error && (
            <Alert
              type="error"
              message={error}
              onClose={clearError}
              className="mb-6"
            />
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Input
                label="First Name"
                placeholder="John"
                {...register("first_name", {
                  required: "First name is required",
                })}
                error={errors.first_name?.message}
              />
              <Input
                label="Last Name"
                placeholder="Doe"
                {...register("last_name", {
                  required: "Last name is required",
                })}
                error={errors.last_name?.message}
              />
            </div>

            <Input
              label="Email Address"
              type="email"
              placeholder="you@example.com"
              {...register("email", {
                required: "Email is required",
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: "Invalid email address",
                },
              })}
              error={errors.email?.message}
            />

            <Input
              label="Phone Number"
              type="tel"
              placeholder="+1234567890"
              {...register("phone_number", {
                required: "Phone number is required",
              })}
              error={errors.phone_number?.message}
            />

            <div>
              <label className="text-sm font-medium text-dark block mb-2">
                Account Type
              </label>
              <div className="flex gap-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="customer"
                    {...register("role")}
                    className="mr-2"
                  />
                  <span className="text-sm text-dark">Customer</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="courier"
                    {...register("role")}
                    className="mr-2"
                  />
                  <span className="text-sm text-dark">Courier</span>
                </label>
              </div>
            </div>

            <Input
              label="Password"
              type="password"
              placeholder="••••••••"
              {...register("password", {
                required: "Password is required",
                minLength: {
                  value: 8,
                  message: "Password must be at least 8 characters",
                },
                pattern: {
                  value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
                  message: "Password must contain uppercase, lowercase, and numbers",
                },
              })}
              error={errors.password?.message}
            />

            <Input
              label="Confirm Password"
              type="password"
              placeholder="••••••••"
              {...register("password2", {
                required: "Please confirm password",
                validate: (value) =>
                  value === password || "Passwords do not match",
              })}
              error={errors.password2?.message}
            />

            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="w-full"
              isLoading={isLoading}
            >
              Create Account
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-small text-gray-600">
              Already have an account?{" "}
              <Link href="/auth/login" className="text-primary-500 hover:text-primary-600 font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
