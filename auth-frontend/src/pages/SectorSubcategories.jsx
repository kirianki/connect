// src/pages/SectorSubcategories.jsx
import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { fetchSubcategories } from '../api/marketplaceService'

const SectorSubcategories = () => {
  const { sectorId } = useParams()
  const [subcategories, setSubcategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadSubcategories = async () => {
      try {
        // Assumes fetchSubcategories accepts a query object to filter by sector
        const data = await fetchSubcategories({ sector: sectorId })
        setSubcategories(data)
      } catch (err) {
        console.error(err)
        setError('Failed to load subcategories')
      } finally {
        setLoading(false)
      }
    }
    loadSubcategories()
  }, [sectorId])

  if (loading) return <p>Loading subcategories...</p>
  if (error) return <p className="text-red-500">{error}</p>

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Subcategories</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {subcategories.map(sub => (
          <Link 
            key={sub.id}
            to={`/subcategories/${sub.id}/providers`}
            className="block border rounded overflow-hidden shadow hover:shadow-lg transition"
          >
            {sub.thumbnail ? (
              <img 
                src={sub.thumbnail} 
                alt={sub.name} 
                className="w-full h-40 object-cover"
              />
            ) : (
              <div className="w-full h-40 bg-gray-300 flex items-center justify-center">
                <span className="text-gray-700">No Image</span>
              </div>
            )}
            <div className="p-4">
              <h2 className="text-xl font-semibold">{sub.name}</h2>
              <p className="text-sm text-gray-600">{sub.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default SectorSubcategories
