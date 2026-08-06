export type SearchType = 'ingredient' | 'formulation' | 'disease' | 'dosage_form' | 'classical_source';

export interface SearchResult {
  id: string;
  title: string;
  description: string;
  type: SearchType;
  source_document: string;
  location: string; // chapter/section/page/verse
  evidence_status: 'supported' | 'partially_supported' | 'insufficient_evidence';
  original_passage?: string;
  english_translation?: string;
  metadata?: Record<string, any>;
}

export interface RAGResponse {
  answer: string;
  supporting_passages: string[];
  citations: {
    document: string;
    edition_volume: string;
    location: string;
  }[];
  evidence_status: 'supported' | 'partially_supported' | 'insufficient_evidence';
}
