/// <reference types="vite/client" />
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for handling token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);
        
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data: any) => api.post('/auth/register', data),
  login: (data: any) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  googleLogin: (token: string) => api.post('/auth/google/callback', { token }),
  githubCallback: (code: string) => api.post('/auth/github/callback', { code }),
};

export const resumeAPI = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  list: () => api.get('/resume/list'),
  get: (id: string) => api.get(`/resume/${id}`),
  delete: (id: string) => api.delete(`/resume/${id}`),
  analyze: (id: string) => api.post(`/resume/${id}/analyze`),
};

export const atsAPI = {
  score: (resumeId: string, jobDescription: string) =>
    api.post('/ats/score', { resume_id: resumeId, job_description: jobDescription }),
  optimize: (resumeId: string, jobDescription: string) =>
    api.post('/ats/optimize', { resume_id: resumeId, job_description: jobDescription }),
};

export const interviewAPI = {
  createSession: (data: any) => api.post('/interview/session/create', data),
  submitAnswer: (sessionId: string, answer: string) =>
    api.post(`/interview/session/${sessionId}/submit_answer`, { answer }),
  getSession: (sessionId: string) => api.get(`/interview/session/${sessionId}`),
};

export const jobAPI = {
  parse: (description: string) => api.post('/job/parse', { description }),
  match: (resumeId: string) => api.post('/job/match', { resume_id: resumeId }),
};

export const templatesAPI = {
  list: (category?: string) => api.get('/templates', { params: { category } }),
  get: (templateId: number) => api.get(`/templates/${templateId}`),
  generate: (data: any) => api.post('/templates/generate', data),
};

export default api;
