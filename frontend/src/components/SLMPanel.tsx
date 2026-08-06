import React from 'react';
import { RAGResponse } from '@/types';

interface SLMPanelProps {
  response: RAGResponse;
  isLoading: boolean;
}

export default function SLMPanel({ response, isLoading }: SLMPanelProps) {
  if (isLoading) {
    return (
      <div className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl p-6 border border-emerald-100 shadow-sm mb-8 animate-pulse">
        <div className="flex items-center mb-4">
          <div className="w-8 h-8 rounded-full bg-emerald-200 mr-3"></div>
          <div className="h-5 bg-emerald-200 rounded w-1/3"></div>
        </div>
        <div className="space-y-3">
          <div className="h-4 bg-emerald-100 rounded w-full"></div>
          <div className="h-4 bg-emerald-100 rounded w-5/6"></div>
          <div className="h-4 bg-emerald-100 rounded w-4/6"></div>
        </div>
      </div>
    );
  }

  const isInsufficient = response.evidence_status === 'insufficient_evidence';

  return (
    <div className={`rounded-2xl p-6 border shadow-sm mb-8 ${isInsufficient ? 'bg-orange-50 border-orange-200' : 'bg-gradient-to-br from-emerald-50 to-teal-50 border-emerald-100'}`}>
      <div className="flex items-center mb-4 pb-4 border-b border-opacity-50 border-gray-300">
        <div className={`w-10 h-10 rounded-full flex items-center justify-center mr-3 text-white ${isInsufficient ? 'bg-orange-500' : 'bg-emerald-600'}`}>
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
        <h2 className={`text-xl font-bold ${isInsufficient ? 'text-orange-900' : 'text-emerald-900'}`}>
          AI Analysis (SLM)
        </h2>
        
        <div className="ml-auto flex items-center">
          <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
            isInsufficient ? 'bg-orange-200 text-orange-800' : 
            response.evidence_status === 'partially_supported' ? 'bg-yellow-200 text-yellow-800' : 
            'bg-emerald-200 text-emerald-800'
          }`}>
            {response.evidence_status.replace('_', ' ').toUpperCase()}
          </span>
        </div>
      </div>

      <div className="prose prose-emerald max-w-none">
        {isInsufficient ? (
          <div className="flex items-start text-orange-800 bg-orange-100 p-4 rounded-lg">
            <svg className="w-6 h-6 mr-3 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <p className="font-medium m-0">{response.answer}</p>
          </div>
        ) : (
          <div className="text-gray-800 text-lg leading-relaxed">
            {response.answer}
          </div>
        )}
      </div>

      {!isInsufficient && response.citations.length > 0 && (
        <div className="mt-6 pt-4 border-t border-emerald-200/50">
          <h3 className="text-sm font-bold text-emerald-800 mb-3 uppercase tracking-wider">Supporting References</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {response.citations.map((cite, idx) => (
              <div key={idx} className="bg-white/60 p-3 rounded-lg border border-emerald-100 text-sm flex items-start">
                <svg className="w-4 h-4 text-emerald-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
                <div>
                  <div className="font-semibold text-gray-800">{cite.document} <span className="font-normal text-gray-500">({cite.edition_volume})</span></div>
                  <div className="text-gray-600 text-xs mt-1">{cite.location}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {!isInsufficient && response.supporting_passages.length > 0 && (
        <div className="mt-4">
          <details className="group">
            <summary className="flex items-center cursor-pointer text-sm font-medium text-emerald-700 hover:text-emerald-800">
              <svg className="w-4 h-4 mr-1 transform transition-transform group-open:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
              </svg>
              View Extracted Passages
            </summary>
            <div className="mt-3 p-4 bg-white/50 rounded-lg border border-emerald-100 text-sm text-gray-700 italic space-y-2">
              {response.supporting_passages.map((passage, idx) => (
                <p key={idx}>"{passage}"</p>
              ))}
            </div>
          </details>
        </div>
      )}
    </div>
  );
}
