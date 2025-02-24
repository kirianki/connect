// src/pages/Providers.jsx
import { useEffect, useState } from 'react'
import { fetchProviderProfiles } from '../api/marketplaceService'
import { Link } from 'react-router-dom'

const Providers = () => {
  const [providers, setProviders] = useState([])

  useEffect(() => {
    const loadProviders = async () => {
      const data = await fetchProviderProfiles()
      setProviders(data)
    }
    loadProviders()
  }, [])

  return (
    <div>
      <h1>Service Providers</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
        {providers.map(provider => (
          <div key={provider.id} style={{ border: '1px solid #ddd', padding: '10px', width: '300px' }}>
            <h3>{provider.business_name}</h3>
            <p>{provider.description}</p>
            <Link to={`/providers/${provider.id}`}>View Details</Link>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Providers
