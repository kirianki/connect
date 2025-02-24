import { useContext } from 'react'
import { Link } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

const AdminDashboard = () => {
  const { user } = useContext(AuthContext)

  // Ensure only admin users can access this page
  if (!user || user.role !== 'overall_admin') {
    return <p>Access denied. You are not authorized to view this page.</p>
  }

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <nav>
        <ul>
          <li>
            <Link to="/admin/sectors">Manage Sectors</Link>
          </li>
          <li>
            <Link to="/admin/subcategories">Manage Subcategories</Link>
          </li>
          {/* Add more admin sections as needed */}
        </ul>
      </nav>
    </div>
  )
}

export default AdminDashboard
