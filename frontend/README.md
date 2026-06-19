# E-numerak Monitoring — Frontend

Production-ready React (Vite) dashboard, connected to your FastAPI backend.

## Theme: "Vitals"

A monitoring tool is checking if something is alive — so the dashboard borrows
the language of a hospital vitals monitor. The signature piece is the **Live
Pulse** strip on the Dashboard: each service gets its own EKG-style lane built
from real check history (a spike on every successful check, a flatline +
red blip on failure). Colors are functional, not decorative: emerald = up,
coral = down, amber = degraded/warning, calm blue = interactive accents.
Headings use Space Grotesk, body text Inter, all data/timestamps/URLs use
JetBrains Mono — so numbers read like instrument readouts.

## Where this goes

Drop this `frontend/` folder into your existing project so it sits next to
`backend/`:

```
E-numerak-Monitoring-System/
├── backend/        (already done)
└── frontend/        (this folder)
```

## Setup

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open **http://localhost:5173** — your backend must already be running on
**http://127.0.0.1:8000** (`uvicorn app.main:app --reload`). CORS is already
open (`allow_origins=["*"]`) in your `main.py`, so no backend change needed.

If your backend runs on a different host/port, edit `VITE_API_BASE_URL` in
`.env.local`.

## File structure (as planned, plus a few necessary additions)

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard/
│   │   │   ├── StatusCard.jsx
│   │   │   ├── UptimeChart.jsx      # the "pulse strip" — signature piece
│   │   │   └── ResponseTime.jsx
│   │   ├── Monitors/
│   │   │   ├── MonitorList.jsx
│   │   │   ├── MonitorForm.jsx
│   │   │   └── MonitorCard.jsx
│   │   ├── Alerts/
│   │   │   ├── AlertHistory.jsx
│   │   │   └── AlertSettings.jsx    # default WhatsApp numbers (localStorage)
│   │   ├── Logs/
│   │   │   └── LogViewer.jsx
│   │   ├── Layout/                  # + added: Sidebar.jsx, Topbar.jsx
│   │   └── common/                  # + added: StatusPill, Modal, EmptyState
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── Monitors.jsx
│   │   ├── Alerts.jsx
│   │   ├── Logs.jsx                 # + added (was missing a route owner)
│   │   └── Settings.jsx
│   ├── utils/format.js              # + added: time/url formatting helpers
│   ├── services/api.js              # every backend route wired in
│   ├── App.jsx
│   └── main.jsx
```

**What I added beyond the original sketch, and why:**
- `Layout/Sidebar.jsx` + `Topbar.jsx` — the pages needed a shared nav shell;
  Sidebar collapses into a bottom tab bar on mobile.
- `common/StatusPill.jsx`, `Modal.jsx`, `EmptyState.jsx` — small shared pieces
  reused across Monitors/Alerts/Logs instead of duplicating markup.
- `pages/Logs.jsx` — `LogViewer.jsx` existed in the plan but had no page/route
  to live on.
- `utils/format.js` — relative time ("3m pehle") and truncation helpers.

Everything else matches the structure exactly as discussed.

## What's wired up

Every backend endpoint you built is connected: monitors CRUD + toggle, alerts
list + clear, logs list, dashboard stats. Dashboard and Alerts/Logs pages
poll the backend every 20 seconds (your scheduler checks every 60s, so this
stays fresh without hammering the API). Adding a monitor pre-fills WhatsApp
numbers from Settings → Default numbers, but you can override per monitor.

## Production build

Already verified — `npm run build` compiles clean. For deployment, serve the
`dist/` folder from any static host (or Nginx on your VPS), and point
`VITE_API_BASE_URL` at your live backend URL.
