// src/components/Layout/Navbar.jsx
import { useContext } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { AuthContext } from '../../context/AuthContext'

const Navbar = () => {
  const { user, logout } = useContext(AuthContext)
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/')
  }

  return (
    <nav style={{ padding: '10px 20px', backgroundColor: '#333', color: '#fff' }}>
      <div className="nav-brand">
        <Link to="/" style={{ color: '#fff', textDecoration: 'none', fontSize: '24px' }}>
          Marketplace
        </Link>
      </div>
      <div className="nav-links" style={{ float: 'right' }}>
        <Link to="/" style={{ margin: '0 10px', color: '#fff' }}>Home</Link>
        <Link to="/providers" style={{ margin: '0 10px', color: '#fff' }}>Providers</Link>
        {user ? (
          <>
            <Link to="/profile" style={{ margin: '0 10px', color: '#fff' }}>Profile</Link>
            <Link to="/messages" style={{ margin: '0 10px', color: '#fff' }}>Messages</Link>
            <Link to="/bookings" style={{ margin: '0 10px', color: '#fff' }}>Bookings</Link>
            <button onClick={handleLogout} style={{ margin: '0 10px' }}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ margin: '0 10px', color: '#fff' }}>Login</Link>
            <Link to="/register" style={{ margin: '0 10px', color: '#fff' }}>Register</Link>
          </>
        )}
      </div>
    </nav>
  )
}

export default Navbar
