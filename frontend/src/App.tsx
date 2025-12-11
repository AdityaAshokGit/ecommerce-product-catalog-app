import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { getProducts, getMetadata } from './api';
import { ProductCard } from './components/ProductCard';
import { PriceFilter } from './components/PriceFilter';
import { ProductModal } from './components/ProductModal';
import type { Product } from './types';

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debouncedValue;
}

function App() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const [search, setSearch] = useState(searchParams.get('q') || '');
  const [selectedCategories, setSelectedCategories] = useState<string[]>(searchParams.getAll('category'));
  const [selectedBrands, setSelectedBrands] = useState<string[]>(searchParams.getAll('brand'));
  const [sort, setSort] = useState(searchParams.get('sort') || 'popular');
  const [availability, setAvailability] = useState<string | null>(searchParams.get('availability') || null);

  const urlMin = searchParams.get('minPrice');
  const urlMax = searchParams.get('maxPrice');
  const [minPrice, setMinPrice] = useState<number | undefined>(urlMin ? Number(urlMin) : undefined);
  const [maxPrice, setMaxPrice] = useState<number | undefined>(urlMax ? Number(urlMax) : undefined);

  const [page, setPage] = useState<number>(Number(searchParams.get('page')) || 1);
  const LIMIT = 18;

  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  const debouncedSearch = useDebounce(search, 300);
  const debouncedMin = useDebounce(minPrice, 300);
  const debouncedMax = useDebounce(maxPrice, 300);
  useEffect(() => {
    const params = new URLSearchParams();
    
    if (debouncedSearch) params.set('q', debouncedSearch);
    
    selectedCategories.forEach(c => params.append('category', c));
    selectedBrands.forEach(b => params.append('brand', b));
    
    if (sort) params.set('sort', sort);
    if (debouncedMin !== undefined) params.set('minPrice', debouncedMin.toString());
    if (debouncedMax !== undefined) params.set('maxPrice', debouncedMax.toString());
    
    if (availability) params.set('availability', availability);
    if (page > 1) params.set('page', page.toString());

    setSearchParams(params);
  }, [debouncedSearch, selectedCategories, selectedBrands, sort, debouncedMin, debouncedMax, availability, page, setSearchParams]);

  const metadataQuery = useQuery({
    queryKey: ['metadata', { q: debouncedSearch, category: selectedCategories, brand: selectedBrands, min: debouncedMin, max: debouncedMax, availability }],
    queryFn: () => getMetadata({
      q: debouncedSearch,
      category: selectedCategories,
      brand: selectedBrands,
      minPrice: debouncedMin,
      maxPrice: debouncedMax,
      availability: availability || undefined
    }),
    placeholderData: (prev) => prev,
  });

  const productQuery = useQuery({
    queryKey: ['products', { q: debouncedSearch, category: selectedCategories, brand: selectedBrands, sort, min: debouncedMin, max: debouncedMax, availability, page }],
    queryFn: () => getProducts({ 
        q: debouncedSearch, 
        category: selectedCategories, 
        brand: selectedBrands, 
        sort,
        minPrice: debouncedMin,
        maxPrice: debouncedMax,
        availability: availability || undefined,
        page: page,
        limit: LIMIT
    }),
    placeholderData: (prev) => prev,
  });

  const handleSearchChange = (val: string) => {
    setSearch(val);
    setPage(1);
  };

  const handleCategoryToggle = (category: string) => {
    setPage(1);
    setSelectedCategories(prev => 
      prev.includes(category) 
        ? prev.filter(c => c !== category)
        : [...prev, category]
    );
  };

  const handleBrandToggle = (brand: string) => {
    setPage(1);
    setSelectedBrands(prev => 
      prev.includes(brand) 
        ? prev.filter(b => b !== brand) 
        : [...prev, brand]
    );
  };

  const handleSortChange = (val: string) => {
    setPage(1);
    setSort(val);
  };

  const handleAvailabilityChange = (val: string | null) => {
    setPage(1);
    setAvailability(val);
  };

  const handlePriceChange = (min?: number, max?: number) => {
    setPage(1);
    setMinPrice(min);
    setMaxPrice(max);
  };

  const handleClearFilters = () => {
    setSearch('');
    setSelectedCategories([]);
    setSelectedBrands([]);
    setMinPrice(undefined);
    setMaxPrice(undefined);
    setAvailability(null);
    setPage(1);
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-30 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer" onClick={handleClearFilters}>
             <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">F</div>
             <h1 className="text-xl font-bold text-gray-900 tracking-tight">FerMart</h1>
          </div>
          
          <div className="w-full max-w-md ml-4 relative">
             <input
               type="text"
               placeholder="Search products..."
               className="w-full bg-gray-100 border-transparent border rounded-md pl-4 pr-10 py-2 text-sm focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none"
               value={search}
               onChange={(e) => handleSearchChange(e.target.value)}
             />
             {search && (
               <button
                 onClick={() => handleSearchChange('')}
                 className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
                 aria-label="Clear search"
               >
                 <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                 </svg>
               </button>
             )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row gap-8">
          
          {/* Sidebar */}
          <aside className="w-full md:w-64 flex-shrink-0 space-y-6">
            
            <div className="flex justify-between items-center px-1">
              <h2 className="text-lg font-bold text-gray-900">Filters</h2>
              <button onClick={handleClearFilters} className="text-sm text-blue-600 hover:text-blue-800 font-medium">
                Reset All
              </button>
            </div>
            
            {/* Sort */}
            <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
               <h3 className="font-bold text-xs text-gray-500 mb-3 uppercase tracking-wider">Sort By</h3>
               <select 
                 className="w-full border-gray-300 rounded-md shadow-sm p-2 text-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 cursor-pointer hover:bg-white transition-colors"
                 value={sort}
                 onChange={(e) => handleSortChange(e.target.value)}
               >
                 <option value="popular">Most Popular</option>
                 <option value="price_asc">Price: Low to High</option>
                 <option value="price_desc">Price: High to Low</option>
                 <option value="rating">Top Rated</option>
               </select>
            </div>

            {metadataQuery.data && (
              <>
                {/* Price Filter */}
                <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-bold text-xs text-gray-500 uppercase tracking-wider">Price Range</h3>
                    {(minPrice !== undefined || maxPrice !== undefined) && (
                      <button 
                        onClick={() => handlePriceChange(undefined, undefined)}
                        className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                      >
                        Reset
                      </button>
                    )}
                  </div>
                  <PriceFilter 
                    min={metadataQuery.data.minPrice}
                    max={metadataQuery.data.maxPrice}
                    initialMin={minPrice}
                    initialMax={maxPrice}
                    onChange={handlePriceChange}
                  />
                </div>

                {/* Categories */}
                <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-bold text-xs text-gray-500 uppercase tracking-wider">Category</h3>
                    {selectedCategories.length > 0 && (
                      <button 
                        onClick={() => { setPage(1); setSelectedCategories([]); }}
                        className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                      >
                        Clear
                      </button>
                    )}
                  </div>
                  <div className="space-y-2">
                     {metadataQuery.data?.categories.map((catObj) => {
                       const isDisabled = catObj.count === 0 && !selectedCategories.includes(catObj.name);
                       return (
                         <label key={catObj.name} className={`flex items-center space-x-3 group ${isDisabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}>
                           <input 
                             type="checkbox" 
                             value={catObj.name}
                             checked={selectedCategories.includes(catObj.name)}
                             onChange={() => handleCategoryToggle(catObj.name)}
                             disabled={isDisabled}
                             className="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 transition duration-150 ease-in-out"
                           />
                           <span className={`text-sm transition-colors capitalize ${isDisabled ? 'text-gray-400' : 'text-gray-700 group-hover:text-blue-600'}`}>
                             {catObj.name} 
                             <span className="text-gray-400 text-xs ml-1">({catObj.count})</span>
                           </span>
                         </label>
                       );
                     })}
                  </div>
                </div>

                {/* Brands */}
                <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-bold text-xs text-gray-500 uppercase tracking-wider">Brand</h3>
                    {selectedBrands.length > 0 && (
                      <button 
                        onClick={() => { setPage(1); setSelectedBrands([]); }}
                        className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                      >
                        Clear
                      </button>
                    )}
                  </div>
                  <div className="space-y-2 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                     {metadataQuery.data?.brands.map((brandObj) => {
                       const isDisabled = brandObj.count === 0 && !selectedBrands.includes(brandObj.name);
                       return (
                         <label key={brandObj.name} className={`flex items-center space-x-3 group ${isDisabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}>
                           <input 
                             type="checkbox" 
                             value={brandObj.name}
                             checked={selectedBrands.includes(brandObj.name)}
                             onChange={() => handleBrandToggle(brandObj.name)}
                             disabled={isDisabled}
                             className="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 transition duration-150 ease-in-out"
                           />
                           <span className={`text-sm transition-colors ${isDisabled ? 'text-gray-400' : 'text-gray-700 group-hover:text-blue-600'}`}>
                             {brandObj.name}
                             <span className="text-gray-400 text-xs ml-1">({brandObj.count})</span>
                           </span>
                         </label>
                       );
                     })}
                  </div>
                </div>

                {/* Availability (Dynamic) */}
                <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-bold text-xs text-gray-500 uppercase tracking-wider">Availability</h3>
                    {availability && (
                      <button 
                        onClick={() => handleAvailabilityChange(null)}
                        className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                      >
                        Clear
                      </button>
                    )}
                  </div>
                  <div className="space-y-2">
                    {metadataQuery.data?.availability?.map((opt) => {
                       const apiValue = opt.value || opt.name;
                       const isSelected = availability === apiValue;
                       const isDisabled = opt.count === 0 && !isSelected;

                       return (
                         <label key={opt.name} className={`flex items-center space-x-3 group ${isDisabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}>
                           <input 
                             type="radio"
                             name="availability"
                             value={apiValue}
                             checked={isSelected}
                             onChange={() => handleAvailabilityChange(apiValue)}
                             disabled={isDisabled}
                             className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                           />
                           <span className={`text-sm transition-colors ${isDisabled ? 'text-gray-400' : 'text-gray-700 group-hover:text-blue-600'}`}>
                             {opt.name}
                             <span className="text-gray-400 text-xs ml-1">({opt.count})</span>
                           </span>
                         </label>
                       );
                    })}
                  </div>
                </div>
              </>
            )}
          </aside>

          {/* Product Grid */}
          <section className="flex-1 flex flex-col">
            {productQuery.isLoading ? (
               <div className="flex-1 flex flex-col items-center justify-center py-20 text-gray-400">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                  <p>Loading catalog...</p>
               </div>
            ) : productQuery.isError ? (
               <div className="text-center py-20 bg-red-50 rounded-lg border border-red-200 text-red-600">
                  <svg className="mx-auto h-12 w-12 text-red-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <h3 className="font-bold text-lg mb-2">Unable to Load Products</h3>
                  <p className="text-sm mb-1">
                    {productQuery.error instanceof Error 
                      ? productQuery.error.message 
                      : 'Could not connect to the backend server'}
                  </p>
                  <p className="text-xs text-red-500 mb-6">Please check that the backend is running on port 8000</p>
                  <button
                    onClick={() => productQuery.refetch()}
                    className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors font-medium"
                  >
                    Try Again
                  </button>
               </div>
            ) : productQuery.data?.items.length === 0 ? (
               <div className="text-center py-20 bg-white rounded-lg border border-gray-200 shadow-sm">
                  <h3 className="text-lg font-medium text-gray-900 mb-1">No products found</h3>
                  <p className="text-gray-500 mb-6">We couldn't find matches for your current filters.</p>
                  <button 
                    onClick={handleClearFilters}
                    className="text-blue-600 hover:text-blue-800 font-medium underline underline-offset-4"
                  >
                    Clear all filters
                  </button>
               </div>
            ) : (
               <>
                 <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {productQuery.data?.items.map((product) => (
                      <ProductCard 
                        key={product.id} 
                        product={product} 
                        onClick={(p) => setSelectedProduct(p)}
                      />
                    ))}
                 </div>

                 {/* Pagination Controls */}
                 {productQuery.data && productQuery.data.total_pages > 1 && (
                    <div className="mt-8 flex justify-center items-center gap-4 py-4 border-t border-gray-200">
                      <button
                        onClick={() => {
                          setPage(p => Math.max(1, p - 1));
                          window.scrollTo({ top: 0, behavior: 'smooth' });
                        }}
                        disabled={page === 1}
                        className="px-4 py-2 text-sm font-medium rounded-md border border-gray-300 text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                      >
                        Previous
                      </button>
                      
                      <span className="text-sm text-gray-600">
                        Page <span className="font-bold text-gray-900">{page}</span> of <span className="font-bold text-gray-900">{productQuery.data.total_pages}</span>
                      </span>

                      <button
                        onClick={() => {
                          setPage(p => Math.min(productQuery.data.total_pages, p + 1));
                          window.scrollTo({ top: 0, behavior: 'smooth' });
                        }}
                        disabled={page >= productQuery.data.total_pages}
                        className="px-4 py-2 text-sm font-medium rounded-md border border-gray-300 text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                      >
                        Next
                      </button>
                    </div>
                 )}
               </>
            )}
          </section>
        </div>
      </main>

      {/* Modal */}
      {selectedProduct && (
        <ProductModal 
          product={selectedProduct} 
          onClose={() => setSelectedProduct(null)} 
        />
      )}
    </div>
  );
}

export default App;