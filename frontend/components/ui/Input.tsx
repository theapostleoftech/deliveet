"use client";

import React, { ReactNode } from "react";
import clsx from "clsx";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
  icon?: ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, hint, icon, className, ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label htmlFor={props.id} className="text-sm font-medium text-dark">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          <input
            ref={ref}
            className={clsx(
              "w-full rounded-lg border px-4 py-2 text-dark placeholder-gray-400 transition-all focus:outline-none",
              error
                ? "border-red-500 focus:border-red-500 focus:ring-1 focus:ring-red-500"
                : "border-light focus:border-primary-500 focus:ring-1 focus:ring-primary-500",
              icon && "pl-10",
              className
            )}
            {...props}
          />
          {icon && <div className="absolute left-3 top-2.5 text-gray-400">{icon}</div>}
        </div>
        {error && <p className="text-sm text-red-500">{error}</p>}
        {hint && <p className="text-sm text-gray-500">{hint}</p>}
      </div>
    );
  }
);

Input.displayName = "Input";
