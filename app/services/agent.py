"""
Recommendation Agent — Core agentic pipeline
4-step workflow:
  Step 1: build_taste_profile()     — LLM analyses persona deeply
  Step 2: score_items_for_persona() — Multi-factor deterministic scoring
  Step 3: generate_recommendations()— LLM reasons & explains in Nigerian tone
  Step 4: handle_multiturn()        — Conversational refinement
"""

import json
import logging
from typing import List, Dict, Any, Optional

from groq import Groq

from app.core.config import settings
from app.data.catalog import ALL_ITEMS

logger = logging.getLogger(__name__)


def _get_client() -> Groq:
    """Lazy Groq client — initialised once per worker."""
    return Groq(api_key=settings.GROQ_API_KEY)


# ── STEP 1: Taste Profile ─────────────────────────────────────────────────────

def build_taste_profile(persona: Dict[str, Any]) -> Dict[str, Any]:
    """
    LLM analyses the persona and returns a structured taste profile.
    Goes beyond simple preference matching — captures psychology,
    personality type, and behavioural signals.
    """
    history_block = ""
    if persona.get("review_history"):
        history_block = "\nPAST INTERACTIONS:\n"
        for h in persona["review_history"]:
            history_block += f"  - {h['stars']}⭐ {h['product']} ({h['domain']})\n"

    prompt = f"""You are a user modeling agent building a taste profile for a Nigerian user.

Analyse this user deeply:

DEMOGRAPHICS:
- Name: {persona['name']}, Age: {persona['age']}
- Location: {persona['location']}
- Occupation: {persona['occupation']}
- Income: {persona['income_level']}
- Price sensitivity: {persona['price_sensitivity']}

BEHAVIOR & PSYCHOLOGY:
- Behavior: {persona['behavior_patterns']}
- Goals: {persona['goals']}
- Pain points: {persona['pain_points']}
- Motivations: {persona['motivations']}
- Values: {persona['values']}

STATED PREFERENCES: {', '.join(persona.get('preferences', []))}
{history_block}

Build a comprehensive taste profile. Reply ONLY in this JSON (no markdown, no preamble):
{{
  "top_domains": ["domain1", "domain2", "domain3"],
  "price_preference": "<budget|mid|premium|any>",
  "personality_type": "<explorer|loyalist|value_hunter|premium_seeker>",
  "key_interests": ["interest1", "interest2", "interest3", "interest4"],
  "avoid_tags": ["tag1", "tag2"],
  "discovery_openness": "<low|medium|high>",
  "social_influence": "<low|medium|high>",
  "profile_summary": "<2 sentence summary of this user>"
}}"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.MAX_TOKENS_PROFILE,
            temperature=settings.TEMPERATURE_PROFILE,
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)

    except Exception as e:
        logger.warning(f"Taste profile LLM parse error: {e} — using fallback")
        return {
            "top_domains": persona.get("preferences", ["food"])[:3],
            "price_preference": "mid",
            "personality_type": "value_hunter",
            "key_interests": persona.get("preferences", []),
            "avoid_tags": [],
            "discovery_openness": "medium",
            "social_influence": "medium",
            "profile_summary": (
                f"{persona['name']} is a {persona['occupation']} "
                f"from {persona['location']}."
            ),
        }


# ── STEP 2: Multi-factor Item Scoring ────────────────────────────────────────

def score_items_for_persona(
    persona: Dict[str, Any],
    taste_profile: Dict[str, Any],
    items: List[Dict[str, Any]],
    context: str = "",
    exclude_ids: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Deterministic multi-factor scoring for every catalog item.

    Score breakdown (100 pts max):
      Domain match       0–30
      Price match        0–20
      Tag overlap        0–25
      Popularity         0–15
      Rating quality     0–10
      Context boost      0–10
      Avoid-tag penalty  −25 per tag hit
    """
    exclude_ids = exclude_ids or []
    scored = []

    price_order = ["budget", "mid", "premium"]

    for item in items:
        if item["id"] in exclude_ids:
            continue

        score = 0.0
        item_tags = set(item.get("tags", []))

        # 1. Domain match (0–30)
        top_domains = taste_profile.get("top_domains", [])
        if item["domain"] in top_domains:
            rank = top_domains.index(item["domain"])
            score += max(30 - rank * 8, 6)

        # 2. Price match (0–20)
        price_pref = taste_profile.get("price_preference", "mid")
        item_price = item.get("price_range", "mid")
        if item_price == "free":
            score += 18
        elif item_price == price_pref:
            score += 20
        elif item_price in price_order and price_pref in price_order:
            diff = abs(price_order.index(item_price) - price_order.index(price_pref))
            score += max(0, 10 - diff * 5)

        # 3. Tag overlap with interests (0–25)
        interests = set(taste_profile.get("key_interests", []))
        overlap = len(interests & item_tags)
        score += min(overlap * 8, 25)

        # 4. Avoid-tag penalty (−25 per hit)
        avoid = set(taste_profile.get("avoid_tags", []))
        score -= len(avoid & item_tags) * 25

        # 5. Popularity (0–15)
        score += item.get("popularity", 0.5) * 15

        # 6. Rating quality (0–10)
        score += (item.get("avg_rating", 3.0) - 1) / 4 * 10

        # 7. Context keyword boost (0–10)
        if context:
            ctx_lower = context.lower()
            if any(tag in ctx_lower for tag in item_tags):
                score += 5
            if item["domain"].replace("_", " ") in ctx_lower:
                score += 5

        scored.append({**item, "score": round(score, 2)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


# ── STEP 3: LLM Recommendation Generation ────────────────────────────────────

def generate_recommendations(
    persona: Dict[str, Any],
    taste_profile: Dict[str, Any],
    scored_items: List[Dict[str, Any]],
    context: str = "",
    num_recs: int = 10,
    is_cold_start: bool = False,
) -> Dict[str, Any]:
    """
    LLM selects and explains the best recommendations from pre-scored
    candidates. Explanations are warm and Nigerian in tone.
    """
    top_candidates = scored_items[:15]
    candidates_text = "\n".join([
        f"{i+1}. {item['name']} ({item['domain']}/{item['category']}) "
        f"— Tags: {', '.join(item['tags'][:4])} "
        f"| Score: {item['score']} "
        f"| Rating: {item['avg_rating']}⭐ "
        f"| Price: {item['price_range']}"
        for i, item in enumerate(top_candidates)
    ])

    cold_note = (
        "\nNOTE: This is a COLD-START user — no review history. "
        "Use demographics and stated preferences only. "
        "Be slightly more conservative.\n"
        if is_cold_start else ""
    )

    prompt = f"""You are a Nigerian recommendation agent — like a knowledgeable friend who knows exactly what different kinds of Nigerians enjoy.

USER PROFILE:
- Name: {persona['name']}, {persona['age']}yrs, {persona['gender']}
- Location: {persona['location']}
- Occupation: {persona['occupation']}
- Goals: {persona['goals']}
- Pain points: {persona['pain_points']}
- Price sensitivity: {persona['price_sensitivity']}

TASTE PROFILE:
- Top domains: {', '.join(taste_profile.get('top_domains', []))}
- Personality: {taste_profile.get('personality_type')}
- Key interests: {', '.join(taste_profile.get('key_interests', []))}
- Profile: {taste_profile.get('profile_summary')}

USER CONTEXT/REQUEST: {context if context else 'General personalised recommendations'}
{cold_note}

CANDIDATE ITEMS (pre-scored by algorithmic engine):
{candidates_text}

Select the BEST {num_recs} items for this specific user.
For each, write a warm, direct explanation in Nigerian English tone — like a friend who knows them.
Reference their specific situation where relevant (their job, location, budget etc).

Reply ONLY in this JSON (no markdown, no preamble):
{{
  "recommendations": [
    {{
      "rank": 1,
      "item_name": "<exact name from candidates>",
      "domain": "<domain>",
      "category": "<category>",
      "why_fits": "<warm Nigerian-toned explanation, 1-2 sentences>",
      "confidence": "<high|medium|low>",
      "cross_domain_note": "<if crosses domains, explain the connection, else empty string>"
    }}
  ],
  "agent_reasoning": "<2-3 sentences on how the agent approached this user>",
  "domains_covered": ["domain1", "domain2"]
}}"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.MAX_TOKENS_RECOMMEND,
            temperature=settings.TEMPERATURE_RECOMMEND,
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)

    except Exception as e:
        logger.warning(f"Recommendation LLM parse error: {e} — using fallback")
        return {
            "recommendations": [
                {
                    "rank": i + 1,
                    "item_name": item["name"],
                    "domain": item["domain"],
                    "category": item["category"],
                    "why_fits": f"Matches your interests in {item['domain']}.",
                    "confidence": "medium",
                    "cross_domain_note": "",
                }
                for i, item in enumerate(top_candidates[:num_recs])
            ],
            "agent_reasoning": "Recommendations based on your preferences and behaviour profile.",
            "domains_covered": list(set(i["domain"] for i in top_candidates[:num_recs])),
        }


# ── STEP 4: Multi-turn Handler ────────────────────────────────────────────────

def handle_multiturn(
    persona: Dict[str, Any],
    conversation_history: List[Dict[str, str]],
    new_message: str,
    current_recommendations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Handles conversational refinement.
    Agent understands user intent and adjusts accordingly.
    """
    history_text = "\n".join([
        f"{turn['role'].upper()}: {turn['content']}"
        for turn in conversation_history[-4:]
    ])
    recs_text = "\n".join([
        f"{r['rank']}. {r['item_name']} ({r['domain']})"
        for r in current_recommendations[:5]
    ])

    prompt = f"""You are a Nigerian recommendation agent in a conversation with {persona['name']}.

CONVERSATION HISTORY:
{history_text}

RECOMMENDATIONS ALREADY SHOWN:
{recs_text}

USER SAYS: {new_message}

Respond naturally as a helpful Nigerian friend. If they want refinements, adjust.
Keep it warm, direct, and culturally aware.

Reply ONLY in this JSON (no markdown, no preamble):
{{
  "response": "<natural Nigerian-toned response>",
  "action": "<refine|explain|confirm|new_search>",
  "refined_context": "<new context to use if refining, else empty string>"
}}"""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.MAX_TOKENS_MULTITURN,
            temperature=settings.TEMPERATURE_MULTITURN,
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)

    except Exception as e:
        logger.warning(f"Multi-turn parse error: {e}")
        return {
            "response": "Oya, let me adjust those recommendations for you!",
            "action": "refine",
            "refined_context": new_message,
        }


# ── MASTER PIPELINE ───────────────────────────────────────────────────────────

def full_recommendation_pipeline(
    persona: Dict[str, Any],
    context: str = "",
    num_recs: int = 10,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    is_cold_start: bool = False,
) -> Dict[str, Any]:
    """
    Master pipeline — called by the API endpoint.

    INPUT:  User Persona dict + optional context string
    OUTPUT: Ranked recommendations + reasoning + taste profile

    Agentic workflow:
      1 → Build taste profile from persona
      2 → Score all catalog items deterministically
      3 → LLM reasons and explains top picks (Nigerian tone)
      4 → Handle multi-turn refinement if conversation exists
    """
    logger.info(f"Pipeline: {persona.get('name')} | cold={is_cold_start} | ctx='{context[:40]}'")

    # Step 1
    taste_profile = build_taste_profile(persona)
    logger.info(f"  Taste profile: {taste_profile.get('personality_type')} | {taste_profile.get('top_domains')}")

    # Step 2
    scored_items = score_items_for_persona(
        persona, taste_profile, ALL_ITEMS, context
    )
    logger.info(f"  Scored {len(scored_items)} items. Top: {scored_items[0]['name'] if scored_items else 'none'}")

    # Step 3
    result = generate_recommendations(
        persona, taste_profile, scored_items,
        context, num_recs, is_cold_start
    )

    # Step 4
    multiturn_response = None
    if conversation_history and len(conversation_history) > 1:
        last_user_msg = next(
            (t["content"] for t in reversed(conversation_history) if t["role"] == "user"),
            new_message if (new_message := context) else ""
        )
        multiturn_response = handle_multiturn(
            persona, conversation_history,
            last_user_msg,
            result.get("recommendations", []),
        )

    return {
        "recommendations": result.get("recommendations", []),
        "agent_reasoning": result.get("agent_reasoning", ""),
        "domains_covered": result.get("domains_covered", []),
        "taste_profile": taste_profile,
        "multiturn_response": multiturn_response,
        "is_cold_start": is_cold_start,
        "total_items_scored": len(scored_items),
        "persona_name": persona.get("name", "Unknown"),
    }
