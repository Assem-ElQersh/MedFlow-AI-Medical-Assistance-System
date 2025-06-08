import axios from 'axios';

const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const endpoints = {
  auth: {
    login: '/auth/login',
    logout: '/auth/logout',
    me: '/auth/me',
  },
  patients: {
    list: '/patients',
    create: '/patients',
    get: (id: string) => `/patients/${id}`,
    update: (id: string) => `/patients/${id}`,
    delete: (id: string) => `/patients/${id}`,
  },
  diagnosis: {
    analyze: '/diagnosis/analyze',
    history: '/diagnosis/history',
    get: (id: string) => `/diagnosis/${id}`,
  },
  radiology: {
    analyze: '/radiology/analyze',
    history: '/radiology/history',
    get: (id: string) => `/radiology/${id}`,
  },
  emergency: {
    detect: '/emergency/detect',
    respond: '/emergency/respond',
    history: '/emergency/history',
  },
  specialists: {
    list: '/specialists',
    match: '/specialists/match',
    get: (id: string) => `/specialists/${id}`,
  },
};

// API service functions
export const apiService = {
  // Auth
  login: async (email: string, password: string) => {
    const response = await api.post(endpoints.auth.login, { email, password });
    return response.data;
  },
  
  logout: async () => {
    const response = await api.post(endpoints.auth.logout);
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await api.get(endpoints.auth.me);
    return response.data;
  },
  
  // Patients
  getPatients: async () => {
    const response = await api.get(endpoints.patients.list);
    return response.data;
  },
  
  getPatient: async (id: string) => {
    const response = await api.get(endpoints.patients.get(id));
    return response.data;
  },
  
  createPatient: async (data: any) => {
    const response = await api.post(endpoints.patients.create, data);
    return response.data;
  },
  
  updatePatient: async (id: string, data: any) => {
    const response = await api.put(endpoints.patients.update(id), data);
    return response.data;
  },
  
  deletePatient: async (id: string) => {
    const response = await api.delete(endpoints.patients.delete(id));
    return response.data;
  },
  
  // Diagnosis
  analyzeDiagnosis: async (data: any) => {
    const response = await api.post(endpoints.diagnosis.analyze, data);
    return response.data;
  },
  
  getDiagnosisHistory: async () => {
    const response = await api.get(endpoints.diagnosis.history);
    return response.data;
  },
  
  getDiagnosis: async (id: string) => {
    const response = await api.get(endpoints.diagnosis.get(id));
    return response.data;
  },
  
  // Radiology
  analyzeRadiology: async (data: any) => {
    const response = await api.post(endpoints.radiology.analyze, data);
    return response.data;
  },
  
  getRadiologyHistory: async () => {
    const response = await api.get(endpoints.radiology.history);
    return response.data;
  },
  
  getRadiology: async (id: string) => {
    const response = await api.get(endpoints.radiology.get(id));
    return response.data;
  },
  
  // Emergency
  detectEmergency: async (data: any) => {
    const response = await api.post(endpoints.emergency.detect, data);
    return response.data;
  },
  
  respondToEmergency: async (data: any) => {
    const response = await api.post(endpoints.emergency.respond, data);
    return response.data;
  },
  
  getEmergencyHistory: async () => {
    const response = await api.get(endpoints.emergency.history);
    return response.data;
  },
  
  // Specialists
  getSpecialists: async () => {
    const response = await api.get(endpoints.specialists.list);
    return response.data;
  },
  
  matchSpecialists: async (data: any) => {
    const response = await api.post(endpoints.specialists.match, data);
    return response.data;
  },
  
  getSpecialist: async (id: string) => {
    const response = await api.get(endpoints.specialists.get(id));
    return response.data;
  },
}; 