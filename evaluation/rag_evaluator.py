"""Evaluate RAG retrieval quality"""
from evaluation.incidents import INCIDENTS

class RAGEvaluator:
    def __init__(self):
        self.incidents = INCIDENTS
    
    def evaluate_retrieval(self, query, retrieved_evidence, ground_truth_evidence):
        """
        Simple evaluation: how much relevant evidence was retrieved?
        Returns: precision, recall, f1
        """
        retrieved_set = set(str(e).lower() for e in retrieved_evidence)
        ground_truth_set = set(str(e).lower() for e in ground_truth_evidence.get("logs", []))
        
        if len(retrieved_set) == 0:
            return {"precision": 0, "recall": 0, "f1": 0}
        
        true_positives = len(retrieved_set & ground_truth_set)
        false_positives = len(retrieved_set - ground_truth_set)
        false_negatives = len(ground_truth_set - retrieved_set)
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
            "true_positives": true_positives,
            "false_positives": false_positives
        }
