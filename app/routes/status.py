from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/status/{request_id}")
async def get_status(request_id: str, db: Session = Depends(get_db)):
    """Fetch processing status and image URLs for a given request."""
    
    # Check if request exists
    request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not request:
        return {"error": "Invalid request ID"}

    # Get images related to this request
    images = db.query(models.Image).filter(models.Image.request_id == request_id).all()

    # Format response
    response = {
        "request_id": request_id,
        "status": request.status,
        "images": [
            {
                "input_url": img.input_url,
                "output_url": img.output_url,
                "status": img.status,
            }
            for img in images
        ],
    }

    return response
