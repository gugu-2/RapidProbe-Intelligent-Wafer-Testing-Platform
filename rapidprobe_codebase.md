```
rapidprobe/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       └── 0001_create_tables.py
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── utils.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── tests.py
│   │   │   └── analytics.py
│   │   └── hardware/
│   │       ├── scpi_driver.py
│   │       └── rest_driver.py
│   └── .env.example
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── api.js
│       └── components/
│           ├── App.jsx
│           ├── Login.jsx
│           ├── Dashboard.jsx
│           └── WaferMap.jsx
├── docker-compose.yml
└── README.md
```  

---

### README.md
```markdown
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
```

---

### docker-compose.yml
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    env_file: ./backend/.env
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: rp_user
      POSTGRES_PASSWORD: rp_pass
      POSTGRES_DB: rapidprobe
    volumes:
      - pgdata:/var/lib/postgresql/data
  redis:
    image: redis:7
    ports:
      - "6379:6379"
volumes:
  pgdata:
```

---

## Backend Code

#### backend/Dockerfile
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### backend/requirements.txt
```
fastapi
uvicorn[standard]
SQLAlchemy
alembic
psycopg2-binary
python-dotenv
pydantic
pyvisa
requests
bcrypt
python-jose[cryptography]
celery[redis]
```

#### backend/.env.example
```
DATABASE_URL=postgresql://rp_user:rp_pass@postgres:5432/rapidprobe
JWT_SECRET=your_jwt_secret_here
REDIS_URL=redis://redis:6379/0
```

#### backend/app/database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### backend/app/models.py
```python
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Wafer(Base):
    __tablename__ = 'wafers'
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    test_results = relationship("TestResult", back_populates="wafer")

class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True, index=True)
    wafer_id = Column(Integer, ForeignKey('wafers.id'))
    die_x = Column(Integer)
    die_y = Column(Integer)
    test_name = Column(String)
    result_value = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    wafer = relationship("Wafer", back_populates="test_results")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_pw = Column(String)
    role = Column(String)
```

