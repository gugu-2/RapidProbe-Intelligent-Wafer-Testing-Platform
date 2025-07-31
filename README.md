# RapidProbe

RapidProbe is an intelligent, full-stack web platform for automating and optimizing wafer testing in chip manufacturing.

## Features
- Test orchestration (SCPI & REST instruments)
- Parallel execution via Celery
- Real-time monitoring with WebSockets
- Yield analytics and failure maps
- Role-based access control (Admin, Engineer, Viewer) 
- Containerized with Docker & Docker Compose

## Setup
1. Copy `.env.example` to `.env` and fill values
2. `docker-compose up --build`
3. Access UI at `http://localhost:3000`, API docs at `http://localhost:8000/docs`

## Tech Stack
- Backend: FastAPI, PostgreSQL, Celery
- Frontend: React, Vite
- Containerization: Docker
