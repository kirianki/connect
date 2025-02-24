// src/context/AuthContext.jsx
import React, { createContext, useState, useEffect } from 'react';
import axios from '../api/axiosInstance';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [tokens, setTokens] = useState(null);

  useEffect(() => {
    const storedTokens = localStorage.getItem('tokens');
    if (storedTokens) {
      const parsedTokens = JSON.parse(storedTokens);
      setTokens(parsedTokens);
      setUser({
        id: parsedTokens.user_id,
        username: parsedTokens.username,
        email: parsedTokens.email,
        role: parsedTokens.role,
        roleDisplay: parsedTokens.role_display,
      });
    }
  }, []);

  const login = async (credentials) => {
    try {
      const response = await axios.post('/accounts/auth/token/', credentials);
      setTokens(response.data);
      setUser({
        id: response.data.user_id,
        username: response.data.username,
        email: response.data.email,
        role: response.data.role,
        roleDisplay: response.data.role_display,
      });
      localStorage.setItem('tokens', JSON.stringify(response.data));
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data || error.message };
    }
  };

  const logout = async () => {
    setTokens(null);
    setUser(null);
    localStorage.removeItem('tokens');
  };

  const register = async (data) => {
    try {
      const response = await axios.post('/accounts/auth/register/', data);
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, message: error.response?.data || error.message };
    }
  };

  return (
    <AuthContext.Provider value={{ user, tokens, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};
