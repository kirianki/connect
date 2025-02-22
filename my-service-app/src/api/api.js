import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api"; // Update if needed

export const fetchSectors = () => axios.get(`${API_BASE_URL}/listings/sectors/`);
export const fetchSubcategories = (sectorId) => axios.get(`${API_BASE_URL}/listings/sectors/${sectorId}/subcategories/`);
export const fetchProviders = (subcategoryId) => axios.get(`${API_BASE_URL}/listings/subcategories/${subcategoryId}/providers/`);
export const fetchProviderDetails = (providerId) => axios.get(`${API_BASE_URL}/listings/providers/${providerId}/`);
export const searchProviders = (query) => axios.get(`${API_BASE_URL}/listings/providers/?${query}`);
