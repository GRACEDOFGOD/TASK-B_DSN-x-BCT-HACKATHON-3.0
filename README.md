# DSN × BCT Hackathon 3.0 — Task B: Recommendation Agent

A FastAPI-based recommendation agent that generates personalised, context-aware suggestions from a user persona. This service supports cold-start users, cross-domain recommendations, conversational refinement, and Nigerian cultural tone.

## Key Features

- Personalized recommendations across food, products, books, and entertainment
- Cold-start support with no prior review history
- Cross-domain suggestions that combine interests naturally
- Multi-turn conversational refinement through follow-up requests
- Browser UI at `/`
- JSON API for integration and evaluation

## Technology Stack

- Python 3.12 (recommended)
- FastAPI
- Uvicorn
- Pydantic v2
- Groq LLM integration via `groq`
- Docker + Docker Compose for container deployment

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/dsn-bct-taskb.git
cd dsn-bct-taskb
cp .env.example .env
```

### 2. Configure environment variables

Open `.env` and set your Groq API key:

```env
GROQ_API_KEY=your_real_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
DEFAULT_NUM_RECS=10
MAX_NUM_RECS=20
```

### 3. Install dependencies

Use Python 3.12 for the best compatibility:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Start the application

```bash
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Open the app in your browser:

```text
http://127.0.0.1:8000/
```

## Docker Option

If Docker is installed, you can run the service in a container:

```bash
docker-compose up --build
```

Then visit:

```text
http://127.0.0.1:8000/
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/v1/personas` | List all preset personas |
| GET | `/api/v1/catalog` | Retrieve the item catalog |
| POST | `/api/v1/recommend` | Generate recommendations from a custom persona |
| POST | `/api/v1/recommend/preset/{id}` | Generate recommendations for a preset persona |
| GET | `/docs` | Swagger UI documentation |

## Example Requests

### Custom persona

```bash
curl -X POST http://127.0.0.1:8000/api/v1/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "persona": {
      "name": "Tunde Bakare",
      "age": 19,
      "gender": "Male",
      "location": "Lagos, Nigeria",
      "education": "Undergraduate Year 2",
      "occupation": "University Student",
      "behavior_patterns": "Budget-conscious, loves gaming.",
      "avg_rating_given": 3.9,
      "total_reviews": 112,
      "goals": "Cheap food, free entertainment, gaming",
      "needs": "Affordability, fun, speed",
      "pain_points": "Expensive prices, data finishing fast",
      "motivations": "Fun and value",
      "values": "Value for money",
      "income_level": "low",
      "price_sensitivity": "very_high",
      "rating_tendency": "extreme",
      "preferences": ["gaming", "music", "cheap food"],
      "review_history": []
    },
    "context": "Show me something fun for the weekend",
    "num_recs": 10
  }'
```

### Preset persona

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/recommend/preset/persona_005?context=show+me+budget+options&num_recs=10"
```

## Preset Personas

The application includes predefined personas for quick demos:

| ID | Name | Occupation | Location |
|---|---|---|---|
| persona_001 | Chukwuemeka Obi | Software Engineer | Lagos |
| persona_002 | Folake Adeyemi | Fashion Designer | Ibadan |
| persona_003 | Emeka Nwosu | Oil & Gas Worker | Port Harcourt |
| persona_004 | Adaeze Okonkwo | Medical Doctor | Abuja |
| persona_005 | Tunde Bakare | University Student | Lagos |
| persona_006 | Ngozi Eze | Registered Nurse | Enugu |
| persona_007 | Babatunde Ogunleye | Business Owner | Lagos |
| persona_008 | Amina Yusuf | Primary School Teacher | Kano |

## Architecture Overview

The app follows this pipeline:

1. Build a persona profile from user input
2. Score catalog items by domain, price, tags, popularity, and rating
3. Use the LLM to choose and explain top recommendations
4. Support multi-turn refinement via follow-up requests

## Troubleshooting

- If `/` returns `500 Internal Server Error`, verify `.env` exists and `static/index.html` is served using UTF-8.
- If `uvicorn` is missing, run `pip install -r requirements.txt`.
- If `pydantic-core` fails to build on Windows, use Python 3.12 or install Visual Studio Build Tools.
- If the API returns no persona data, verify the service by calling `/api/v1/personas`.

## Notes

- The frontend UI is served from `static/index.html`.
- The backend entrypoint is `app/main.py`.
- Router modules are located in `app/routers/`.
- This repository is built for hackathon demonstration and evaluation.


### Competition metrics (Task B scoring):
- **NDCG@10** — 30 pts
- **Cold-Start + Cross-Domain** — 25 pts
- **Contextual Relevance** — 20 pts
- **This Solution Paper** — 15 pts
- **Code Reproducibility** — 10 pts

---

## 🗂️ Project Structure

```
taskb_recommendation/
├── app/
│   ├── main.py              # FastAPI app + lifespan
│   ├── schemas.py           # Pydantic request/response models
│   ├── core/
│   │   └── config.py        # Settings from .env
│   ├── data/
│   │   ├── catalog.py       # 35+ items across 8 domains
│   │   └── personas.py      # 8 Nigerian user personas
│   ├── services/
│   │   ├── agent.py         # 4-step agentic pipeline
│   │   └── metrics.py       # NDCG, Hit Rate, Precision, Recall
│   └── routers/
│       ├── recommend.py     # All recommendation endpoints
│       └── health.py        # Health check
├── static/
│   └── index.html           # Full web UI (no build step)
├── tests/
│   └── test_agent.py        # Pytest test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

Tests cover:
- NDCG@10, Hit Rate, Precision, Recall (edge cases + normal cases)
- Multi-factor scoring correctness
- Catalog integrity (no duplicate IDs, valid ranges)
- All 8 personas loaded correctly

---

## 🔑 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ Yes | — | Your Groq API key |
| `MODEL_NAME` | No | `llama-3.3-70b-versatile` | Groq model |
| `DEFAULT_NUM_RECS` | No | `10` | Default recommendation count |

---

## 📦 Datasets Used

| Dataset | Source | Usage |
|---------|--------|-------|
| Yelp Review Full | HuggingFace `Yelp/yelp_review_full` | Food/services signals |
| Amazon Reviews 2023 | HuggingFace `McAuley-Lab/Amazon-Reviews-2023` | Product signals |
| Goodreads Reviews | HuggingFace `sentence-transformers/goodreads-reviews` | Book signals |

The item catalog and persona preference weights were derived from statistical analysis of these datasets in the companion Colab notebook (`TASK_B_DSN_x_BCT_HACKATHON_3_0.ipynb`).

---

## 🏆 Competition

**DSN × Bluechip Technologies Hackathon 3.0**  
Task B — Recommendation Agent  
Submission deadline: 24 May 2026  

---

*Built with ❤️ and jollof rice energy 🇳🇬*
