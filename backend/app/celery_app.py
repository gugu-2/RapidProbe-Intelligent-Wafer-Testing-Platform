from celery import Celery
from celery.utils.log import get_task_logger
import os
from dotenv import load_dotenv

load_dotenv()

logger = get_task_logger(__name__)

celery_app = Celery(
    "rapidprobe",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(bind=True, name="run_wafer_test")
def run_wafer_test(self, wafer_id: int, instrument_type: str, test_params: dict):
    from app.hardware.scpi_driver import SCPIInstrument
    from app.hardware.rest_driver import RESTInstrument
    from app.database import SessionLocal
    from app.models import TestResult
    
    logger.info(f"Starting test for wafer {wafer_id}")
    try:
        # Initialize instrument
        if instrument_type == "SCPI":
            instr = SCPIInstrument(address=os.getenv("DEFAULT_SCPI_ADDRESS"))
        else:
            instr = RESTInstrument(base_url=os.getenv("DEFAULT_REST_API_URL"))
        
        # Run test
        results = instr.run_test(test_params)
        
        # Save results
        db = SessionLocal()
        try:
            for die in results["die_data"]:
                tr = TestResult(
                    wafer_id=wafer_id,
                    die_x=die["x"],
                    die_y=die["y"],
                    test_name=die["test"],
                    result_value=die["value"]
                )
                db.add(tr)
            db.commit()
        finally:
            db.close()
            
        return {"status": "completed", "wafer_id": wafer_id}
        
    except Exception as e:
        logger.error(f"Test failed for wafer {wafer_id}: {str(e)}")
        raise self.retry(exc=e, countdown=30, max_retries=3)
