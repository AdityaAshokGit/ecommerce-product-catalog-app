import { useState, useEffect, useCallback } from 'react';

interface Props {
  min: number; // Global Min
  max: number; // Global Max (from dataset)
  onChange: (min: number, max: number) => void;
  initialMin?: number;
  initialMax?: number;
}

export const PriceFilter = ({min, max, onChange, initialMin, initialMax }: Props) => {
  const rangeMin = 0; 
  const rangeMax = Math.ceil(max);

  const [minVal, setMinVal] = useState(initialMin ?? rangeMin);
  const [maxVal, setMaxVal] = useState(initialMax ?? rangeMax);

  useEffect(() => {
    let nextMin = initialMin ?? rangeMin;
    let nextMax = initialMax ?? rangeMax;

    if (nextMax > rangeMax) {
      nextMax = rangeMax;
    }

    if (nextMin < rangeMin) {
      nextMin = rangeMin;
    }

    setMinVal(nextMin);
    setMaxVal(nextMax);
  }, [initialMin, initialMax, rangeMin, rangeMax]);

  const handleMinInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    let value = parseInt(e.target.value, 10);
    if (isNaN(value)) value = rangeMin;

    value = Math.min(Math.max(rangeMin, value), maxVal - 1);
    
    setMinVal(value);
    onChange(value, maxVal);
  };

  const handleMaxInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    let value = parseInt(e.target.value, 10);
    if (isNaN(value)) value = rangeMax;

    // Constraint: (minVal + 1) <= value <= rangeMax
    value = Math.max(value, minVal + 1);
    value = Math.min(value, rangeMax);

    setMaxVal(value);
    onChange(minVal, value);
  };

  const handleMinSlide = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = Math.min(Math.round(Number(e.target.value)), maxVal - 1);
    setMinVal(value);
    onChange(value, maxVal);
  };

  const handleMaxSlide = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = Math.max(Math.round(Number(e.target.value)), minVal + 1);
    setMaxVal(value);
    onChange(minVal, value);
  };

  // --- UI HELPERS ---

  const getPercent = useCallback(
    (value: number) => {
      // Safety check to prevent NaN if range is 0
      if (rangeMax === rangeMin) return 0;
      return Math.round(((value - rangeMin) / (rangeMax - rangeMin)) * 100);
    },
    [rangeMin, rangeMax]
  );

  return (
    <div className="w-full pb-4">
      {/* 1. Input Boxes */}
      <div className="flex justify-between items-center mb-4 gap-4">
        <div className="flex items-center bg-white border border-gray-300 rounded px-2 py-1 focus-within:ring-2 focus-within:ring-blue-200">
          <span className="text-gray-500 text-sm">$</span>
          <input
            type="number"
            min={rangeMin}
            max={rangeMax}
            step="1"
            value={minVal}
            onChange={handleMinInput}
            onKeyDown={(e) => {
                if (e.key === '.' || e.key === 'e') e.preventDefault();
            }}
            className="w-16 text-sm outline-none border-none ml-1 text-right font-mono"
          />
        </div>
        <span className="text-gray-400">-</span>
        <div className="flex items-center bg-white border border-gray-300 rounded px-2 py-1 focus-within:ring-2 focus-within:ring-blue-200">
          <span className="text-gray-500 text-sm">$</span>
          <input
            type="number"
            min={rangeMin}
            max={rangeMax}
            step="1"
            value={maxVal}
            onChange={handleMaxInput}
            onKeyDown={(e) => {
                if (e.key === '.' || e.key === 'e') e.preventDefault();
            }}
            className="w-16 text-sm outline-none border-none ml-1 text-right font-mono"
          />
        </div>
      </div>

      {/* 2. The Dual Slider */}
      <div className="relative w-full h-5 flex items-center">
        {/* Track */}
        <div className="absolute w-full h-1 bg-gray-200 rounded z-0"></div>
        
        {/* Highlight Range */}
        <div 
            className="absolute h-1 bg-blue-600 rounded z-0"
            style={{
                left: `${getPercent(minVal)}%`,
                width: `${getPercent(maxVal) - getPercent(minVal)}%`
            }}
        ></div>

        {/* Left Thumb */}
        <input
          type="range"
          min={rangeMin}
          max={rangeMax}
          step="1" 
          value={minVal}
          onChange={handleMinSlide}
          className="absolute w-full h-0 appearance-none pointer-events-none z-10 
                     [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:pointer-events-auto 
                     [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full 
                     [&::-webkit-slider-thumb]:bg-blue-600 [&::-webkit-slider-thumb]:shadow-md [&::-webkit-slider-thumb]:cursor-pointer"
        />

        {/* Right Thumb */}
        <input
          type="range"
          min={rangeMin}
          max={rangeMax}
          step="1" 
          value={maxVal}
          onChange={handleMaxSlide}
          className="absolute w-full h-0 appearance-none pointer-events-none z-20 
                     [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:pointer-events-auto 
                     [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full 
                     [&::-webkit-slider-thumb]:bg-blue-600 [&::-webkit-slider-thumb]:shadow-md [&::-webkit-slider-thumb]:cursor-pointer"
        />
      </div>
    </div>
  );
};