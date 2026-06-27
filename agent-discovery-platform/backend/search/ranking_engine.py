from typing import List, Dict, Any

class RankingEngine:
    """
    Implements the 8-Factor Weighted Ranking algorithm.
    """
    
    # Ranking Weights
    WEIGHTS = {
        "semantic_similarity": 0.40,
        "capability_match": 0.20,
        "usage_popularity": 0.10,
        "success_rate": 0.10,
        "documentation_quality": 0.05,
        "freshness": 0.05,
        "compliance_score": 0.05,
        "health_score": 0.05
    }
    
    def rank_candidates(self, query_context: Dict[str, Any], candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ranked = []
        
        for candidate in candidates:
            # 1. Semantic Similarity (from Qdrant search score)
            sim_score = candidate.get("_score", 0.0)
            
            # 2. Capability Match (Jaccard similarity approximation)
            req_caps = set(query_context.get("capabilities", []))
            cand_caps = set(candidate.get("capabilities", []))
            cap_score = 0.0
            if req_caps:
                intersection = len(req_caps.intersection(cand_caps))
                union = len(req_caps.union(cand_caps))
                cap_score = intersection / union if union > 0 else 0.0
                
            # 3-8. Other factors (mocked for MVP, normally fetched from DB/Analytics)
            popularity_score = candidate.get("normalized_popularity", 0.5)
            success_score = candidate.get("success_rate", 0.9)
            doc_score = 1.0 if candidate.get("description") else 0.5
            freshness_score = 0.8
            compliance_score = 1.0 if candidate.get("status") == "PRODUCTION" else 0.5
            health_score = 0.95
            
            # Calculate composite score
            composite = (
                self.WEIGHTS["semantic_similarity"] * sim_score +
                self.WEIGHTS["capability_match"] * cap_score +
                self.WEIGHTS["usage_popularity"] * popularity_score +
                self.WEIGHTS["success_rate"] * success_score +
                self.WEIGHTS["documentation_quality"] * doc_score +
                self.WEIGHTS["freshness"] * freshness_score +
                self.WEIGHTS["compliance_score"] * compliance_score +
                self.WEIGHTS["health_score"] * health_score
            )
            
            candidate["composite_score"] = composite
            ranked.append(candidate)
            
        # Sort by composite score descending
        ranked.sort(key=lambda x: x["composite_score"], reverse=True)
        return ranked

ranking_engine = RankingEngine()
