"""
Tests — Task B Recommendation Agent
Run: python -m unittest discover -s tests -p '*.py'
"""

import math
import unittest
from app.services.metrics import (
    compute_ndcg_at_k,
    compute_hit_rate_at_k,
    compute_precision_at_k,
    compute_recall_at_k,
    evaluate_recommendations,
)
from app.services.agent import score_items_for_persona
from app.data.catalog import ALL_ITEMS, FOOD_ITEMS, BOOK_ITEMS
from app.data.personas import USER_PERSONAS


# ── Metrics tests ──────────────────────────────────────────────────────────

class TestNDCG(unittest.TestCase):
    def test_perfect_ranking(self):
        recs = ["A", "B", "C"]
        rel = ["A", "B", "C"]
        assert compute_ndcg_at_k(recs, rel, k=3) == 1.0

    def test_zero_hits(self):
        recs = ["X", "Y", "Z"]
        rel = ["A", "B", "C"]
        assert compute_ndcg_at_k(recs, rel, k=3) == 0.0

    def test_partial_hit_top(self):
        recs = ["A", "X", "Y"]
        rel = ["A"]
        score = compute_ndcg_at_k(recs, rel, k=3)
        assert score == 1.0  # Only 1 relevant, it's at rank 1

    def test_partial_hit_low(self):
        recs = ["X", "Y", "A"]
        rel = ["A"]
        score = compute_ndcg_at_k(recs, rel, k=3)
        assert score < 1.0  # Relevant item at rank 3, not ideal

    def test_empty_recommendations(self):
        assert compute_ndcg_at_k([], ["A"], k=10) == 0.0

    def test_empty_relevant(self):
        assert compute_ndcg_at_k(["A", "B"], [], k=10) == 0.0


class TestHitRate(unittest.TestCase):
    def test_hit(self):
        recs = ["A", "B", "C"]
        rel = ["C", "D"]
        assert compute_hit_rate_at_k(recs, rel, k=3) == 1.0

    def test_miss(self):
        recs = ["X", "Y", "Z"]
        rel = ["A", "B"]
        assert compute_hit_rate_at_k(recs, rel, k=3) == 0.0

    def test_hit_beyond_k(self):
        recs = ["X", "Y", "Z", "A"]
        rel = ["A"]
        # A is at position 4, k=3 — should miss
        assert compute_hit_rate_at_k(recs, rel, k=3) == 0.0


class TestPrecisionRecall(unittest.TestCase):
    def test_precision(self):
        recs = ["A", "B", "X"]
        rel = ["A", "B", "C"]
        p = compute_precision_at_k(recs, rel, k=3)
        assert math.isclose(p, 2/3, rel_tol=1e-3)

    def test_recall(self):
        recs = ["A", "B", "X"]
        rel = ["A", "B", "C", "D"]
        r = compute_recall_at_k(recs, rel, k=3)
        assert math.isclose(r, 2/4, rel_tol=1e-3)


# ── Scoring tests ──────────────────────────────────────────────────────────

class TestItemScoring(unittest.TestCase):
    def test_scores_all_items(self):
        persona = USER_PERSONAS["persona_001"]
        taste_profile = {
            "top_domains": ["electronics", "food"],
            "price_preference": "mid",
            "key_interests": ["tech", "music"],
            "avoid_tags": [],
            "personality_type": "value_hunter",
        }
        scored = score_items_for_persona(persona, taste_profile, ALL_ITEMS)
        assert len(scored) == len(ALL_ITEMS)

    def test_sorted_descending(self):
        persona = USER_PERSONAS["persona_005"]
        taste_profile = {
            "top_domains": ["entertainment", "food"],
            "price_preference": "budget",
            "key_interests": ["gaming", "music", "cheap food"],
            "avoid_tags": [],
            "personality_type": "value_hunter",
        }
        scored = score_items_for_persona(persona, taste_profile, ALL_ITEMS)
        scores = [s["score"] for s in scored]
        assert scores == sorted(scores, reverse=True)

    def test_domain_match_boosts_score(self):
        taste_profile = {
            "top_domains": ["books"],
            "price_preference": "budget",
            "key_interests": [],
            "avoid_tags": [],
        }
        persona = USER_PERSONAS["persona_004"]
        scored = score_items_for_persona(persona, taste_profile, ALL_ITEMS)
        book_scores = [s["score"] for s in scored if s["domain"] == "books"]
        non_book_scores = [s["score"] for s in scored if s["domain"] != "books"]
        assert max(book_scores) > min(non_book_scores)

    def test_exclude_ids(self):
        taste_profile = {
            "top_domains": ["food"],
            "price_preference": "budget",
            "key_interests": [],
            "avoid_tags": [],
        }
        persona = USER_PERSONAS["persona_003"]
        exclude = [FOOD_ITEMS[0]["id"]]
        scored = score_items_for_persona(
            persona, taste_profile, ALL_ITEMS, exclude_ids=exclude
        )
        ids = [s["id"] for s in scored]
        assert FOOD_ITEMS[0]["id"] not in ids

    def test_avoid_tags_reduce_score(self):
        taste_profile = {
            "top_domains": ["food"],
            "price_preference": "budget",
            "key_interests": [],
            "avoid_tags": ["nigerian", "local"],
        }
        persona = USER_PERSONAS["persona_001"]
        scored = score_items_for_persona(persona, taste_profile, ALL_ITEMS)
        buka = next((s for s in scored if s["id"] == "f002"), None)
        assert buka is not None
        assert buka["score"] < 30  # penalised heavily


# ── Catalog tests ──────────────────────────────────────────────────────────

class TestCatalog(unittest.TestCase):
    def test_all_items_have_required_fields(self):
        required = {"id", "name", "domain", "category", "price_range", "tags", "avg_rating", "popularity"}
        for item in ALL_ITEMS:
            missing = required - set(item.keys())
            assert not missing, f"Item {item.get('id')} missing: {missing}"

    def test_no_duplicate_ids(self):
        ids = [i["id"] for i in ALL_ITEMS]
        assert len(ids) == len(set(ids))

    def test_ratings_in_range(self):
        for item in ALL_ITEMS:
            assert 1.0 <= item["avg_rating"] <= 5.0

    def test_popularity_in_range(self):
        for item in ALL_ITEMS:
            assert 0.0 <= item["popularity"] <= 1.0


# ── Persona tests ──────────────────────────────────────────────────────────

class TestPersonas(unittest.TestCase):
    def test_eight_personas_loaded(self):
        assert len(USER_PERSONAS) == 8

    def test_all_personas_have_review_history(self):
        for pid, p in USER_PERSONAS.items():
            assert "review_history" in p, f"{pid} missing review_history"

    def test_cold_start_persona_no_history(self):
        # Simulate cold-start — empty history
        cold = {**USER_PERSONAS["persona_001"], "review_history": []}
        assert cold["review_history"] == []
