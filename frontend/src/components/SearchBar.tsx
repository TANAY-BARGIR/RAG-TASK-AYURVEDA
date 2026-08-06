import React, { useState } from 'react';
import { SearchType } from '@/types';

interface SearchBarProps {
  onSearch: (query: string, type: SearchType) => void;
  isLoading: boolean;
}

export default function SearchBar({ onSearch, isLoading }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [type, setType] = useState<SearchType>('ingredient');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }
    setError('');
    onSearch(query.trim(), type);
  };

  return (
    <div className="w-full max-w-4xl mx-auto my-8">
      <form onSubmit={handleSubmit} className="relative">
        <div className="flex flex-col md:flex-row shadow-sm rounded-lg overflow-hidden border border-gray-300 bg-white focus-within:ring-2 focus-within:ring-emerald-500 focus-within:border-emerald-500 transition-shadow">
          <select
            value={type}
            onChange={(e) => setType(e.target.value as SearchType)}
            className="px-4 py-3 bg-gray-50 border-r border-gray-300 text-gray-700 font-medium focus:outline-none md:w-48"
          >
            <option value="ingredient">Ingredient / Dravya</option>
            <option value="formulation">Formulation / Yoga</option>
            <option value="disease">Disease / Indication</option>
            <option value="dosage_form">Dosage Form</option>
            <option value="classical_source">Classical Source</option>
          </select>
          
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              if (error) setError('');
            }}
            placeholder="Search Ayurvedic knowledge..."
            className="flex-1 px-4 py-3 focus:outline-none text-gray-800"
          />
          
          <button
            type="submit"
            disabled={isLoading}
            className="px-8 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-medium transition-colors flex items-center justify-center min-w-[120px] disabled:bg-emerald-400"
          >
            {isLoading ? (
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              'Search'
            )}
          </button>
        </div>
        {error && <p className="text-red-500 text-sm mt-2 absolute">{error}</p>}
      </form>
    </div>
  );
}
