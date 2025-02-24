import { useState, useEffect } from 'react'
import { fetchSectors, createSector, deleteSector } from '../api/adminService'

const ManageSectors = () => {
  const [sectors, setSectors] = useState([])
  const [newSector, setNewSector] = useState({ name: '', description: '' })
  const [error, setError] = useState('')

  const loadSectors = async () => {
    try {
      const data = await fetchSectors()
      setSectors(data)
    } catch (err) {
      setError('Failed to load sectors')
    }
  }

  useEffect(() => {
    loadSectors()
  }, [])

  const handleInputChange = (e) => {
    setNewSector({ ...newSector, [e.target.name]: e.target.value })
  }

  const handleCreateSector = async (e) => {
    e.preventDefault()
    try {
      await createSector(newSector)
      setNewSector({ name: '', description: '' })
      loadSectors()
    } catch (err) {
      setError('Failed to create sector')
    }
  }

  const handleDeleteSector = async (id) => {
    try {
      await deleteSector(id)
      loadSectors()
    } catch (err) {
      setError('Failed to delete sector')
    }
  }

  return (
    <div>
      <h2>Manage Sectors</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleCreateSector}>
        <input
          type="text"
          name="name"
          placeholder="Sector Name"
          value={newSector.name}
          onChange={handleInputChange}
          required
        />
        <input
          type="text"
          name="description"
          placeholder="Description"
          value={newSector.description}
          onChange={handleInputChange}
        />
        <button type="submit">Create Sector</button>
      </form>
      <hr />
      <ul>
        {sectors.map(sector => (
          <li key={sector.id}>
            <strong>{sector.name}</strong> - {sector.description}
            <button onClick={() => handleDeleteSector(sector.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ManageSectors
