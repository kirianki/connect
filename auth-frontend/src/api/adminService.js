import axios from './axiosInstance'

// Sectors
export const fetchSectors = async () => {
  const response = await axios.get('/listings/sectors/')
  return response.data
}

export const createSector = async (data) => {
  const response = await axios.post('/listings/sectors/', data)
  return response.data
}

export const deleteSector = async (id) => {
  const response = await axios.delete(`/listings/sectors/${id}/`)
  return response.data
}

// Subcategories
export const fetchSubcategories = async () => {
  const response = await axios.get('/listings/subcategories/')
  return response.data
}

export const createSubcategory = async (data) => {
  const response = await axios.post('/listings/subcategories/', data)
  return response.data
}

export const deleteSubcategory = async (id) => {
  const response = await axios.delete(`/listings/subcategories/${id}/`)
  return response.data
}
