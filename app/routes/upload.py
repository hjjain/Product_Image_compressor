from fastapi import APIRouter, UploadFile, File, Depends,Form
from sqlalchemy.orm import Session
import pandas as pd
import uuid

from app.database import get_db
from app import models
from app.tasks import process_image  # Import Celery task

router = APIRouter()
@router.post("/upload/")
async def upload_csv(file: UploadFile = File(...), webhook_url:str = Form(...), db: Session = Depends(get_db)):
    """Upload CSV file, validate format, and store data in the database."""
    try:
        df = pd.read_csv(file.file)
        required_columns = ["S. No.", "Product Name", "Input Image Urls"]
        if not all(col in df.columns for col in required_columns):
            return {"error": "Invalid CSV format. Missing required columns."}

        request_id = str(uuid.uuid4())
        new_request = models.Request(id=request_id, status="pending")
        db.add(new_request)
        db.commit()

        # print(f"✅ Webhook URL received in FastAPI: {webhook_url}")  # Debugging log
        print(f"🔥 Full Request Received: file={file.filename}, webhook_url={webhook_url}")



        for _, row in df.iterrows():
            product_name = row["Product Name"]
            input_urls = row["Input Image Urls"].split(",")

            for url in input_urls:
                image_entry = models.Image(
                    request_id=request_id,
                    product_name=product_name.strip(),
                    input_url=url.strip(),
                    status="pending",
                )
                db.add(image_entry)
                db.commit()

                # 🚀 Pass webhook URL to Celery
                process_image.delay(image_entry.id, url.strip(), webhook_url)  

        return {"request_id": request_id, "message": "File uploaded successfully","webhook_url": webhook_url}

    except Exception as e:
        return {"error": str(e)}
