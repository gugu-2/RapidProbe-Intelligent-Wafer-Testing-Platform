import asyncio
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..models import Wafer, TestResult
from ..celery_app import run_wafer_test
from ..routers.auth import get_current_user, get_current_admin
from ..schemas import TestResult, WaferTestConfig

router = APIRouter()

@router.post("/run")
async def start_test(
    config: WaferTestConfig,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Start a wafer test with the given configuration.
    
    Args:
        config: Test configuration including wafer ID and instrument settings
        current_user: The authenticated user making the request
        db: Database session
        
    Returns:
        Dict with task ID and status
    
    Raises:
        HTTPException: If wafer not found or user not authorized
    """
    # Verify wafer exists
    wafer = db.query(Wafer).get(config.wafer_id)
    if not wafer:
        raise HTTPException(status_code=404, detail="Wafer not found")
        
    # Start Celery task
    task = run_wafer_test.delay(
        wafer_id=config.wafer_id,
        instrument_type=config.instrument_type,
        test_params=config.test_params
    )
    
    return {
        "task_id": task.id,
        "status": "started",
        "wafer_id": config.wafer_id
    }

@router.get("/status/{task_id}")
async def get_test_status(
    task_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get the status of a running test task.
    """
    task = run_wafer_test.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }

@router.websocket("/ws/{wafer_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    wafer_id: int,
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time test monitoring
    """
    await websocket.accept()
    try:
        while True:
            # Get latest results
            results = (
                db.query(TestResult)
                .filter(TestResult.wafer_id == wafer_id)
                .order_by(TestResult.timestamp.desc())
                .limit(10)
                .all()
            )
            
            # Send updates
            await websocket.send_json({
                "wafer_id": wafer_id,
                "results": [
                    {
                        "die_x": r.die_x,
                        "die_y": r.die_y,
                        "test_name": r.test_name,
                        "result_value": r.result_value,
                        "timestamp": r.timestamp.isoformat()
                    }
                    for r in results
                ]
            })
            
            await asyncio.sleep(1)  # Update every second
            
    except WebSocketDisconnect:
        print(f"Client disconnected from wafer {wafer_id} monitoring")
