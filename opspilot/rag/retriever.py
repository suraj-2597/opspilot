"""Production RAG pipeline with dense-sparse retrieval"""
import numpy as np
from rank_bm25 import BM25Okapi
from dataclasses import dataclass

@dataclass
class RetrievalConfig:
    dense_weight: float = 0.65
    sparse_weight: float = 0.35
    top_k: int = 10
    rerank_top_k: int = 5

class DenseSparseRetriever:
    """Hybrid retrieval combining BM25 (sparse) and TF-IDF (dense)"""
    
    def __init__(self, documents: list, config: RetrievalConfig = None):
        self.config = config or RetrievalConfig()
        self.documents = documents
        
        self.tokenized = [d.split() for d in documents]
        self.bm25 = BM25Okapi(self.tokenized)
        
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.embeddings = self.vectorizer.fit_transform(documents).toarray()
    
    def retrieve(self, query: str) -> list:
        """End-to-end retrieval with hybrid fusion"""
        sparse_scores = self._sparse_score(query)
        dense_scores = self._dense_score(query)
        
        fused_scores = (
            self.config.sparse_weight * sparse_scores +
            self.config.dense_weight * dense_scores
        )
        
        top_indices = np.argsort(fused_scores)[::-1][:self.config.top_k]
        
        candidates = []
        for i in top_indices:
            candidates.append({
                "doc": self.documents[i],
                "fusion_score": float(fused_scores[i]),
                "sparse_score": float(sparse_scores[i]),
                "dense_score": float(dense_scores[i]),
                "rank": len(candidates) + 1
            })
        
        return candidates[:self.config.rerank_top_k]
    
    def _sparse_score(self, query: str) -> np.ndarray:
        """BM25 keyword-based scores"""
        scores = self.bm25.get_scores(query.split())
        if scores.max() > 0:
            return (scores - scores.min()) / (scores.max() - scores.min() + 1e-6)
        return scores
    
    def _dense_score(self, query: str) -> np.ndarray:
        """TF-IDF semantic similarity scores"""
        from sklearn.metrics.pairwise import cosine_similarity
        query_embedding = self.vectorizer.transform([query]).toarray()
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        if similarities.max() > 0:
            return (similarities - similarities.min()) / (similarities.max() - similarities.min() + 1e-6)
        return similarities
