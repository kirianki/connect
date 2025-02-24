// src/api/axiosInstance.js
import axios from 'axios'

const instance = axios.create({
  baseURL: '/api', // Proxy handles the backend URL
})

// Add request interceptor to include JWT token
instance.interceptors.request.use(
  (config) => {
    const tokens = localStorage.getItem('tokens')
    if (tokens) {
      const { access } = JSON.parse(tokens)
      config.headers.Authorization = `Bearer ${access}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

export default instance
