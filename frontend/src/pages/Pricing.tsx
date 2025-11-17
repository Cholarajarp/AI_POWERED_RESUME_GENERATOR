import React, { useState, useEffect } from 'react';
import { Check, Zap } from 'lucide-react';

const plans = [
  {
    id: 'basic',
    name: 'Basic',
    price: '$9.99',
    period: '/month',
    description: 'Perfect for getting started',
    features: [
      '5 resumes per month',
      'Basic AI templates',
      'PDF export',
      'Email support'
    ],
    cta: 'Get Started',
    highlighted: false
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '$19.99',
    period: '/month',
    description: 'For serious job seekers',
    features: [
      'Unlimited resumes',
      'All AI templates',
      'Premium PDF templates',
      'Interview prep module',
      'Priority support'
    ],
    cta: 'Get Pro',
    highlighted: true
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: '$49.99',
    period: '/month',
    description: 'For teams and agencies',
    features: [
      'Everything in Pro',
      'Team collaboration',
      'Custom templates',
      'API access',
      'Dedicated support',
      'Analytics dashboard'
    ],
    cta: 'Contact Sales',
    highlighted: false
  }
];

export default function Pricing() {
  const [selectedPlan, setSelectedPlan] = useState('pro');
  const [loading, setLoading] = useState(false);

  const handleSelectPlan = async (planId: string) => {
    setLoading(true);
    try {
      const userEmail = localStorage.getItem('user_email') || 'user@example.com';
      
      const response = await fetch('http://localhost:8000/payments/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          plan_type: planId,
          email: userEmail
        })
      });

      if (!response.ok) throw new Error('Failed to create checkout session');
      
      const data = await response.json();
      if (data.session_url) {
        window.location.href = data.session_url;
      }
    } catch (error) {
      console.error('Failed to initiate checkout:', error);
      alert('Failed to initiate checkout. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Simple, Transparent Pricing
        </h1>
        <p className="text-xl text-gray-600">
          Choose the perfect plan for your career needs
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8 mb-12">
        {plans.map((plan) => (
          <div
            key={plan.id}
            className={`rounded-2xl shadow-lg transition transform hover:scale-105 ${
              plan.highlighted
                ? 'ring-2 ring-blue-600 relative -top-4 bg-blue-50'
                : 'bg-white'
            }`}
          >
            {plan.highlighted && (
              <div className="bg-blue-600 text-white px-4 py-2 rounded-t-2xl text-center font-semibold">
                Most Popular
              </div>
            )}
            
            <div className="p-8">
              <h3 className="text-2xl font-bold text-gray-900">{plan.name}</h3>
              <p className="text-gray-600 text-sm mt-2">{plan.description}</p>
              
              <div className="mt-6">
                <span className="text-5xl font-bold text-gray-900">
                  {plan.price}
                </span>
                <span className="text-gray-600">{plan.period}</span>
              </div>

              <button
                onClick={() => handleSelectPlan(plan.id)}
                disabled={loading}
                className={`w-full mt-8 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition ${
                  plan.highlighted
                    ? 'bg-blue-600 hover:bg-blue-700 text-white'
                    : 'bg-gray-100 hover:bg-gray-200 text-gray-900'
                } disabled:opacity-50`}
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    <Zap className="w-5 h-5" />
                    {plan.cta}
                  </>
                )}
              </button>

              <ul className="mt-8 space-y-4">
                {plan.features.map((feature, idx) => (
                  <li key={idx} className="flex items-center gap-3">
                    <Check className="w-5 h-5 text-green-500 flex-shrink-0" />
                    <span className="text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-blue-50 rounded-2xl p-8 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Start Your Free Trial
        </h2>
        <p className="text-gray-600 mb-6">
          Get full access to Pro features for 14 days, no credit card required
        </p>
        <button className="px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700">
          Start Free Trial
        </button>
      </div>
    </main>
  );
}
