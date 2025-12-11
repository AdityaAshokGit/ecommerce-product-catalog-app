export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  brand: string;
  rating: number;
  inStock: boolean;
  imageUrl: string;
  tags: string[];
  popularityScore: number;
}

export interface FacetOption {
  name: string;
  value?: string;
  count: number;
}

export interface FilterOptions {
  categories: FacetOption[];
  brands: FacetOption[];
  availability: FacetOption[];
  minPrice: number;
  maxPrice: number;
}

// NEW: Pagination Response Wrapper
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface ProductParams {
  q?: string;
  category?: string | string[];
  brand?: string | string[];
  minPrice?: number;
  maxPrice?: number;
  sort?: string;
  availability?: string;
  page?: number;  // NEW
  limit?: number; // NEW
}