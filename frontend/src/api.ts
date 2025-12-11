import axios from 'axios';
import type { Product, FilterOptions, ProductParams } from './types';

const API_URL = 'http://localhost:8000/api';

export const getProducts = async (params: ProductParams): Promise<Product[]> => {
  const searchParams = new URLSearchParams();

  // 1. Search Query: Only append if not empty
  if (params.q && params.q.trim() !== '') {
    searchParams.append('q', params.q);
  }
  
  // 2. Category: Handle String vs Array, IGNORE empty strings
  if (params.category) {
    const cats = Array.isArray(params.category) ? params.category : [params.category];
    cats.forEach(c => {
      if (c && c.trim() !== '') searchParams.append('category', c);
    });
  }

  // 3. Brand: Handle String vs Array, IGNORE empty strings
  if (params.brand) {
    const brands = Array.isArray(params.brand) ? params.brand : [params.brand];
    brands.forEach(b => {
      if (b && b.trim() !== '') searchParams.append('brand', b);
    });
  }

  // 4. Other Params
  if (params.sort) searchParams.append('sort', params.sort);
  
  // Explicit check for undefined to allow 0
  if (params.minPrice !== undefined) searchParams.append('minPrice', params.minPrice.toString());
  if (params.maxPrice !== undefined) searchParams.append('maxPrice', params.maxPrice.toString());

  console.log("Requesting:", searchParams.toString()); // Debug log for browser console

  const response = await axios.get<Product[]>(`${API_URL}/products?${searchParams.toString()}`);
  return response.data;
};

// ... keep getMetadata same
export const getMetadata = async (): Promise<FilterOptions> => {
  const response = await axios.get<FilterOptions>(`${API_URL}/metadata`);
  return response.data;
};