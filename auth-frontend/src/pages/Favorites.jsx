// src/pages/Favorites.jsx
import { useEffect, useState } from 'react'
import { fetchFavorites } from '../api/marketplaceService'
import { Link } from 'react-router-dom'

const Favorites = () => {
  const [favorites, setFavorites] = useState([])

  useEffect(() => {
    const loadFavorites = async () => {
      const data = await fetchFavorites()
      setFavorites(data)
    }
    loadFavorites()
  }, [])

  return (
    <div>
      <h1>My Favorites</h1>
      <ul>
        {favorites.map(fav => (
          <li key={fav.id}>
            Provider ID: {fav.provider} <Link to={`/providers/${fav.provider}`}>View Details</Link>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Favorites
