// src/pages/Profile.jsx
import { useEffect, useState, useContext } from 'react'
import { fetchProfile } from "../api/AuthService"
import { fetchProviderProfileByUser } from "../api/marketplaceService"
import { AuthContext } from '../context/AuthContext'
import { Link } from 'react-router-dom'

const Profile = () => {
  const { user } = useContext(AuthContext)
  const [profile, setProfile] = useState(null)
  const [providerProfile, setProviderProfile] = useState(null)

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const data = await fetchProfile()
        setProfile(data)
      } catch (err) {
        console.error(err)
      }
    }
    loadProfile()
  }, [])

  useEffect(() => {
    if (user && user.id) {
      const loadProviderProfile = async () => {
        try {
          const data = await fetchProviderProfileByUser(user.id)
          setProviderProfile(data)
        } catch (err) {
          console.error(err)
        }
      }
      loadProviderProfile()
    }
  }, [user])

  if (!profile) return <p>Loading profile...</p>

  // Check if provider profile exists and is complete.
  const hasProviderProfile = providerProfile && Object.keys(providerProfile).length > 0
  const isProviderProfileComplete = hasProviderProfile &&
    !!providerProfile.business_name &&
    !!providerProfile.address

  return (
    <div>
      <h1>My Profile</h1>
      <div>
        <p><strong>ID:</strong> {profile.id}</p>
        <p><strong>Username:</strong> {profile.username}</p>
        <p><strong>Email:</strong> {profile.email}</p>
        <p>
          <strong>Role:</strong> {profile.role} ({profile.role_display})
        </p>
        <p><strong>First Name:</strong> {profile.first_name}</p>
        <p><strong>Last Name:</strong> {profile.last_name}</p>
      </div>

      {profile.role === "service_provider" && (
        <div style={{ marginTop: '2rem', borderTop: '1px solid #ccc', paddingTop: '1rem' }}>
          <h2>Service Provider Dashboard</h2>
          {hasProviderProfile ? (
            <div>
              <h3>Your Provider Profile</h3>
              <p>
                <strong>Business Name:</strong> {providerProfile.business_name}
              </p>
              <p>
                <strong>Address:</strong> {providerProfile.address}
              </p>
              {/* Additional provider profile fields here */}
              <div style={{ marginTop: '1rem' }}>
                <Link to="/provider-profile/edit" style={{ marginRight: '1rem' }}>
                  Edit Provider Profile
                </Link>
                {isProviderProfileComplete ? (
                  <Link to="/listings/create">Create Listing</Link>
                ) : (
                  <p style={{ color: 'red' }}>
                    Your provider profile is incomplete. Please complete your profile to create listings.
                  </p>
                )}
              </div>
            </div>
          ) : (
            <div>
              <p>You haven't created your provider profile yet.</p>
              <Link to="/provider-profile/create">Create Provider Profile</Link>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Profile
