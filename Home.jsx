import { Link } from "react-router-dom";
import {
  Sparkles,
  Code2,
  Rocket,
  ShieldCheck,
  ArrowRight,
} from "lucide-react";

export default function Home() {
  const features = [
    {
      icon: Sparkles,
      title: "AI Powered",
      description: "Generate complete applications using AI with just a prompt.",
    },
    {
      icon: Code2,
      title: "Full Stack",
      description: "Frontend, Backend and Database generated automatically.",
    },
    {
      icon: Rocket,
      title: "Fast Deployment",
      description: "Build, preview and deploy your application instantly.",
    },
    {
      icon: ShieldCheck,
      title: "Secure",
      description: "Authentication and protected routes built into your project.",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-blue-950 text-white overflow-hidden">

      {/* Background */}
      <div className="absolute top-20 left-20 w-72 h-72 rounded-full bg-blue-600/20 blur-3xl"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 rounded-full bg-purple-600/20 blur-3xl"></div>

      {/* Navbar */}
      <nav className="relative z-20 flex justify-between items-center px-8 py-6 max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
          AI App Generator
        </h1>

        <div className="space-x-4">
          <Link
            to="/login"
            className="px-5 py-2 rounded-lg border border-cyan-400 hover:bg-cyan-500 hover:text-black transition"
          >
            Login
          </Link>

          <Link
            to="/register"
            className="px-5 py-2 rounded-lg bg-cyan-500 text-black font-semibold hover:bg-cyan-400 transition"
          >
            Register
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative z-10 flex flex-col items-center justify-center text-center px-6 py-24 max-w-6xl mx-auto">

        <span className="bg-blue-500/20 border border-blue-500 px-4 py-2 rounded-full text-blue-300 mb-6">
          ✨ Build Smarter with AI
        </span>

        <h1 className="text-5xl md:text-7xl font-extrabold leading-tight mb-6">
          Create Amazing
          <br />
          <span className="bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
            AI Applications
          </span>
        </h1>

        <p className="text-lg md:text-xl text-gray-300 max-w-3xl mb-10">
          Describe your idea, generate a complete application with AI,
          edit it live, and deploy instantly using one powerful platform.
        </p>

        <div className="flex flex-col sm:flex-row gap-5">

          <Link
            to="/login"
            className="flex items-center justify-center bg-cyan-500 hover:bg-cyan-400 text-black font-bold px-8 py-4 rounded-xl transition"
          >
            Get Started
            <ArrowRight className="ml-2" size={20} />
          </Link>

          <Link
            to="/register"
            className="px-8 py-4 rounded-xl border border-cyan-400 hover:bg-cyan-500 hover:text-black transition"
          >
            Create Account
          </Link>

        </div>

      </section>

      {/* Features */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 pb-24">

        <h2 className="text-4xl font-bold text-center mb-14">
          Why Choose Us?
        </h2>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">

          {features.map((feature, index) => {
            const Icon = feature.icon;

            return (
              <div
                key={index}
                className="bg-white/10 backdrop-blur-lg border border-white/10 rounded-2xl p-8 hover:scale-105 transition duration-300"
              >
                <Icon
                  className="text-cyan-400 mb-5"
                  size={42}
                />

                <h3 className="text-xl font-bold mb-3">
                  {feature.title}
                </h3>

                <p className="text-gray-300 text-sm">
                  {feature.description}
                </p>
              </div>
            );
          })}

        </div>

      </section>

      {/* CTA */}
      <section className="relative z-10 max-w-5xl mx-auto px-6 pb-24">

        <div className="rounded-3xl bg-gradient-to-r from-cyan-600 to-purple-600 p-12 text-center shadow-2xl">

          <h2 className="text-4xl font-bold mb-4">
            Start Building Today
          </h2>

          <p className="text-lg text-blue-100 mb-8">
            Join thousands of developers creating powerful AI applications.
          </p>

          <Link
            to="/register"
            className="inline-block bg-white text-blue-700 font-bold px-8 py-4 rounded-xl hover:bg-gray-100 transition"
          >
            Create Free Account
          </Link>

        </div>

      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-8 text-center text-gray-400">

        <p>
          © 2026 AI App Generator. All Rights Reserved.
        </p>

      </footer>

    </div>
  );
}