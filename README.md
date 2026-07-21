# Vera Merchant AI Assistant ("Vera")

[![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Deployment](https://img.shields.io/badge/deploy-Render-black.svg)](https://render.com/)

A production-ready, highly specific, modular AI assistant API for **magicpin** built to engage merchants and customers over WhatsApp. Rebuilt on a **4-Context Architecture** (Category, Merchant, Trigger, Customer), Vera composes verifiable, high-compulsion messages tailored to 5 business verticals: Dentists, Salons, Restaurants, Gyms, and Pharmacies.

---

## Table of Contents

1. [Architecture & Design](#architecture--design)
2. [Folder Structure](#folder-structure)
3. [Technology Stack](#technology-stack)
4. [Environment Variables](#environment-variables)
5. [Local Installation & Setup](#local-installation--setup)
6. [API Documentation & cURL Examples](#api-documentation--curl-examples)
   - [`GET /v1/healthz`](#1-get-v1healthz)
   - [`GET /v1/metadata`](#2-get-v1metadata)
   - [`POST /v1/context`](#3-post-v1context)
   - [`POST /v1/tick`](#4-post-v1tick)
   - [`POST /v1/reply`](#5-post-v1reply)
7. [Render Deployment Guide](#render-deployment-guide)
8. [Multi-Turn Intelligence](#multi-turn-intelligence)
9. [Running Tests](#running-tests)
10. [Troubleshooting](#troubleshooting)

---

## Architecture & Design

Vera is designed around the **4-Context Composition Framework**:

$$\text{message} = \text{compose}(\text{CategoryContext}, \text{MerchantContext}, \text{TriggerContext}, \text{CustomerContext}_?) $$

* **CategoryContext**: Slow-changing domain knowledge per vertical (clinical vocabulary, taboo rules, canonical service+price catalog, research digests).
* **MerchantContext**: Business performance, rating, view deltas, active catalog offers, and customer roster aggregates.
* **TriggerContext**: Specific event prompting outreach (research digests, seasonal dips, competitor openings, recall windows, IPL matches).
* **CustomerContext**: Optional patient/customer profile (visit history, preferred slot times, language preference) used for `send_as = merchant_on_behalf` sends.

---

## Folder Structure

```
.
├── app/
│   ├── api/                  # FastAPI router modules
│   │   ├── __init__.py
│   │   ├── health.py         # GET /v1/healthz
│   │   ├── metadata.py       # GET /v1/metadata
│   │   ├── context.py        # POST /v1/context
│   │   ├── tick.py           # POST /v1/tick
│   │   └── reply.py          # POST /v1/reply
│   ├── config/               # App settings & environment resolution
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── models/               # Pydantic domain dataclasses & API contract models
│   │   ├── __init__.py
│   │   ├── context_models.py
│   │   └── api_models.py
│   ├── services/             # Core business & composition services
│   │   ├── __init__.py
│   │   ├── context_service.py
│   │   ├── composer_service.py
│   │   ├── detector_service.py
│   │   └── reply_service.py
│   ├── storage/              # Thread-safe JSON file & in-memory persistence
│   │   ├── __init__.py
│   │   └── json_storage.py
│   ├── utils/                # Logging and string processing utilities
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── text_helpers.py
│   └── tests/                # Application unit test package
│       ├── __init__.py
│       ├── test_api.py
│       ├── test_composer.py
│       └── test_reply.py
├── data/                     # Automatic JSON persistence directory
├── dataset/                  # Seed dataset & expanded benchmark context
├── tests/                    # Top-level pytest suite
├── main.py                   # FastAPI application server entrypoint
├── bot.py                    # Standalone challenge composer entrypoint
├── submission.jsonl          # Evaluated test pairs benchmark file
├── requirements.txt          # Production Python dependencies
├── render.yaml               # Render cloud deployment blueprint
├── Procfile                  # Web process definition
├── README.md                 # Project documentation
└── .gitignore                # Source control exclusions
```

---

## Technology Stack

* **Language**: Python 3.12+ / 3.13
* **Web Framework**: FastAPI (Async ASGI)
* **Data Validation**: Pydantic v2 & Pydantic-Settings
* **Server**: Uvicorn (ASGI server with standard extensions)
* **Persistence**: Thread-safe JSON File & In-Memory Storage under `/data`
* **Testing**: Pytest & HTTPX TestClient

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `PORT` | `8080` | Network port for server binding (automatically set by Render) |
| `HOST` | `0.0.0.0` | Host IP binding address |
| `DATA_DIR` | `data` | Directory path for JSON persistence |
| `LOG_LEVEL` | `INFO` | Logging output level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `LLM_API_KEY` | `""` | Optional LLM API key for hybrid provider enrichment |

---

## Local Installation & Setup

### Prerequisites

* Python 3.12 or Python 3.13 installed
* Git

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/vera-merchant-ai.git
   cd vera-merchant-ai
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application server**:
   ```bash
   python main.py
   # Or directly via Uvicorn:
   uvicorn main:app --host 0.0.0.0 --port 8080
   ```

---

## API Documentation & cURL Examples

### 1. `GET /v1/healthz`

Liveness and health check endpoint polled by judging harnesses.

#### cURL Request
```bash
curl -X GET http://localhost:8080/v1/healthz
```

#### Expected Response (`200 OK`)
```json
{
  "status": "ok",
  "uptime_seconds": 142,
  "contexts_loaded": {
    "category": 5,
    "merchant": 50,
    "customer": 200,
    "trigger": 100
  }
}
```

---

### 2. `GET /v1/metadata`

Bot identity and framework information.

#### cURL Request
```bash
curl -X GET http://localhost:8080/v1/metadata
```

#### Expected Response (`200 OK`)
```json
{
  "team_name": "Senior Staff Vera AI",
  "team_members": ["Vera AI Engineering"],
  "model": "4-context-deterministic-modular-composer",
  "approach": "Deterministic 4-context modular engine with intent transition & auto-reply detection",
  "contact_email": "vera-ai@magicpin.in",
  "version": "1.0.0",
  "submitted_at": "2026-04-26T08:00:00Z"
}
```

---

### 3. `POST /v1/context`

Pushes or updates context objects. Idempotent by `(scope, context_id, version)`. Re-pushing an existing version returns `accepted: true`. Pushing a strictly lower version returns HTTP 409 Conflict.

#### cURL Request
```bash
curl -X POST http://localhost:8080/v1/context \
  -H "Content-Type: application/json" \
  -d '{
    "scope": "category",
    "context_id": "dentists",
    "version": 1,
    "delivered_at": "2026-04-26T10:00:00Z",
    "payload": {
      "slug": "dentists",
      "voice": { "tone": "peer_clinical" }
    }
  }'
```

#### Expected Response (`200 OK`)
```json
{
  "accepted": true,
  "ack_id": "ack_dentists_v1",
  "stored_at": "2026-07-21T21:48:00.123456Z"
}
```

#### Error Response (`409 Conflict` - Stale Version)
```json
{
  "accepted": false,
  "reason": "stale_version",
  "current_version": 2
}
```

---

### 4. `POST /v1/tick`

Periodic tick wake-up allowing the bot to initiate proactive outreach based on active triggers.

#### cURL Request
```bash
curl -X POST http://localhost:8080/v1/tick \
  -H "Content-Type: application/json" \
  -d '{
    "now": "2026-04-26T10:35:00Z",
    "available_triggers": ["trg_001_research_digest_dentists"]
  }'
```

#### Expected Response (`200 OK`)
```json
{
  "actions": [
    {
      "conversation_id": "conv_m_001_drmeera_dentist_delhi_trg_001_research_digest_dentists",
      "merchant_id": "m_001_drmeera_dentist_delhi",
      "customer_id": null,
      "send_as": "vera",
      "trigger_id": "trg_001_research_digest_dentists",
      "template_name": "vera_research_digest_v1",
      "template_params": [
        "Dr. Meera",
        "3-month fluoride recall cuts caries 38% better than 6-month",
        "JIDA Oct 2026, p.14"
      ],
      "body": "Dr. Meera, JIDA's Oct issue landed. One item relevant to your high-risk adult patients — 2,100-patient trial showed 3-month fluoride recall cuts caries recurrence 38% better than 6-month. Worth a look (2-min abstract). Want me to pull it + draft a patient-ed WhatsApp you can share?  — JIDA Oct 2026, p.14",
      "cta": "open_ended",
      "suppression_key": "research:dentists:2026-W17",
      "rationale": "Clinical-peer voice referencing JIDA research digest. Anchored on verifiable facts (2,100 patients, 38% reduction, JIDA Oct 2026, p.14) and Dr. Meera's high-risk patient cohort (124 patients)."
    }
  ]
}
```

---

### 5. `POST /v1/reply`

Receives simulated replies from merchants or customers and returns synchronous next actions.

#### cURL Request (Intent Transition)
```bash
curl -X POST http://localhost:8080/v1/reply \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_001",
    "merchant_id": "m_001_drmeera_dentist_delhi",
    "customer_id": null,
    "from_role": "merchant",
    "message": "Yes please send the abstract. Whats next?",
    "received_at": "2026-04-26T10:40:00Z",
    "turn_number": 2
  }'
```

#### Expected Response (`200 OK` - Send Action)
```json
{
  "action": "send",
  "body": "Done! Sending the abstract now (2-page PDF). I've also drafted your patient WhatsApp note below:\n\n\"3-month vs 6-month dental cleaning — new research shows 3-month fluoride recall cuts caries recurrence by 38%. Drop us a note for a quick check.\"\n\nReply CONFIRM to schedule this post for tomorrow 10am.",
  "cta": "binary_confirm_cancel",
  "rationale": "Merchant explicitly committed; switching immediately from qualification mode to action execution. Provided complete drafted artifact + binary confirmation CTA."
}
```

#### Expected Response (`200 OK` - Auto-Reply Wait Action)
```json
{
  "action": "wait",
  "wait_seconds": 14400,
  "rationale": "Detected automated business auto-reply. Backing off 4 hours for human owner to review."
}
```

#### Expected Response (`200 OK` - Hostile Opt-Out End Action)
```json
{
  "action": "end",
  "rationale": "Merchant explicitly requested to stop messages. Gracefully closing conversation."
}
```

---

## Render Deployment Guide

### Deployment via Blueprint (`render.yaml`)

1. Connect your repository to **Render Dashboard**.
2. Click **New +** -> **Blueprint**.
3. Select your repository containing `render.yaml`.
4. Render will automatically detect the web service configuration:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Apply**.

### Deployment Verification

Once deployed, verify public endpoint availability:
```bash
curl https://<your-render-app>.onrender.com/v1/healthz
curl https://<your-render-app>.onrender.com/v1/metadata
```

---

## Multi-Turn Intelligence

Vera includes built-in pattern detection rules in `DetectorService`:

1. **WhatsApp Business Auto-Reply Detection**:
   - Detects canned auto-replies ("Thank you for contacting us...") or repeated identical messages across consecutive turns.
   - Responds with `action: "wait"` (`wait_seconds: 14400`) on turns 1-2, and `action: "end"` on turn 3+.
2. **Immediate Intent Transition**:
   - When a merchant says "Yes", "OK let's do it", "Go ahead", or "Send abstract", Vera immediately transitions from qualification mode to action execution mode without asking additional qualifying questions.
3. **Graceful Opt-Out**:
   - Recognizes opt-out phrases ("Stop messaging", "Not interested", "Useless spam") and returns `action: "end"` gracefully.
4. **Out-of-Scope Query Handling**:
   - Identifies non-platform requests (e.g., GST or tax filing questions), politely declines out-of-scope tasks, and redirects to the core campaign thread.

---

## Running Tests

Run the full pytest suite locally:

```bash
python -m pytest
```

Output:
```
============================= test session starts =============================
platform win32 -- Python 3.13.2, pytest-9.1.1
collected 15 items

app\tests\test_api.py ..                                                 [ 13%]
app\tests\test_composer.py .                                             [ 20%]
app\tests\test_reply.py .                                                [ 26%]
tests\test_api.py ....                                                   [ 53%]
tests\test_composer.py ...                                               [ 73%]
tests\test_reply.py ....                                                 [100%]

======================== 15 passed in 0.85s ========================
```

---

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `HTTP 409 Conflict` on `/v1/context` | Pushing a version number strictly lower than currently stored version | Ensure incremental context pushes use `version >= current_version` |
| `HTTP 400 Bad Request` on `/v1/context` | Malformed JSON or invalid `scope` | Check payload against `ContextPushRequest` model requirements |
| `Errno 10048` address in use | Another process is using port 8080 | Change `PORT` env var or terminate conflicting process |
| `actions: []` returned from `/v1/tick` | Trigger ID not found or already suppressed | Push trigger context first via `/v1/context` before requesting tick |

---

## License

Internal proprietary submission for magicpin AI Challenge 2026.
