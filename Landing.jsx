import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { Button } from '../components/common/Button'
import {
  Zap,
  Code2,
  Rocket,
  ArrowRight,
  Check,
  Sparkles,
} from 'lucide-react'
import axios from "axios";
export function Landing() {
  const { isAuthenticated } = useAuth()

  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered Generation',
      description: 'Describe your app idea and let AI generate it for you',
    },
    {
      icon: Code2,
      title: 'Full-Stack Development',
      description: 'Frontend, backend, and database setup automatically',
    },
    {
      icon: Rocket,
      title: 'One-Click Deployment',
      description: 'Deploy to Vercel with a single click',
    },
    {
      icon: Zap,
      title: 'AI Chat Assistant',
      description: 'Modify your app by chatting with the AI',
    },
  ]

  const steps = [
    { number: '1', title: 'Describe', description: 'Describe your application idea' },
    { number: '2', title: 'Generate', description: 'AI creates the complete application' },
    { number: '3', title: 'Edit', description: 'Fine-tune the code with AI assistance' },
    { number: '4', title: 'Deploy', description: 'Deploy instantly to production' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-dark to-gray-900">
      {/* Navbar is handled by Layout */}

      {/* Hero Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 md:py-32 max-w-7xl mx-auto">
        <div className="text-center space-y-6">
          <div className="inline-block">
            <span className="px-4 py-1.5 bg-blue-600 bg-opacity-20 border border-blue-600 text-blue-400 rounded-full text-sm font-medium">
              ✨ Build apps with AI
            </span>
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-white leading-tight">
            Generate Your Next App
            <br />
            <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              with AI
            </span>
          </h1>

          <p className="text-lg md:text-xl text-gray-400 max-w-3xl mx-auto">
            Describe your application in natural language and let AI generate the complete
            source code. Edit with our IDE, test instantly, and deploy to production.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard">
                  <Button variant="primary" size="lg" className="group">
                    Go to Dashboard
                    <ArrowRight size={20} className="ml-2 group-hover:translate-x-1 transition" />
                  </Button>
                </Link>
              </>
            ) : (
              <>
                <Link to="/register">
                  <Button variant="primary" size="lg" className="group">
                    Get Started Free
                    <ArrowRight size={20} className="ml-2 group-hover:translate-x-1 transition" />
                  </Button>
                </Link>
                <Link to="/login">
                  <Button variant="outline" size="lg">
                    Sign In
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-white text-center mb-16">
          Powerful Features
        </h2>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature) => {
            const Icon = feature.icon
            return (
              <div
                key={feature.title}
                className="p-6 rounded-lg border border-gray-800 bg-gray-900 bg-opacity-50 hover:border-gray-700 hover:bg-opacity-80 transition"
              >
                <Icon className="text-blue-400 mb-4" size={32} />
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-400 text-sm">{feature.description}</p>
              </div>
            )
          })}
        </div>
      </section>

      {/* How It Works */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-white text-center mb-16">
          How It Works
        </h2>

        <div className="grid md:grid-cols-4 gap-6">
          {steps.map((step) => (
            <div key={step.number} className="relative">
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-lg mb-4">
                  {step.number}
                </div>
                <h3 className="text-lg font-semibold text-white text-center mb-2">
                  {step.title}
                </h3>
                <p className="text-gray-400 text-sm text-center">{step.description}</p>
              </div>
              {step.number !== '4' && (
                <div className="hidden md:block absolute top-6 left-full w-6 h-0.5 bg-gradient-to-r from-blue-600 to-transparent" />
              )}
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 max-w-4xl mx-auto">
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to build your next app?
          </h2>
          <p className="text-blue-100 mb-8 text-lg">
            Join thousands of developers using AI to build apps faster
          </p>
          {!isAuthenticated && (
            <Link to="/register">
              <Button variant="primary" size="lg" className="bg-white text-blue-600 hover:bg-gray-100">
                Start Building Now
              </Button>
            </Link>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 mt-20">
        <div className="px-4 sm:px-6 lg:px-8 py-12 max-w-7xl mx-auto">
          <p className="text-center text-gray-500 text-sm">
            © 2024 AI App Generator. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  )
}
export default Landing;