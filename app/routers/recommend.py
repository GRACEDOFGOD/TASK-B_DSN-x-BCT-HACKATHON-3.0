"""
Recommendation API Router
All Task B endpoints.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from app.schemas import (
    RecommendRequest,
    RecommendResponse,
    PresetPersonaResponse,
)
from app.services.agent import full_recommendation_pipeline
from app.services.metrics import evaluate_recommendations, GROUND_TRUTH
from app.data.personas import USER_PERSONAS
from app.data.catalog import ALL_ITEMS, CATALOG_STATS

logger = logging.getLogger(__name__)
router = APIRouter()


# ── POST /recommend ───────────────────────────────────────────────────────────

@router.post("/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest):
    """
    **Main recommendation endpoint.**

    Takes a user persona and returns personalised, ranked recommendations.

    - Handles **cold-start** users (no review history)
    - Handles **cross-domain** recommendations automatically
    - Supports **multi-turn** via `conversation_history`
    - Explanations are warm and Nigerian in tone
    """
    try:
        persona_dict = request.persona.model_dump()

        # Convert nested ReviewHistoryItem to plain dicts
        persona_dict["review_history"] = [
            r.model_dump() if hasattr(r, "model_dump") else r
            for r in persona_dict.get("review_history", [])
        ]

        conv_history = None
        if request.conversation_history:
            conv_history = [
                {"role": t.role, "content": t.content}
                for t in request.conversation_history
            ]

        result = full_recommendation_pipeline(
            persona=persona_dict,
            context=request.context,
            num_recs=request.num_recs,
            conversation_history=conv_history,
            is_cold_start=request.is_cold_start,
        )

        return RecommendResponse(**result)

    except Exception as e:
        logger.error(f"Recommendation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ── POST /recommend/preset ────────────────────────────────────────────────────

@router.post("/recommend/preset/{persona_id}", response_model=RecommendResponse)
async def recommend_preset(
    persona_id: str,
    context: str = "",
    num_recs: int = Query(default=10, ge=1, le=20),
):
    """
    Recommend for one of the 8 pre-built Nigerian personas.

    `persona_id` options: persona_001 … persona_008
    """
    if persona_id not in USER_PERSONAS:
        raise HTTPException(
            status_code=404,
            detail=f"Persona '{persona_id}' not found. "
                   f"Valid: {list(USER_PERSONAS.keys())}",
        )

    persona = USER_PERSONAS[persona_id]

    try:
        result = full_recommendation_pipeline(
            persona=persona,
            context=context,
            num_recs=num_recs,
        )
        return RecommendResponse(**result)

    except Exception as e:
        logger.error(f"Preset recommendation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /personas ─────────────────────────────────────────────────────────────

@router.get("/personas", response_model=List[PresetPersonaResponse])
async def list_personas():
    """List all 8 pre-built Nigerian user personas."""
    return [
        PresetPersonaResponse(
            id=pid,
            name=p["name"],
            occupation=p["occupation"],
            location=p["location"],
            age=p["age"],
            income_level=p["income_level"],
            preferences=p.get("preferences", []),
            total_reviews=p.get("total_reviews", 0),
        )
        for pid, p in USER_PERSONAS.items()
    ]


# ── GET /catalog ──────────────────────────────────────────────────────────────

@router.get("/catalog")
async def get_catalog(domain: Optional[str] = None):
    """
    Return the full item catalog (optionally filtered by domain).

    Available domains: food, electronics, beauty, fashion, fintech,
    books, education, entertainment
    """
    items = ALL_ITEMS
    if domain:
        items = [i for i in items if i["domain"] == domain]
    return {
        "stats": CATALOG_STATS,
        "filter": domain,
        "count": len(items),
        "items": items,
    }


# ── GET /evaluate/{persona_id} ────────────────────────────────────────────────

@router.get("/evaluate/{persona_id}")
async def evaluate_persona(
    persona_id: str,
    k: int = Query(default=10, ge=1, le=20),
):
    """
    Run NDCG@K + Hit Rate evaluation for a preset persona.
    Uses the competition ground truth.
    """
    if persona_id not in USER_PERSONAS:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' not found.")

    persona = USER_PERSONAS[persona_id]
    ground_truth = GROUND_TRUTH.get(persona_id, [])

    if not ground_truth:
        raise HTTPException(
            status_code=422,
            detail=f"No ground truth defined for {persona_id}.",
        )

    result = full_recommendation_pipeline(persona=persona, num_recs=k)
    metrics = evaluate_recommendations(result["recommendations"], ground_truth, k)

    return {
        "persona": persona["name"],
        "persona_id": persona_id,
        "ground_truth": ground_truth,
        "recommended": [r["item_name"] for r in result["recommendations"]],
        "metrics": metrics,
        "taste_profile": result["taste_profile"],
    }
