'use client';

import React, { useState } from 'react';
import SearchBar from '@/components/SearchBar';
import SearchResultCard from '@/components/SearchResultCard';
import SLMPanel from '@/components/SLMPanel';
import ReferenceModal from '@/components/ReferenceModal';
import { SearchResult, SearchType, RAGResponse } from '@/types';
import { mockSearchResults, mockRAGResponse, mockInsufficientRAGResponse } from '@/lib/mockData';

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [ragResponse, setRagResponse] = useState<RAGResponse | null>(null);
  const [selectedReference, setSelectedReference] = useState<SearchResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string, type: SearchType) => {
    setIsLoading(true);
    setHasSearched(true);
    setError(null);
    setRagResponse(null);
    setResults([]);

    try {
      const useMock = process.env.NEXT_PUBLIC_USE_MOCK_API === 'true';
      
      if (useMock) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const mockKey = query.toLowerCase().includes('ashwagandha') ? 'ashwagandha' : 
                        query.toLowerCase().includes('triphala') ? 'triphala' : null;
        
        if (mockKey) {
          setResults(mockSearchResults[mockKey]);
          // If query is broad/open-ended, show RAG
          if (mockKey === 'ashwagandha') {
             setRagResponse(mockRAGResponse);
          }
        } else {
          setResults([]);
          // Show insufficient RAG if no direct hits but might be a question
          if (query.split(' ').length > 2) {
             setRagResponse(mockInsufficientRAGResponse);
          }
        }
      } else {
        // Real API calls
        const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
        
        // 1. Fetch structured search results
        const searchRes = await fetch(`${baseUrl}/api/search?q=${encodeURIComponent(query)}&type=${type}`);
        if (!searchRes.ok) throw new Error('Failed to fetch search results');
        const searchData = await searchRes.json();
        setResults(searchData.results || []);

        // 2. Fetch RAG response if it's a descriptive query (e.g., > 2 words or specific trigger)
        // In a real app, backend might decide when to trigger this, or we always query it.
        try {
          const ragRes = await fetch(`${baseUrl}/api/rag/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, type })
          });
          
          if (ragRes.ok) {
            const ragData = await ragRes.json();
            setRagResponse(ragData);
          }
        } catch (ragErr) {
          console.error("RAG fetch error:", ragErr);
          // Don't fail the whole search if RAG fails
        }
      }
    } catch (err) {
      console.error(err);
      setError('An error occurred while fetching the results. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12 max-w-5xl">
      <div className="text-center mb-10">
        <h1 className="text-4xl md:text-5xl font-extrabold text-emerald-900 mb-4 tracking-tight">
          Ayurvedic Reference Intelligence
        </h1>
        <p className="text-lg text-emerald-700/80 max-w-2xl mx-auto">
          Search authentic classical texts, ingredients, and formulations with citation-backed AI answers.
        </p>
      </div>

      <SearchBar onSearch={handleSearch} isLoading={isLoading} />

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded-r-lg flex items-start">
          <svg className="w-5 h-5 text-red-500 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {hasSearched && (
        <div className="mt-8">
          {(isLoading || ragResponse) && (
            <SLMPanel response={ragResponse!} isLoading={isLoading && !ragResponse} />
          )}

          {!isLoading && results.length > 0 && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                Structured Knowledge Records
                <span className="ml-3 bg-gray-100 text-gray-600 py-1 px-3 rounded-full text-sm font-medium">
                  {results.length} found
                </span>
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {results.map((result) => (
                  <SearchResultCard 
                    key={result.id} 
                    result={result} 
                    onViewReference={setSelectedReference} 
                  />
                ))}
              </div>
            </div>
          )}

          {!isLoading && results.length === 0 && !error && !ragResponse && (
            <div className="text-center py-16 bg-white rounded-2xl border border-gray-200 shadow-sm">
              <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              <h3 className="text-xl font-medium text-gray-900 mb-2">No results found</h3>
              <p className="text-gray-500">We couldn't find any classical references matching your query. Try different keywords or search type.</p>
            </div>
          )}
        </div>
      )}

      <ReferenceModal 
        result={selectedReference} 
        onClose={() => setSelectedReference(null)} 
      />
    </div>
  );
}
