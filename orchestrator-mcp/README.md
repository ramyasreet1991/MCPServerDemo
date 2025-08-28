# MCP Orchestrator

This project provides an MCP orchestrator that connects to vendor MCP servers and exposes wrapped tools with policy enforcement. It includes a FastAPI bridge and a minimal React front-end scaffold.

## Backend

Run the backend with:

```bash
cd backend
uvicorn orchestrator.bridge.api:app --reload
```

## Frontend

The frontend is a Vite + React TypeScript application. Start the development server with:

```bash
cd frontend
npm run dev
```

## Configuration

Vendor and policy configuration live under `backend/orchestrator/config`.

## Testing

```bash
cd backend
pytest
```
