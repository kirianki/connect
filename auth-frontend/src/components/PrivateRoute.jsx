// src/components/PrivateRoute.jsx
import { useContext } from 'react'
import { Navigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

const PrivateRoute = ({ children, adminOnly = false }) => {
  const { user } = useContext(AuthContext)
  if (!user) return <Navigate to="/login" />
  if (adminOnly && user.role !== 'overall_admin') {
    return <p>Access denied. Admins only.</p>
  }
  return children
}

export default PrivateRoute
