import { useState, useEffect } from 'react'
import { fetchSubcategories, createSubcategory, deleteSubcategory } from '../api/adminService'

const ManageSubcategories = () => {
  const [subcategories, setSubcategories] = useState([])
  const [newSubcategory, setNewSubcategory] = useState({ name: '', description: '', sector: '' })
  const [error, setError] = useState('')

  const loadSubcategories = async () => {
    try {
      const data = await fetchSubcategories()
      setSubcategories(data)
    } catch (err) {
      setError('Failed to load subcategories')
    }
  }

  useEffect(() => {
    loadSubcategories()
  }, [])

  const handleInputChange = (e) => {
    setNewSubcategory({ ...newSubcategory, [e.target.name]: e.target.value })
  }

  const handleCreateSubcategory = async (e) => {
    e.preventDefault()
    try {
      await createSubcategory(newSubcategory)
      setNewSubcategory({ name: '', description: '', sector: '' })
      loadSubcategories()
    } catch (err) {
      setError('Failed to create subcategory')
    }
  }

  const handleDeleteSubcategory = async (id) => {
    try {
      await deleteSubcategory(id)
      loadSubcategories()
    } catch (err) {
      setError('Failed to delete subcategory')
    }
  }

  return (
    <div>
      <h2>Manage Subcategories</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleCreateSubcategory}>
        <input
          type="text"
          name="name"
          placeholder="Subcategory Name"
          value={newSubcategory.name}
          onChange={handleInputChange}
          required
        />
        <input
          type="text"
          name="description"
          placeholder="Description"
          value={newSubcategory.description}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="sector"
          placeholder="Sector ID"
          value={newSubcategory.sector}
          onChange={handleInputChange}
          required
        />
        <button type="submit">Create Subcategory</button>
      </form>
      <hr />
      <ul>
        {subcategories.map(sub => (
          <li key={sub.id}>
            <strong>{sub.name}</strong> - {sub.description} (Sector: {sub.sector})
            <button onClick={() => handleDeleteSubcategory(sub.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ManageSubcategories
