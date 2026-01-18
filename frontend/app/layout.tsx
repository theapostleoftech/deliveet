import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Deliveet - On-Demand Package Delivery",
  description: "Fast, reliable, and affordable package delivery service",
  keywords: "delivery, package, courier, shipping",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-white">
        <main>{children}</main>
      </body>
    </html>
  );
}
