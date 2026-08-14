"""Knowledge graph for structured incident context"""
from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum

class EntityType(Enum):
    SERVICE = "service"
    METRIC = "metric"
    ERROR = "error"
    DEPLOYMENT = "deployment"

@dataclass
class Entity:
    id: str
    type: EntityType
    name: str
    description: str

@dataclass
class Relationship:
    source_id: str
    target_id: str
    relation_type: str  # "causes", "correlates_with", "depends_on"
    strength: float  # 0-1 confidence

class KnowledgeGraph:
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
    
    def add_entity(self, entity: Entity):
        self.entities[entity.id] = entity
    
    def add_relationship(self, rel: Relationship):
        self.relationships.append(rel)
    
    def find_related_entities(self, entity_id: str, relation_type: str = None) -> List[Entity]:
        """Find all entities connected to given entity"""
        related_ids = set()
        
        for rel in self.relationships:
            if rel.source_id == entity_id:
                if relation_type is None or rel.relation_type == relation_type:
                    related_ids.add(rel.target_id)
            elif rel.target_id == entity_id:
                if relation_type is None or rel.relation_type == relation_type:
                    related_ids.add(rel.source_id)
        
        return [self.entities[eid] for eid in related_ids if eid in self.entities]
    
    def get_evidence_for_hypothesis(self, hypothesis: str) -> Dict[str, float]:
        """Find supporting evidence for a hypothesis"""
        supporting = {}
        
        for entity_id, entity in self.entities.items():
            if any(word in entity.name.lower() for word in hypothesis.split()):
                related = self.find_related_entities(entity_id)
                for rel_entity in related:
                    supporting[f"{entity.name} -> {rel_entity.name}"] = 0.8
        
        return dict(sorted(supporting.items(), key=lambda x: x[1], reverse=True))
