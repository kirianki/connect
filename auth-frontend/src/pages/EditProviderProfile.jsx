// src/pages/EditProviderProfile.jsx
import { useState, useEffect, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchProviderProfileByUser, updateProviderProfile } from '../api/marketplaceService'
import { AuthContext } from '../context/AuthContext'

const EditProviderProfile = () => {
  const navigate = useNavigate()
  const { user } = useContext(AuthContext)
  const [formData, setFormData] = useState({
    business_name: '',
    address: '',
    sector: '',
    subcategory: '',
    description: '',
    website: '',
    county: '',
    subcounty: '',
    town: '',
    tags: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadProviderProfile = async () => {
      try {
        const data = await fetchProviderProfileByUser(user.id)
        if (data) {
          setFormData({
            business_name: data.business_name || '',
            address: data.address || '',
            sector: data.sector || '',
            subcategory: data.subcategory || '',
            description: data.description || '',
            website: data.website || '',
            county: data.county || '',
            subcounty: data.subcounty || '',
            town: data.town || '',
            tags: data.tags || ''
          })
        }
      } catch (err) {
        console.error(err)
        setError('Failed to load provider profile')
      } finally {
        setLoading(false)
      }
    }
    if (user && user.id) {
      loadProviderProfile()
    }
  }, [user])

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await updateProviderProfile(formData)
      setLoading(false)
      navigate('/profile')
    } catch (err) {
      console.error(err)
      setError('Failed to update provider profile')
      setLoading(false)
    }
  }

  if (loading) return <p>Loading provider profile...</p>

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Edit Provider Profile</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block mb-1">Business Name</label>
          <input
            type="text"
            name="business_name"
            value={formData.business_name}
            onChange={handleChange}
            required
            className="w-full border rounded p-2"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">Address</label>
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleChange}
            required
            className="w-full border rounded p-2"
          />
        </div>
        {/* You can include sector and subcategory selection here if desired */}
        <div className="mb-4">
          <label className="block mb-1">Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            className="w-full border rounded p-2"
          ></textarea>
        </div>
        <div className="mb-4">
          <label className="block mb-1">Website</label>
          <input
            type="url"
            name="website"
            value={formData.website}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">County</label>
          <input
            type="text"
            name="county"
            value={formData.county}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">Subcounty</label>
          <input
            type="text"
            name="subcounty"
            value={formData.subcounty}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">Town</label>
          <input
            type="text"
            name="town"
            value={formData.town}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">Tags</label>
          <input
            type="text"
            name="tags"
            value={formData.tags}
            onChange={handleChange}
            placeholder="Comma separated tags"
            className="w-full border rounded p-2"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          {loading ? 'Saving...' : 'Save Changes'}
        </button>
      </form>
    </div>
  )
}

export default EditProviderProfile
