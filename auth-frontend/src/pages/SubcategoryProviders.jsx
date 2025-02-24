// src/pages/SubcategoryProviders.jsx
import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchProviderProfiles } from '../api/marketplaceService'

const SubcategoryProviders = () => {
  const { subcategoryId } = useParams()
  const [providers, setProviders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadProviders = async () => {
      try {
        // Assumes fetchProviderProfiles accepts a query object to filter by subcategory
        const data = await fetchProviderProfiles({ subcategory: subcategoryId })
        setProviders(data)
      } catch (err) {
        console.error(err)
        setError('Failed to load providers')
      } finally {
        setLoading(false)
      }
    }
    loadProviders()
  }, [subcategoryId])

  if (loading) return <p>Loading providers...</p>
  if (error) return <p className="text-red-500">{error}</p>

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Providers</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {providers.map(provider => (
          <Link
            key={provider.id}
            to={`/providers/${provider.id}`}
            className="block border rounded overflow-hidden shadow hover:shadow-lg transition"
          >
            {/* If provider has a thumbnail property or use first portfolio image as thumbnail */}
            {provider.thumbnail ? (
              <img 
                src={provider.thumbnail}
                alt={provider.business_name}
                className="w-full h-40 object-cover"
              />
            ) : (
              <div className="w-full h-40 bg-gray-300 flex items-center justify-center">
                <span className="text-gray-700">No Image</span>
              </div>
            )}
            <div className="p-4">
              <h2 className="text-xl font-semibold">{provider.business_name}</h2>
              <p className="text-sm text-gray-600">{provider.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default SubcategoryProviders
