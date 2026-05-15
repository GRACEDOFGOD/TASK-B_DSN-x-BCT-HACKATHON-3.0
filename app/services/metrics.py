"""
Evaluation Metrics — Task B scoring
NDCG@10, Hit Rate@10, Cold-Start success rate
Exact metrics used by the competition judges.
"""

import math
import numpy as np
from typing import List, Dict, Any


def compute_ndcg_at_k(
    recommended_items: List[str],
    relevant_items: List[str],
    k: int = 10,
) -> float:
    """
    Normalized Discounted Cumulative Gain @ K

    Measures ranking quality — rewards putting relevant items higher.
    Score 0.0 (bad) to 1.0 (perfect ranking).
    """
    dcg = 0.0
    for i, item in enumerate(recommended_items[:k]):
        if item in relevant_items:
            dcg += 1.0 / math.log2(i + 2)  # log2(position + 1), 1-indexed

    # Ideal DCG — all relevant items ranked first
    ideal_hits = min(len(relevant_items), k)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))

    return round(dcg / idcg, 4) if idcg > 0 else 0.0


def compute_hit_rate_at_k(
    recommended_items: List[str],
    relevant_items: List[str],
    k: int = 10,
) -> float:
    """
    Hit Rate @ K

    Binary: 1.0 if at least one relevant item appears in top-K, else 0.0.
    """
    top_k = set(recommended_items[:k])
    return 1.0 if top_k & set(relevant_items) else 0.0


def compute_precision_at_k(
    recommended_items: List[str],
    relevant_items: List[str],
    k: int = 10,
) -> float:
    """Precision@K — fraction of top-K that are relevant."""
    top_k = recommended_items[:k]
    hits = sum(1 for item in top_k if item in relevant_items)
    return round(hits / k, 4) if k > 0 else 0.0


def compute_recall_at_k(
    recommended_items: List[str],
    relevant_items: List[str],
    k: int = 10,
) -> float:
    """Recall@K — fraction of relevant items found in top-K."""
    if not relevant_items:
        return 0.0
    top_k = set(recommended_items[:k])
    hits = len(top_k & set(relevant_items))
    return round(hits / len(relevant_items), 4)


def evaluate_recommendations(
    recommendations: List[Dict[str, Any]],
    ground_truth: List[str],
    k: int = 10,
) -> Dict[str, float]:
    """
    Full evaluation suite for a single recommendation list.

    Args:
        recommendations: List of recommendation dicts with 'item_name' key
        ground_truth: List of relevant item names
        k: Cut-off (default 10)

    Returns:
        Dict with ndcg, hit_rate, precision, recall
    """
    rec_names = [r["item_name"] for r in recommendations]

    return {
        "ndcg_at_k": compute_ndcg_at_k(rec_names, ground_truth, k),
        "hit_rate_at_k": compute_hit_rate_at_k(rec_names, ground_truth, k),
        "precision_at_k": compute_precision_at_k(rec_names, ground_truth, k),
        "recall_at_k": compute_recall_at_k(rec_names, ground_truth, k),
        "k": k,
        "num_recommended": len(rec_names),
        "num_relevant": len(ground_truth),
    }


# Ground truth relevant items per persona (from competition evaluation design)
GROUND_TRUTH: Dict[str, List[str]] = {
    "persona_001": [
        "Tecno Camon 30 Pro", "Samsung Galaxy A54",
        "JBL Portable Speaker", "Atomic Habits — James Clear",
        "Audiomack Music App",
    ],
    "persona_002": [
        "MAC Studio Fix Foundation", "Ankara Print Dress",
        "Netflix Nigeria Subscription", "Chicken Republic",
        "Purple Hibiscus — Chimamanda Adichie",
    ],
    "persona_003": [
        "Suya Spot PH", "Buka Local Restaurant",
        "DSTV Premium Package", "Smokey Joes Bar and Grill",
        "Audiomack Music App",
    ],
    "persona_004": [
        "Medical Biochemistry — Baynes",
        "Things Fall Apart — Chinua Achebe",
        "Transcorp Hilton Restaurant",
        "Atomic Habits — James Clear",
        "Cowrywise Investment App",
    ],
    "persona_005": [
        "PUBG Mobile", "Indomie Noodles",
        "Audiomack Music App", "Chicken Republic",
        "Showmax Nigeria",
    ],
    "persona_006": [
        "Purple Hibiscus — Chimamanda Adichie",
        "Chi Exotic Juice", "Konga Grocery Delivery",
        "Atomic Habits — James Clear",
        "Cowrywise Investment App",
    ],
    "persona_007": [
        "Zero to One — Peter Thiel",
        "Opay POS Machine",
        "Rich Dad Poor Dad — Robert Kiyosaki",
        "Transcorp Hilton Restaurant",
        "How to Win Friends — Dale Carnegie",
    ],
    "persona_008": [
        "Atomic Habits — James Clear",
        "Kano Suya Spot",
        "Cowrywise Investment App",
        "Udemy Online Course (Tech)",
        "Indomie Noodles",
    ],
}
