// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Layout/Navbar'
import Footer from './components/Layout/Footer'
import PrivateRoute from './components/PrivateRoute'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import Providers from './pages/Providers'
import ProviderDetail from './pages/ProviderDetail'
import Messages from './pages/Messages'
import Bookings from './pages/Bookings'
import Notifications from './pages/Notifications'
import Favorites from './pages/Favorites'
import Reports from './pages/Reports'
import ProviderProfileCreate from './pages/ProviderProfileCreate'
import AdminDashboard from './pages/AdminDashboard'
import ManageSectors from './pages/ManageSectors'
import ManageSubcategories from './pages/ManageSubcategories'
import SectorSubcategories from './pages/SectorSubcategories'
import SubcategoryProviders from './pages/SubcategoryProviders'
import EditProviderProfile from './pages/EditProviderProfile'

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container" style={{ padding: '20px', minHeight: '80vh' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <Profile />
              </PrivateRoute>
            }
          />
          <Route path="/provider-profile/edit" element={<EditProviderProfile />} />
          <Route path="/sectors/:sectorId/subcategories" element={<SectorSubcategories />} />
          <Route path="/subcategories/:subcategoryId/providers" element={<SubcategoryProviders />} />
          {/* Admin routes */}
          <Route path="/admin" element={<PrivateRoute adminOnly><AdminDashboard /></PrivateRoute>} />
          <Route path="/admin/sectors" element={<PrivateRoute><ManageSectors /></PrivateRoute>} />
          <Route path="/admin/subcategories" element={<PrivateRoute><ManageSubcategories /></PrivateRoute>} />
          {/* ... other admin routes */}
          <Route path="/provider-profile/create" element={<ProviderProfileCreate />} />

          <Route path="/providers" element={<Providers />} />
          <Route path="/providers/:id" element={<ProviderDetail />} />

          <Route
            path="/messages"
            element={
              <PrivateRoute>
                <Messages />
              </PrivateRoute>
            }
          />

          <Route
            path="/bookings"
            element={
              <PrivateRoute>
                <Bookings />
              </PrivateRoute>
            }
          />

          <Route
            path="/notifications"
            element={
              <PrivateRoute>
                <Notifications />
              </PrivateRoute>
            }
          />

          <Route
            path="/favorites"
            element={
              <PrivateRoute>
                <Favorites />
              </PrivateRoute>
            }
          />

          <Route
            path="/reports"
            element={
              <PrivateRoute>
                <Reports />
              </PrivateRoute>
            }
          />
        </Routes>
      </div>
      <Footer />
    </Router>
  )
}

export default App
