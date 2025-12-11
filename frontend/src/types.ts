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

export interface FilterOptions {
  categories: string[];
  brands: string[];
  minPrice: number;
  maxPrice: number;
}

export interface ProductParams {
  q?: string;
  category?: string | string[];
  brand?: string | string[];
  minPrice?: number;
  maxPrice?: number;
  sort?: string;
}