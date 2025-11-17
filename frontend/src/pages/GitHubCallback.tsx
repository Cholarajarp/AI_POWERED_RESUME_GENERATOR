import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { authAPI } from '../services/api';

export default function GitHubCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [error, setError] = React.useState('');

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const state = searchParams.get('state');

      if (!code) {
        setError('No authorization code received');
        return;
      }

      try {
        const response = await authAPI.githubCallback(code);
        localStorage.setItem('access_token', response.data.access_token);
        navigate('/dashboard');
      } catch (err: any) {
        setError(err.response?.data?.detail || 'GitHub authentication failed');
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center">
          <h2 className="text-xl font-bold text-red-600 mb-2">Authentication Failed</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <a href="/login" className="text-blue-600 hover:text-blue-700">
            Back to Login
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Authenticating with GitHub...</p>
      </div>
    </div>
  );
}
