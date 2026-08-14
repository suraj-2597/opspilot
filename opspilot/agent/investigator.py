"""Agentic incident investigator with improved refinement"""
from dataclasses import dataclass

@dataclass
class InvestigationStep:
    iteration: int
    hypothesis: str
    evidence_gathered: list
    confidence: float
    action: str

class IncidentInvestigator:
    def __init__(self, retriever, knowledge_graph, max_iterations: int = 5):
        self.retriever = retriever
        self.kg = knowledge_graph
        self.max_iterations = max_iterations
        self.investigation_log = []
    
    def investigate(self, incident_description: str) -> dict:
        """Main investigation loop"""
        
        hypothesis = incident_description
        confidence = 0.0
        all_evidence = []
        iteration = 0
        
        print(f"\n{'='*70}")
        print(f"INCIDENT INVESTIGATION")
        print(f"{'='*70}")
        print(f"\nIncident: {incident_description}\n")
        
        while iteration < self.max_iterations and confidence < 0.85:
            iteration += 1
            
            print(f"--- Iteration {iteration} ---")
            print(f"Hypothesis: {hypothesis}")
            
            # Gather evidence
            evidence = self.retriever.retrieve(hypothesis)
            all_evidence.extend([e["doc"] for e in evidence])
            
            # Score confidence based on evidence quality
            confidence = self._score_hypothesis(evidence)
            
            # Log step
            step = InvestigationStep(
                iteration=iteration,
                hypothesis=hypothesis,
                evidence_gathered=[e["doc"][:60] for e in evidence[:2]],
                confidence=confidence,
                action=self._decide_action(confidence)
            )
            self.investigation_log.append(step)
            
            print(f"Confidence: {confidence:.2%}")
            if evidence:
                print(f"Top Evidence: {evidence[0]['doc'][:70]}...")
            print(f"Action: {step.action}\n")
            
            # Smart refinement
            if confidence < 0.75 and iteration < self.max_iterations:
                hypothesis = self._smart_refine(incident_description, evidence, iteration)
            else:
                break
        
        print(f"{'='*70}")
        print(f"FINAL RESULT")
        print(f"{'='*70}")
        
        return {
            "root_cause": self._extract_root_cause(all_evidence),
            "confidence": confidence,
            "iterations": iteration,
            "evidence_count": len(all_evidence),
            "investigation_path": [
                {
                    "iteration": s.iteration,
                    "hypothesis": s.hypothesis,
                    "confidence": s.confidence,
                    "action": s.action
                }
                for s in self.investigation_log
            ]
        }
    
    def _score_hypothesis(self, evidence: list) -> float:
        """Score based on top evidence quality"""
        if not evidence:
            return 0.0
        
        # Use the fusion score from retriever
        top_score = evidence[0].get("fusion_score", 0)
        return min(top_score * 0.95, 1.0)
    
    def _decide_action(self, confidence: float) -> str:
        if confidence > 0.80:
            return "RESOLVE - High confidence"
        elif confidence > 0.6:
            return "REFINE - Improve precision"
        else:
            return "SEARCH - Gather more evidence"
    
    def _smart_refine(self, original: str, evidence: list, iteration: int) -> str:
        """Smart hypothesis refinement strategy"""
        if not evidence:
            return original
        
        # Strategy: Focus on the top evidence
        top_doc = evidence[0]["doc"]
        
        # Iteration 1: Search for service names
        if iteration == 1:
            for service in ["checkout", "order", "payment", "database", "notification"]:
                if service in original.lower() and service in top_doc.lower():
                    return f"{service} service {' '.join(top_doc.split()[2:5])}"
        
        # Iteration 2: Search for error patterns
        if iteration == 2:
            error_patterns = ["timeout", "exhausted", "degradation", "errors", "backed"]
            for pattern in error_patterns:
                if pattern in top_doc.lower():
                    return top_doc[:80]
        
        # Iteration 3: Use specific evidence
        if iteration >= 3:
            return top_doc
        
        return original
    
    def _extract_root_cause(self, all_evidence: list) -> str:
        """Extract most likely root cause from evidence"""
        if not all_evidence:
            return "Unknown"
        
        # Most frequently appearing cause
        cause_keywords = {
            "connection pool": "Database connection pool exhausted",
            "timeout": "Service timeout or latency issue",
            "degradation": "API degradation",
            "backed": "Queue backup",
            "leak": "Memory leak"
        }
        
        for keyword, cause in cause_keywords.items():
            for evidence in all_evidence:
                if keyword in evidence.lower():
                    return cause
        
        return all_evidence[0][:80]
