import React from 'react';
import { SearchResult } from '@/types';

interface ReferenceModalProps {
  result: SearchResult | null;
  onClose: () => void;
}

export default function ReferenceModal({ result, onClose }: ReferenceModalProps) {
  if (!result) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm transition-opacity">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-3xl max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="flex justify-between items-center p-5 border-b border-gray-200 bg-gray-50/50">
          <h2 className="text-xl font-bold text-gray-900 pr-8 line-clamp-1">{result.title}</h2>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 p-1.5 rounded-full transition-colors"
            aria-label="Close modal"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        {/* Body */}
        <div className="p-6 overflow-y-auto flex-1">
          <div className="flex items-center space-x-3 mb-6">
            <span className="inline-block px-3 py-1 rounded-md text-xs font-semibold bg-emerald-100 text-emerald-800 uppercase tracking-wider">
              {result.type.replace('_', ' ')}
            </span>
            <span className="inline-block px-3 py-1 rounded-md text-xs font-semibold bg-gray-100 text-gray-700">
              {result.source_document}
            </span>
          </div>

          <div className="mb-8">
            <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-2">Description</h3>
            <p className="text-gray-800 text-lg leading-relaxed">{result.description}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-amber-50/50 rounded-xl p-5 border border-amber-100">
              <h3 className="text-sm font-bold text-amber-800 uppercase tracking-wider mb-3 flex items-center">
                <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Original Source Text
              </h3>
              {result.original_passage ? (
                <p className="text-gray-700 font-serif italic text-lg leading-relaxed bg-white/60 p-4 rounded-lg border border-amber-100/50 shadow-inner">
                  {result.original_passage}
                </p>
              ) : (
                <p className="text-gray-500 italic text-sm">Original text not available.</p>
              )}
            </div>

            <div className="bg-blue-50/50 rounded-xl p-5 border border-blue-100">
              <h3 className="text-sm font-bold text-blue-800 uppercase tracking-wider mb-3 flex items-center">
                <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path>
                </svg>
                English Translation
              </h3>
              {result.english_translation ? (
                <p className="text-gray-700 text-base leading-relaxed bg-white/60 p-4 rounded-lg border border-blue-100/50 shadow-inner">
                  {result.english_translation}
                </p>
              ) : (
                <p className="text-gray-500 italic text-sm">Translation not available.</p>
              )}
            </div>
          </div>

          <div className="mb-6">
            <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3 border-b border-gray-100 pb-2">Reference Metadata</h3>
            <div className="bg-gray-50 rounded-lg p-4 grid grid-cols-1 sm:grid-cols-2 gap-y-4 gap-x-6 text-sm">
              <div>
                <span className="block text-gray-500 mb-1 text-xs font-semibold uppercase">Document</span>
                <span className="font-medium text-gray-900">{result.source_document}</span>
              </div>
              <div>
                <span className="block text-gray-500 mb-1 text-xs font-semibold uppercase">Location</span>
                <span className="font-medium text-gray-900">{result.location}</span>
              </div>
              <div>
                <span className="block text-gray-500 mb-1 text-xs font-semibold uppercase">Evidence Status</span>
                <span className="font-medium text-gray-900">{result.evidence_status.replace('_', ' ')}</span>
              </div>
            </div>
          </div>

          {result.metadata && Object.keys(result.metadata).length > 0 && (
            <div>
              <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3 border-b border-gray-100 pb-2">Additional Properties</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
                {Object.entries(result.metadata).map(([key, value]) => (
                  <div key={key} className="bg-gray-50 rounded p-3 flex justify-between items-center">
                    <span className="text-gray-600 font-medium capitalize">{key.replace(/_/g, ' ')}</span>
                    <span className="text-gray-900 font-semibold text-right">
                      {Array.isArray(value) ? value.join(', ') : value}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
        
        {/* Footer */}
        <div className="p-4 border-t border-gray-200 bg-gray-50 flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-white border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-200 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
