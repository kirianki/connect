// src/pages/Home.jsx
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchSectors, fetchProviderProfiles } from '../api/marketplaceService'

const Home = () => {
  const [sectors, setSectors] = useState([])
  const [featuredProviders, setFeaturedProviders] = useState([])

  useEffect(() => {
    const loadData = async () => {
      try {
        const sectorsData = await fetchSectors()
        setSectors(sectorsData)
        // Example: fetch providers with featured flag (adjust query parameters as needed)
        const providersData = await fetchProviderProfiles({ is_featured: true })
        setFeaturedProviders(providersData)
      } catch (error) {
        console.error("Error loading data:", error)
      }
    }
    loadData()
  }, [])

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold mb-6">Welcome to the Marketplace</h1>

      {/* Featured Providers Section */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">Featured Providers</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {featuredProviders.map(provider => (
            <div key={provider.id} className="border p-4 rounded shadow">
              <h3 className="text-xl font-bold">{provider.business_name}</h3>
              <p className="text-gray-600">{provider.description}</p>
              <a
                href={`/providers/${provider.id}`}
                className="text-blue-500 hover:underline mt-2 inline-block"
              >
                View Details
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* Sectors Section */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Sectors</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {sectors.map(sector => (
            <Link 
              to={`/sectors/${sector.id}/subcategories`} 
              key={sector.id}
              className="block border rounded overflow-hidden shadow hover:shadow-lg transition"
            >
              {sector.thumbnail ? (
                <img 
                  src={sector.thumbnail} 
                  alt={sector.name} 
                  className="w-full h-40 object-cover"
                />
              ) : (
                <div className="w-full h-40 bg-gray-300 flex items-center justify-center">
                  <span className="text-gray-700">No Image</span>
                </div>
              )}
              <div className="p-4">
                <h3 className="text-xl font-bold">{sector.name}</h3>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}

export default Home
