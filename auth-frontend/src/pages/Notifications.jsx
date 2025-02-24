// src/pages/Notifications.jsx
import { useEffect, useState } from 'react'
import { fetchNotifications, markNotificationsRead } from '../api/marketplaceService'

const Notifications = () => {
  const [notifications, setNotifications] = useState([])

  useEffect(() => {
    const loadNotifications = async () => {
      const data = await fetchNotifications()
      setNotifications(data)
    }
    loadNotifications()
  }, [])

  const handleMarkRead = async () => {
    await markNotificationsRead()
    const data = await fetchNotifications()
    setNotifications(data)
  }

  return (
    <div>
      <h1>Notifications</h1>
      <button onClick={handleMarkRead}>Mark all as read</button>
      <ul>
        {notifications.map(note => (
          <li key={note.id} style={{ fontWeight: note.is_read ? 'normal' : 'bold' }}>
            {note.message} - {new Date(note.created_at).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Notifications
