from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import json
import os
from dotenv import load_dotenv
from sqlalchemy import text

from .database import Base, engine
from .routers import auth, users, tests, analytics
from .celery_app import celery_app

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="RapidProbe Wafer Test API",
    description="A full-featured wafer testing automation platform",
    version="1.0.0"
)

# Configure CORS
allowed_origins = json.loads(os.getenv("CORS_ORIGINS", '["http://localhost:3000"]'))
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tests.router, prefix="/tests", tags=["tests"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    # Apply security globally
    openapi_schema["security"] = [{"bearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = True
    except Exception:
        db_status = False
    
    try:
        # Test Celery connection
        celery_status = bool(celery_app.control.ping())
    except Exception:
        celery_status = False
    
    return {
        "status": "healthy" if db_status and celery_status else "unhealthy",
        "celery": celery_status,
        "database": db_status
    }
