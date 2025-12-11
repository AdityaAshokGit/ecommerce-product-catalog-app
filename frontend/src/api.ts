import axios from 'axios';
import type { Product, FilterOptions, ProductParams, PaginatedResponse } from './types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const getProducts = async (params: ProductParams): Promise<PaginatedResponse<Product>> => {
  const searchParams = new URLSearchParams();

  if (params.q && params.q.trim() !== '') searchParams.append('q', params.q);
  
  if (params.category) {
    const cats = Array.isArray(params.category) ? params.category : [params.category];
    cats.forEach(c => {
      if (c && c.trim() !== '') searchParams.append('category', c);
    });
  }

  if (params.brand) {
    const brands = Array.isArray(params.brand) ? params.brand : [params.brand];
    brands.forEach(b => {
      if (b && b.trim() !== '') searchParams.append('brand', b);
    });
  }

  if (params.sort) searchParams.append('sort', params.sort);
  if (params.minPrice !== undefined) searchParams.append('minPrice', params.minPrice.toString());
  if (params.maxPrice !== undefined) searchParams.append('maxPrice', params.maxPrice.toString());
  if (params.availability) searchParams.append('availability', params.availability);

  searchParams.append('page', (params.page || 1).toString());
  searchParams.append('limit', (params.limit || 20).toString());

  const response = await axios.get<PaginatedResponse<Product>>(`${API_URL}/products?${searchParams.toString()}`);
  return response.data;
};

export const getMetadata = async (params: ProductParams): Promise<FilterOptions> => {
  const searchParams = new URLSearchParams();

  if (params.q && params.q.trim() !== '') searchParams.append('q', params.q);
  
  if (params.category) {
    const cats = Array.isArray(params.category) ? params.category : [params.category];
    cats.forEach(c => {
      if (c && c.trim() !== '') searchParams.append('category', c);
    });
  }

  if (params.brand) {
    const brands = Array.isArray(params.brand) ? params.brand : [params.brand];
    brands.forEach(b => {
      if (b && b.trim() !== '') searchParams.append('brand', b);
    });
  }

  if (params.minPrice !== undefined) searchParams.append('minPrice', params.minPrice.toString());
  if (params.maxPrice !== undefined) searchParams.append('maxPrice', params.maxPrice.toString());
  if (params.availability) searchParams.append('availability', params.availability);

  const response = await axios.get<FilterOptions>(`${API_URL}/metadata?${searchParams.toString()}`);
  return response.data;
};

export const getRecommendations = async (productId: string): Promise<Product[]> => {
  const response = await axios.get<Product[]>(`${API_URL}/products/${productId}/recommendations`);
  return response.data;
};