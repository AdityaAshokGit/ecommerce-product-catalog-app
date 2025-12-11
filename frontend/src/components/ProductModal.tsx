import React from 'react';
import { useQuery } from '@tanstack/react-query';
import type { Product } from '../types';
import { getRecommendations } from '../api';

interface ProductModalProps {
  product: Product;
  onClose: () => void;
}

export const ProductModal: React.FC<ProductModalProps> = ({ product, onClose }) => {
  // 1. Fetch Recommendations for THIS product
  const { data: recommendations, isLoading } = useQuery({
    queryKey: ['recommendations', product.id],
    queryFn: () => getRecommendations(product.id),
    staleTime: 1000 * 60 * 5, // Cache for 5 minutes
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-sm transition-opacity" 
        onClick={onClose}
      />

      {/* Modal Content */}
      <div className="relative bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto flex flex-col md:flex-row overflow-hidden">
        
        {/* Close Button */}
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 z-10 p-2 bg-white/80 rounded-full hover:bg-gray-100 transition-colors"
        >
          <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Left: Main Product Image */}
        <div className="w-full md:w-1/2 bg-gray-50 flex items-center justify-center p-8">
          <img 
            src={product.imageUrl} 
            alt={product.name} 
            className="max-h-[400px] object-contain mix-blend-multiply"
          />
        </div>

        {/* Right: Details & Recommendations */}
        <div className="w-full md:w-1/2 p-8 flex flex-col">
          {/* Main Product Info */}
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-2">
               <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded-full uppercase tracking-wide">
                 {product.brand}
               </span>
               <span className="text-xs text-gray-500 font-medium border border-gray-200 px-2 py-1 rounded-full">
                 {product.category}
               </span>
            </div>
            
            <h2 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h2>
            
            <div className="flex items-center gap-4 mb-4">
              <span className="text-2xl font-bold text-gray-900">${product.price.toFixed(2)}</span>
              <div className="flex items-center text-yellow-500 font-medium">
                <span>★</span>
                <span className="ml-1 text-gray-700">{product.rating}</span>
              </div>
            </div>

            <p className="text-gray-600 leading-relaxed mb-6">
              {product.description}
            </p>

            <button 
              className={`w-full py-3 rounded-lg font-bold text-white transition-all transform active:scale-95 ${
                product.inStock 
                  ? 'bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-200' 
                  : 'bg-gray-300 cursor-not-allowed'
              }`}
              disabled={!product.inStock}
            >
              {product.inStock ? 'Add to Cart' : 'Out of Stock'}
            </button>
          </div>

          {/* Bonus: Recommendations Section */}
          <div className="border-t border-gray-100 pt-6 mt-auto">
            <h3 className="font-bold text-sm text-gray-900 uppercase tracking-wide mb-4 flex items-center gap-2">
              <span className="text-orange-500">⚡</span> Frequently Bought Together
            </h3>
            
            {isLoading ? (
              <div className="flex gap-4 animate-pulse">
                {[1,2,3].map(i => <div key={i} className="w-20 h-20 bg-gray-200 rounded-md" />)}
              </div>
            ) : recommendations && recommendations.length > 0 ? (
              <div className="grid grid-cols-3 gap-3">
                {recommendations.map(rec => (
                  <div key={rec.id} className="group cursor-pointer border border-gray-100 rounded-lg p-2 hover:border-blue-200 transition-colors">
                    <div className="aspect-square bg-gray-50 rounded-md mb-2 overflow-hidden">
                      <img src={rec.imageUrl} alt={rec.name} className="w-full h-full object-contain mix-blend-multiply group-hover:scale-105 transition-transform" />
                    </div>
                    <p className="text-xs font-medium text-gray-900 line-clamp-2 leading-tight">{rec.name}</p>
                    <p className="text-xs text-gray-500 mt-1">${rec.price}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-400 italic">No historical combinations found.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};