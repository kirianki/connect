import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { createProviderProfile, fetchSectors, fetchSubcategories } from '../api/marketplaceService'

const ProviderProfileCreate = () => {
  const navigate = useNavigate()
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

  const [sectors, setSectors] = useState([])
  const [subcategories, setSubcategories] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // Load sectors on mount
  useEffect(() => {
    const loadSectors = async () => {
      try {
        const data = await fetchSectors()
        setSectors(data)
      } catch (err) {
        console.error('Error loading sectors:', err)
      }
    }
    loadSectors()
  }, [])

  // Load subcategories when a sector is selected
  useEffect(() => {
    const loadSubcategories = async () => {
      if (formData.sector) {
        try {
          // We assume fetchSubcategories accepts a parameter for filtering by sector id.
          const data = await fetchSubcategories({ sector: formData.sector })
          setSubcategories(data)
        } catch (err) {
          console.error('Error loading subcategories:', err)
        }
      }
    }
    loadSubcategories()
  }, [formData.sector])

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await createProviderProfile(formData)
      setLoading(false)
      // After successfully creating the profile, navigate to the profile page
      navigate('/profile')
    } catch (err) {
      console.error('Error creating profile:', err)
      setError(err.response?.data || 'An error occurred')
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>Create Provider Profile</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Business Name:</label>
          <input 
            type="text" 
            name="business_name" 
            value={formData.business_name} 
            onChange={handleChange} 
            required 
          />
        </div>
        <div>
          <label>Address:</label>
          <input 
            type="text" 
            name="address" 
            value={formData.address} 
            onChange={handleChange} 
            required 
          />
        </div>
        <div>
          <label>Sector:</label>
          <select 
            name="sector" 
            value={formData.sector} 
            onChange={handleChange} 
            required
          >
            <option value="">Select a sector</option>
            {sectors.map(sector => (
              <option key={sector.id} value={sector.id}>
                {sector.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Subcategory:</label>
          <select 
            name="subcategory" 
            value={formData.subcategory} 
            onChange={handleChange} 
            required
          >
            <option value="">Select a subcategory</option>
            {subcategories.map(sub => (
              <option key={sub.id} value={sub.id}>
                {sub.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Description:</label>
          <textarea 
            name="description" 
            value={formData.description} 
            onChange={handleChange} 
            required
          />
        </div>
        <div>
          <label>Website:</label>
          <input 
            type="url" 
            name="website" 
            value={formData.website} 
            onChange={handleChange} 
          />
        </div>
        <div>
          <label>County:</label>
          <input 
            type="text" 
            name="county" 
            value={formData.county} 
            onChange={handleChange} 
            required 
          />
        </div>
        <div>
          <label>Subcounty:</label>
          <input 
            type="text" 
            name="subcounty" 
            value={formData.subcounty} 
            onChange={handleChange} 
            required 
          />
        </div>
        <div>
          <label>Town:</label>
          <input 
            type="text" 
            name="town" 
            value={formData.town} 
            onChange={handleChange} 
            required 
          />
        </div>
        <div>
          <label>Tags:</label>
          <input 
            type="text" 
            name="tags" 
            value={formData.tags} 
            onChange={handleChange} 
            placeholder="Comma separated tags" 
          />
        </div>
        <div>
          <button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create Profile'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default ProviderProfileCreate
