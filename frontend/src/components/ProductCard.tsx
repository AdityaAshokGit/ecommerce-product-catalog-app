import type { Product } from '../types';

interface Props {
  product: Product;
}

export const ProductCard = ({ product }: Props) => {
  const isPopular = product.popularityScore > 50;

  return (
    <div className="border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow p-4 bg-white flex flex-col h-full group/card">
      {/* Image Container */}
      <div className="relative aspect-square mb-4 bg-gray-100 rounded-md overflow-hidden group">
        <img
          src={product.imageUrl}
          alt={product.name}
          className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
          onError={(e) => {
            (e.target as HTMLImageElement).src = 'https://via.placeholder.com/300?text=No+Image';
          }}
        />
        {isPopular && (
           <span className="absolute top-2 right-2 bg-yellow-400 text-yellow-900 text-xs font-bold px-2 py-1 rounded-full shadow-sm z-10">
             HOT
           </span>
        )}
      </div>

      {/* Content */}
      <div className="flex-grow">
        <div className="flex justify-between items-start mb-1">
          {/* UPDATED: Brand + Category */}
          <div className="flex flex-col">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">
              {product.brand}
            </span>
            <span className="text-[10px] text-gray-400 font-medium bg-gray-100 px-1.5 py-0.5 rounded-sm w-fit mt-0.5">
              {product.category}
            </span>
          </div>
          
          <div className="flex items-center text-yellow-500 text-sm font-medium">
            <span>★</span>
            <span className="ml-1 text-gray-700">{product.rating}</span>
          </div>
        </div>
        
        <h3 className="font-bold text-lg text-gray-900 leading-tight mb-2 mt-2">
          {product.name}
        </h3>
        
        <p className="text-sm text-gray-600 line-clamp-2 mb-4" title={product.description}>
          {product.description}
        </p>
      </div>

      {/* Footer / Price */}
      <div className="mt-auto pt-3 border-t border-gray-100 flex items-center justify-between">
        <span className="text-xl font-bold text-gray-900">
          ${product.price.toFixed(2)}
        </span>
        <button 
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                product.inStock 
                ? 'bg-blue-600 text-white hover:bg-blue-700' 
                : 'bg-gray-100 text-gray-400 cursor-not-allowed'
            }`}
            disabled={!product.inStock}
        >
          {product.inStock ? 'Add' : 'No Stock'}
        </button>
      </div>
    </div>
  );
};