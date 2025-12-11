import axios from 'axios';
import type { Product, FilterOptions, ProductParams } from './types';

// If you are running on a different port, update this
const API_URL = 'http://localhost:8000/api';

export const getProducts = async (params: ProductParams): Promise<Product[]> => {
  // Axios automatically handles the query string serialization
  const response = await axios.get(`${API_URL}/products`, { params });
  return response.data;
};

export const getMetadata = async (): Promise<FilterOptions> => {
  const response = await axios.get(`${API_URL}/metadata`);
  return response.data;
};