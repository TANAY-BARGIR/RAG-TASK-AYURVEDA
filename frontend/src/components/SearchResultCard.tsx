import React from 'react';
import { SearchResult } from '@/types';

interface SearchResultCardProps {
  result: SearchResult;
  onViewReference: (result: SearchResult) => void;
}

export default function SearchResultCard({ result, onViewReference }: SearchResultCardProps) {
  const getEvidenceColor = (status: string) => {
    switch (status) {
      case 'supported':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'partially_supported':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'insufficient_evidence':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatEvidenceStatus = (status: string) => {
    return status.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <div>
          <span className="inline-block px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 mb-2 uppercase tracking-wide">
            {result.type.replace('_', ' ')}
          </span>
          <h3 className="text-xl font-bold text-gray-900">{result.title}</h3>
        </div>
        <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${getEvidenceColor(result.evidence_status)}`}>
          {formatEvidenceStatus(result.evidence_status)}
        </span>
      </div>
      
      <p className="text-gray-600 mb-4 line-clamp-2">{result.description}</p>
      
      <div className="bg-gray-50 rounded-lg p-3 mb-4 text-sm border border-gray-100 flex items-start">
        <svg className="w-5 h-5 text-gray-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
        </svg>
        <div>
          <span className="font-semibold text-gray-700">{result.source_document}</span>
          <span className="text-gray-500 ml-2">• {result.location}</span>
        </div>
      </div>
      
      <div className="flex justify-end">
        <button
          onClick={() => onViewReference(result)}
          className="text-emerald-600 hover:text-emerald-700 font-medium text-sm flex items-center transition-colors"
        >
          View Full Reference
          <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
          </svg>
        </button>
      </div>
    </div>
  );
}
