// src/pages/ProviderDetail.jsx
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchProviderDetail, fetchReviews, postReview } from '../api/marketplaceService'

const ProviderDetail = () => {
  const { id } = useParams()
  const [provider, setProvider] = useState(null)
  const [reviews, setReviews] = useState([])
  const [newReview, setNewReview] = useState({ rating: '', comment: '' })

  useEffect(() => {
    const loadDetails = async () => {
      const providerData = await fetchProviderDetail(id)
      setProvider(providerData)
      const reviewsData = await fetchReviews({ provider: id })
      setReviews(reviewsData)
    }
    loadDetails()
  }, [id])

  const handleReviewChange = (e) => {
    setNewReview({ ...newReview, [e.target.name]: e.target.value })
  }

  const handleReviewSubmit = async (e) => {
    e.preventDefault()
    await postReview({ ...newReview, provider: id })
    // Reload reviews after posting
    const reviewsData = await fetchReviews({ provider: id })
    setReviews(reviewsData)
    setNewReview({ rating: '', comment: '' })
  }

  if (!provider) return <p>Loading provider details...</p>

  return (
    <div>
      <h1>{provider.business_name}</h1>
      <p>{provider.description}</p>
      <h2>Reviews</h2>
      <ul>
        {reviews.map(review => (
          <li key={review.id}>
            <strong>{review.client_name}:</strong> {review.comment} (Rating: {review.rating})
          </li>
        ))}
      </ul>
      <form onSubmit={handleReviewSubmit}>
        <h3>Leave a Review</h3>
        <div>
          <label>Rating (1-5):</label>
          <input type="number" name="rating" value={newReview.rating} onChange={handleReviewChange} required min="1" max="5" />
        </div>
        <div>
          <label>Comment:</label>
          <textarea name="comment" value={newReview.comment} onChange={handleReviewChange} required />
        </div>
        <button type="submit">Submit Review</button>
      </form>
    </div>
  )
}

export default ProviderDetail
