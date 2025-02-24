// src/pages/Bookings.jsx
import { useEffect, useState } from 'react'
import { fetchBookings } from '../api/marketplaceService'

const Bookings = () => {
  const [bookings, setBookings] = useState([])

  useEffect(() => {
    const loadBookings = async () => {
      const data = await fetchBookings()
      setBookings(data)
    }
    loadBookings()
  }, [])

  return (
    <div>
      <h1>My Bookings</h1>
      <ul>
        {bookings.map(booking => (
          <li key={booking.id}>
            Provider: {booking.provider} | Service Date: {new Date(booking.service_date).toLocaleString()} | Status: {booking.status}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Bookings
