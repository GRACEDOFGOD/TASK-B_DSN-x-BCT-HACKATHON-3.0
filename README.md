# DSN × BCT Hackathon 3.0 — Task B: Recommendation Agent

A FastAPI recommendation agent that delivers personalised, context-aware suggestions from user personas. It supports cold-start scenarios, cross-domain recommendations, conversational refinement, and Nigerian cultural tone.

## Key Features

- Personalized recommendations across food, products, books, and entertainment
- Cold-start support with no prior review history
- Cross-domain suggestions that connect interests naturally
- Multi-turn conversational refinement via follow-up requests
- Browser UI available at `/`
- JSON API for integration and experimentation

## Technology Stack

- Python 3.12 (recommended)
- FastAPI
- Uvicorn
- Pydantic v2
- Groq LLM integration via `groq`
- Docker + Docker Compose

## Setup

### 1. Prepare the repository

```bash
git clone https://github.com/GRACEDOFGOD/TASK-B_DSN-x-BCT-HACKATHON-3.0.git
cd TASK-B_DSN-x-BCT-HACKATHON-3.0
cp .env.example .env
```

### 2. Configure environment variables

Edit `.env` with your Groq API key:

```env
GROQ_API_KEY=your_real_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
DEFAULT_NUM_RECS=10
MAX_NUM_RECS=20
```

### 3. Install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Start the application

```bash
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Open in your browser:

```text
http://127.0.0.1:8000/
```

## Docker Option

```bash
docker-compose up --build
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/v1/personas` | List preset personas |
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

The application pipeline:

1. Build a persona profile from user input
2. Score candidate items across domain, price, tags, popularity, and rating
3. Use the LLM to select and explain the top recommendations
4. Support follow-up refinement via additional requests

## Troubleshooting

- If `/` returns `500 Internal Server Error`, verify `.env` exists and `static/index.html` is read with UTF-8 encoding.
- If `uvicorn` is missing, run `pip install -r requirements.txt`.
- If `pydantic-core` fails on Windows, use Python 3.12 or install Visual Studio Build Tools.
- If the API returns no persona data, call `/api/v1/personas` to verify the service.

## Notes

- Frontend UI is served from `static/index.html`.
- Backend entrypoint is `app/main.py`.
- Router definitions are in `app/routers/`.
- This repository is prepared for hackathon demonstration and evaluation.
