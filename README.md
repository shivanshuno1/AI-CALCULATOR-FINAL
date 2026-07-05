# AI Calculator (iPad-style)

A hand-drawn math/graphics solver: draw an expression, equation, or diagram on
a canvas, send it to a Gemini-powered backend, and get the solved result
rendered back over your drawing.

This is the original `shivanshuno1/Ipady` project, reorganized from a single
flat folder into a standard **frontend/backend** split, with a few bugs fixed
along the way (see "What changed" below).

```
.
├── frontend/   React + TypeScript + Vite app (the drawing canvas UI)
└── backend/    FastAPI + Gemini service (analyzes the drawing)
```

## ⚠️ Security notice — rotate your Gemini API key

The original repo had a **live Gemini API key committed in `.env`** and
another hardcoded, machine-specific path to a second `.env` file in
`utils.py`. Both are public on GitHub right now, which means that key should
be treated as compromised.

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and
   **revoke/delete** that key immediately.
2. Generate a new key.
3. Put the new key only in `backend/.env` (see below) — never commit it.

This reorganized version uses a placeholder in `backend/.env.example` and
does not contain any real key.

## Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # then edit .env and paste your new GEMINI_API_KEY
python main.py
```

The API runs at `http://localhost:8900`, exposing `POST /calculate`.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The app runs at the Vite dev URL (usually `http://localhost:5173`) and talks
to the backend via `VITE_API_URL` in `frontend/.env.local` (defaults to
`http://localhost:8900`).

## What changed in the reorganization

- Split the single flat folder into `frontend/` (Vite/React) and `backend/`
  (FastAPI), each with their own config, dependencies, and `.gitignore`.
- Fixed `_init_.py` → `apps/calculator/__init__.py` (the original filename
  was missing its double underscores, so the package import silently
  wouldn't have worked as intended).
- Moved the orphaned root-level `index.tsx` (which was actually the `Home`
  screen component, referenced by `App.tsx` as `@/screens/Home` but never
  placed there) into `frontend/src/screens/Home.tsx`.
- Removed the hardcoded, machine-specific Windows path to a second `.env`
  file in `utils.py`; config now comes only from `backend/constants.py` /
  `backend/.env`.
- Removed a large block of commented-out, unused LLaVA/transformers code
  from `utils.py`.
- Dropped `analyse_img.py`, an unused, dummy grayscale-only
  `analyze_image()` that duplicated the name of (and was shadowed by) the
  real Gemini implementation in `utils.py` — keeping both would have been
  confusing dead code.
- `route.py` now imports its request schema from `schema.py` instead of
  redefining an identical `ImageData` model inline.
- Frontend now reads the backend URL from `VITE_API_URL` (via a shared
  `axiosInstance`) instead of a hardcoded `localhost:8900`, so it works
  outside local dev too.
- Removed a redundant duplicate `postcss.config.js` (kept `postcss.config.cjs`,
  which matches this project's ESM `package.json`).

## Notes

- The frontend still loads MathJax 2.7 from a CDN at runtime for rendering
  LaTeX — this matches the original behavior and wasn't changed.
- No test suite existed in the original project, so none was added.
