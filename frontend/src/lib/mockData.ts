import { SearchResult, RAGResponse } from '@/types';

export const mockSearchResults: Record<string, SearchResult[]> = {
  ashwagandha: [
    {
      id: 'ing-001',
      title: 'Ashwagandha',
      description: 'A popular rasayana (rejuvenator) used for stress and vitality.',
      type: 'ingredient',
      source_document: 'Charaka Samhita',
      location: 'Chikitsa Sthana, 1.1/43',
      evidence_status: 'supported',
      original_passage: 'Ashwagandha original sanskrit text here...',
      english_translation: 'Ashwagandha promotes strength and vitality.',
      metadata: { botanical_name: 'Withania somnifera', rasa: 'Katu, Tikta, Kashaya', guna: 'Laghu, Snigdha' }
    }
  ],
  triphala: [
    {
      id: 'form-001',
      title: 'Triphala Churna',
      description: 'A classic polyherbal formulation consisting of Amalaki, Bibhitaki, and Haritaki.',
      type: 'formulation',
      source_document: 'Sushruta Samhita',
      location: 'Sutra Sthana, 38/56',
      evidence_status: 'supported',
      original_passage: 'Triphala sanskrit text...',
      english_translation: 'Triphala is indicated for digestive health and eye care.',
      metadata: { dosage_form: 'Churna (Powder)', indications: ['Digestive disorders', 'Eye diseases'] }
    }
  ]
};

export const mockRAGResponse: RAGResponse = {
  answer: 'Ashwagandha is widely cited in classical texts as a potent adaptogen and rasayana. It is traditionally used to improve strength, vitality, and support the nervous system. The primary reference for its rejuvenating properties is found in the Charaka Samhita.',
  supporting_passages: [
    'Ashwagandha is classified under the Balya (strength promoting) and Brimhana (nourishing) groups of herbs.'
  ],
  citations: [
    {
      document: 'Charaka Samhita',
      edition_volume: 'Vol 1',
      location: 'Chikitsa Sthana, Chapter 1.1, Verse 43'
    }
  ],
  evidence_status: 'supported'
};

export const mockInsufficientRAGResponse: RAGResponse = {
  answer: 'Insufficient evidence to provide a confident answer based on the available classical texts.',
  supporting_passages: [],
  citations: [],
  evidence_status: 'insufficient_evidence'
};
