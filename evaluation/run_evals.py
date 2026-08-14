"""Run evaluation on all incidents"""
import json
from evaluation.incidents import INCIDENTS
from evaluation.rag_evaluator import RAGEvaluator

def main():
    evaluator = RAGEvaluator()
    results = []
    
    for incident in INCIDENTS:
        incident_id = incident["incident_id"]
        description = incident["description"]
        evidence = incident["evidence"]
        ground_truth = incident["ground_truth"]
        
        # Simulate RAG retrieval (for now, just use all logs as retrieved)
        retrieved = evidence.get("logs", [])
        
        # Evaluate
        rag_metrics = evaluator.evaluate_retrieval(
            query=description,
            retrieved_evidence=retrieved,
            ground_truth_evidence=evidence
        )
        
        results.append({
            "incident_id": incident_id,
            "root_cause": ground_truth["root_cause"],
            "severity": ground_truth["severity"],
            "rag_metrics": rag_metrics
        })
        
        print(f"\n{incident_id}:")
        print(f"  Root Cause: {ground_truth['root_cause']}")
        print(f"  Severity: {ground_truth['severity']}")
        print(f"  RAG F1: {rag_metrics['f1']}")
    
    # Summary
    avg_f1 = sum(r["rag_metrics"]["f1"] for r in results) / len(results)
    print(f"\n{'='*50}")
    print(f"Average RAG F1: {avg_f1}")
    print(f"{'='*50}")
    
    # Save results
    with open("evaluation/results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to evaluation/results.json")

if __name__ == "__main__":
    main()
