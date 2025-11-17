import React, { useState, useEffect } from 'react';
import { BarChart3, Users, TrendingUp, DollarSign, Activity } from 'lucide-react';

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const loadMetrics = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('http://localhost:8000/admin/dashboard', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const data = await response.json();
        setMetrics(data);
      } catch (error) {
        console.error('Failed to load metrics:', error);
      } finally {
        setLoading(false);
      }
    };
    loadMetrics();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <main className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-2">Real-time analytics and management</p>
        </div>

        {/* Tabs */}
        <div className="flex space-x-4 mb-8 border-b border-gray-200">
          {['overview', 'users', 'revenue', 'features'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 font-semibold ${
                activeTab === tab
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && metrics && (
          <div className="space-y-8">
            {/* Key Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Total Users</p>
                    <p className="text-3xl font-bold text-gray-900 mt-1">
                      {metrics.total_users}
                    </p>
                  </div>
                  <Users className="w-12 h-12 text-blue-500 opacity-50" />
                </div>
                <p className="text-green-600 text-sm mt-4">+12% from last month</p>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Active Today</p>
                    <p className="text-3xl font-bold text-gray-900 mt-1">
                      {metrics.active_users_today}
                    </p>
                  </div>
                  <Activity className="w-12 h-12 text-green-500 opacity-50" />
                </div>
                <p className="text-gray-600 text-sm mt-4">
                  {((metrics.active_users_today / metrics.total_users) * 100).toFixed(1)}% of users
                </p>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Total Revenue</p>
                    <p className="text-3xl font-bold text-gray-900 mt-1">
                      ${metrics.total_revenue.toFixed(2)}
                    </p>
                  </div>
                  <DollarSign className="w-12 h-12 text-purple-500 opacity-50" />
                </div>
                <p className="text-green-600 text-sm mt-4">+8% from last month</p>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Conversion Rate</p>
                    <p className="text-3xl font-bold text-gray-900 mt-1">
                      {(metrics.conversion_rate * 100).toFixed(1)}%
                    </p>
                  </div>
                  <TrendingUp className="w-12 h-12 text-orange-500 opacity-50" />
                </div>
                <p className="text-gray-600 text-sm mt-4">
                  {metrics.total_resumes_generated} resumes generated
                </p>
              </div>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">
                  Feature Usage
                </h3>
                <div className="space-y-4">
                  {[
                    { name: 'Resume Generation', value: 3500, max: 4000 },
                    { name: 'Interview Prep', value: 890, max: 1200 },
                    { name: 'ATS Optimization', value: 1200, max: 1500 }
                  ].map(feature => (
                    <div key={feature.name}>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-700 font-medium">{feature.name}</span>
                        <span className="text-gray-600">{feature.value.toLocaleString()}</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${(feature.value / feature.max) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">
                  Subscription Plans
                </h3>
                <div className="space-y-3">
                  {[
                    { plan: 'Basic', users: 300, revenue: '$2,970' },
                    { plan: 'Pro', users: 450, revenue: '$8,995' },
                    { plan: 'Enterprise', users: 50, revenue: '$2,500' }
                  ].map(sub => (
                    <div key={sub.plan} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                      <div>
                        <p className="font-medium text-gray-900">{sub.plan}</p>
                        <p className="text-sm text-gray-600">{sub.users} subscribers</p>
                      </div>
                      <p className="font-bold text-gray-900">{sub.revenue}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Users Management</h3>
            <p className="text-gray-600">User management features coming soon...</p>
          </div>
        )}

        {/* Revenue Tab */}
        {activeTab === 'revenue' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Revenue Metrics</h3>
            <p className="text-gray-600">Revenue analytics coming soon...</p>
          </div>
        )}

        {/* Features Tab */}
        {activeTab === 'features' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Feature Analytics</h3>
            <p className="text-gray-600">Feature usage analytics coming soon...</p>
          </div>
        )}
      </div>
    </main>
  );
}
