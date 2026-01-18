"use client";

import React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Navbar } from "@/components/common/Navbar";

export default function Home() {
  const router = useRouter();
  const { isAuthenticated, user } = useAuthStore();

  React.useEffect(() => {
    if (isAuthenticated && user) {
      if (user.role === "customer") {
        router.push("/dashboard/customer");
      } else if (user.role === "courier") {
        router.push("/dashboard/courier");
      }
    }
  }, [isAuthenticated, user, router]);

  return (
    <>
      <Navbar />
      <main className="bg-gradient-to-br from-white via-blue-50 to-orange-50">
        {/* Hero Section */}
        <section className="container-fluid py-20 md:py-32">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-display text-dark mb-6">
                Fast & Reliable Delivery
                <span className="text-gradient"> Right at Your Doorstep</span>
              </h1>
              <p className="text-body text-gray-600 mb-8 leading-relaxed">
                Send packages with confidence. Deliveet offers same-day delivery, real-time
                tracking, and competitive pricing for individuals and businesses.
              </p>
              <div className="flex flex-wrap gap-4">
                <Button
                  variant="primary"
                  size="lg"
                  onClick={() => router.push("/auth/register")}
                >
                  Get Started
                </Button>
                <Button variant="outline" size="lg" onClick={() => router.push("/about")}>
                  Learn More
                </Button>
              </div>
            </div>
            <div className="relative h-96 md:h-full rounded-2xl overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-primary-500 to-secondary-500 opacity-10"></div>
              <div className="absolute top-10 left-10 w-32 h-32 bg-primary-200 rounded-full blur-3xl opacity-30"></div>
              <div className="absolute bottom-10 right-10 w-40 h-40 bg-secondary-200 rounded-full blur-3xl opacity-30"></div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="container-fluid py-16 md:py-24">
          <h2 className="text-heading text-center text-dark mb-16">Why Choose Deliveet?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: "⚡",
                title: "Lightning Fast",
                description: "Get your packages delivered the same day with our express service.",
              },
              {
                icon: "📍",
                title: "Real-time Tracking",
                description: "Know exactly where your package is with live GPS tracking.",
              },
              {
                icon: "💰",
                title: "Affordable",
                description: "Competitive prices without compromising on quality or reliability.",
              },
              {
                icon: "🔒",
                title: "Secure",
                description: "Your packages are insured and handled with the utmost care.",
              },
              {
                icon: "📱",
                title: "Easy to Use",
                description: "Simple booking process in just a few taps.",
              },
              {
                icon: "👥",
                title: "24/7 Support",
                description: "Our customer support team is always ready to help.",
              },
            ].map((feature, idx) => (
              <Card key={idx} hoverable>
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-subheading text-dark mb-2">{feature.title}</h3>
                <p className="text-body text-gray-600">{feature.description}</p>
              </Card>
            ))}
          </div>
        </section>

        {/* CTA Section */}
        <section className="container-fluid py-16 md:py-24">
          <Card className="bg-gradient-to-r from-primary-500 to-secondary-500 text-white border-0">
            <div className="text-center">
              <h2 className="text-heading text-white mb-4">Ready to Send Your First Delivery?</h2>
              <p className="text-body text-white/90 mb-8">
                Join thousands of satisfied customers who trust Deliveet.
              </p>
              <Button variant="primary" size="lg" onClick={() => router.push("/auth/register")}>
                Create Account Free
              </Button>
            </div>
          </Card>
        </section>

        {/* Footer */}
        <footer className="border-t border-light bg-gray-50 py-12">
          <div className="container-fluid">
            <div className="grid md:grid-cols-4 gap-8 mb-8">
              <div>
                <h4 className="font-bold text-dark mb-4">Deliveet</h4>
                <p className="text-small text-gray-600">Fast, reliable, and affordable delivery.</p>
              </div>
              <div>
                <h4 className="font-bold text-dark mb-4">Company</h4>
                <ul className="space-y-2 text-small text-gray-600">
                  <li>
                    <Link href="/about" className="hover:text-primary-500">
                      About
                    </Link>
                  </li>
                  <li>
                    <Link href="/careers" className="hover:text-primary-500">
                      Careers
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="font-bold text-dark mb-4">Legal</h4>
                <ul className="space-y-2 text-small text-gray-600">
                  <li>
                    <Link href="/privacy" className="hover:text-primary-500">
                      Privacy
                    </Link>
                  </li>
                  <li>
                    <Link href="/terms" className="hover:text-primary-500">
                      Terms
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="font-bold text-dark mb-4">Contact</h4>
                <p className="text-small text-gray-600">support@deliveet.com</p>
              </div>
            </div>
            <div className="border-t border-light pt-8 text-center text-small text-gray-500">
              <p>&copy; 2024 Deliveet. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </main>
    </>
  );
}
