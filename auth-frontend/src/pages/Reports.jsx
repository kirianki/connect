// src/pages/Reports.jsx
import { useState } from 'react'
import { postReport } from '../api/marketplaceService'

const Reports = () => {
  const [formData, setFormData] = useState({ provider: '', description: '' })
  const [message, setMessage] = useState('')

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    await postReport(formData)
    setMessage('Report submitted successfully!')
    setFormData({ provider: '', description: '' })
  }

  return (
    <div>
      <h1>Report a Provider</h1>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Provider ID:</label>
          <input name="provider" value={formData.provider} onChange={handleChange} required />
        </div>
        <div>
          <label>Description:</label>
          <textarea name="description" value={formData.description} onChange={handleChange} required />
        </div>
        <button type="submit">Submit Report</button>
      </form>
    </div>
  )
}

export default Reports
