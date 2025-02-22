import { createContext, useState, useEffect } from "react";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/auth/";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));

  useEffect(() => {
    if (token) {
      axios
        .get(`${API_BASE_URL}user/`, { headers: { Authorization: `Token ${token}` } })
        .then(res => setUser(res.data))
        .catch(() => logout());
    }
  }, [token]);

  const login = async (credentials) => {
    const res = await axios.post(`${API_BASE_URL}login/`, credentials);
    setToken(res.data.token);
    localStorage.setItem("token", res.data.token);
    setUser(res.data.user);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
