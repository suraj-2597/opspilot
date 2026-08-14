"""Run complete OpsPilot advanced system"""
from opspilot.rag.retriever import DenseSparseRetriever
from opspilot.rag.knowledge_graph import KnowledgeGraph
from opspilot.agent.investigator import IncidentInvestigator
from evaluation.benchmarks import BenchmarkSuite
import json

# Production knowledge base
knowledge_base = [
    "Database connection pool exhausted due to increased traffic",
    "Payment gateway API experiencing degradation and timeouts",
    "Message queue backed up causing notification delays",
    "CPU usage high on order service due to inefficient queries",
    "Memory leak detected in payment processing service",
    "Checkout service returning 500 errors from upstream",
    "Order service database query timeout after 30 seconds",
    "Connection pool utilization at 100%",
    "Recent deployment causing regression in payment flow",
    "DNS resolution failures for external payment gateway",
    "Service mesh circuit breaker open for order-db",
    "High latency on checkout API endpoints",
]

# Test incidents
test_incidents = [
    {
        "id": "inc-001",
        "description": "Checkout service failing with 500 errors and database timeouts",
        "ground_truth": "Database connection pool exhausted"
    },
    {
        "id": "inc-002",
        "description": "Payment requests experiencing high latency and failures",
        "ground_truth": "Payment gateway degradation"
    },
    {
        "id": "inc-003",
        "description": "Users not receiving order notifications",
        "ground_truth": "Message queue backed up"
    }
]

print("\n" + "="*70)
print("OpsPilot Advanced AI System - Complete Evaluation")
print("="*70)

# Initialize components
retriever = DenseSparseRetriever(knowledge_base)
kg = KnowledgeGraph()
agent = IncidentInvestigator(retriever, kg, max_iterations=5)

# Run investigations
results = []
for incident in test_incidents:
    print(f"\n\n{'#'*70}")
    print(f"# Testing: {incident['id']}")
    print(f"{'#'*70}")
    
    result = agent.investigate(incident["description"])
    result["incident_id"] = incident["id"]
    result["ground_truth"] = incident["ground_truth"]
    results.append(result)

# Generate benchmarks
suite = BenchmarkSuite(test_incidents)
report = suite.generate_report(results)

print("\n\n" + "="*70)
print("BENCHMARK REPORT")
print("="*70)
print(json.dumps(report, indent=2))

# Save results
with open("evaluation/system_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n✅ Results saved to evaluation/system_results.json")
print(f"✅ Processed {len(results)} incidents with average confidence: {report['metrics']['avg_confidence']:.2%}")
