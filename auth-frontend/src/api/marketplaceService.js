// src/api/marketplaceService.js
import axios from './axiosInstance';

// Sectors, Subcategories, Providers, etc.
export const fetchSectors = async (params) => {
  const response = await axios.get('/listings/sectors/', { params });
  return response.data;
};

export const fetchSubcategories = async (params) => {
  const response = await axios.get('/listings/subcategories/', { params });
  return response.data;
};

export const fetchProviderProfiles = async (params) => {
  const response = await axios.get('/listings/providers/', { params });
  return response.data;
};

export const fetchProviderDetail = async (id) => {
  const response = await axios.get(`/listings/providers/${id}/`);
  return response.data;
};

// Reviews
export const fetchReviews = async (params) => {
  const response = await axios.get('/listings/reviews/', { params });
  return response.data;
};

export const postReview = async (data) => {
  const response = await axios.post('/listings/reviews/', data);
  return response.data;
};

// Messaging, Bookings, Notifications, Favorites, Reports
export const fetchMessages = async () => {
  const response = await axios.get('/listings/messages/');
  return response.data;
};

export const postMessage = async (data) => {
  const response = await axios.post('/listings/messages/', data);
  return response.data;
};

export const fetchBookings = async () => {
  const response = await axios.get('/listings/bookings/');
  return response.data;
};

export const fetchNotifications = async () => {
  const response = await axios.get('/listings/notifications/');
  return response.data;
};

export const markNotificationsRead = async () => {
  const response = await axios.post('/listings/notifications/mark-read/');
  return response.data;
};

export const fetchFavorites = async () => {
  const response = await axios.get('/listings/favorites/');
  return response.data;
};

export const postReport = async (data) => {
  const response = await axios.post('/listings/reports/', data);
  return response.data;
};

export const createProviderProfile = async (data) => {
  const response = await axios.post('/listings/providers/', data)
  return response.data
}
export const fetchProviderProfileByUser = async (userId) => {
  const response = await axios.get(`/listings/providers/?user=${userId}`)
  // Assuming the response returns an array of profiles (should be only one)
  return response.data[0] || null
}

export const updateProviderProfile = async (data) => {
  // Ensure that 'data' includes the provider profile id.
  // For example, data.id should be the provider profile's id.
  const response = await axios.patch(`/listings/providers/${data.id}/`, data)
  return response.data
}