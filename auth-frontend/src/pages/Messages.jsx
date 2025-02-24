// src/pages/Messages.jsx
import { useEffect, useState } from 'react'
import { fetchMessages, postMessage } from '../api/marketplaceService'

const Messages = () => {
  const [messages, setMessages] = useState([])
  const [newMsg, setNewMsg] = useState({ receiver: '', content: '' })

  useEffect(() => {
    const loadMessages = async () => {
      const data = await fetchMessages()
      setMessages(data)
    }
    loadMessages()
  }, [])

  const handleChange = (e) => {
    setNewMsg({ ...newMsg, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    await postMessage(newMsg)
    const data = await fetchMessages()
    setMessages(data)
    setNewMsg({ receiver: '', content: '' })
  }

  return (
    <div>
      <h1>Messages</h1>
      <ul>
        {messages.map(msg => (
          <li key={msg.id}>
            <strong>{msg.sender}</strong> to <strong>{msg.receiver}</strong>: {msg.content}
          </li>
        ))}
      </ul>
      <form onSubmit={handleSubmit}>
        <h3>Send a Message</h3>
        <div>
          <label>Receiver ID:</label>
          <input name="receiver" value={newMsg.receiver} onChange={handleChange} required />
        </div>
        <div>
          <label>Content:</label>
          <textarea name="content" value={newMsg.content} onChange={handleChange} required />
        </div>
        <button type="submit">Send</button>
      </form>
    </div>
  )
}

export default Messages
