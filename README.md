# Binflow QIL Chatbot (Local Rules)

FastAPI chatbot that simulates a **Binflow** mindset: patterns > randomness.
No external API keys required; you can swap in a real LLM later.

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
