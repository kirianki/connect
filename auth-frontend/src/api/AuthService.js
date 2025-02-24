// src/api/authService.js
import axios from './axiosInstance'

export const loginUser = async (credentials) => {
  const response = await axios.post('/token/', credentials)
  return response.data
}

export const registerUser = async (data) => {
  const response = await axios.post('/register/', data)
  return response.data
}

export const fetchProfile = async () => {
  const response = await axios.get('/accounts/profile/')
  return response.data
}

// Add other auth-related services as needed (change password, reset, logout, etc.)
