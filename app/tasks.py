import requests
from io import BytesIO
from PIL import Image
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.worker import celery

OUTPUT_DIR = "processed_images/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@celery.task
def process_image(image_id: int, input_url: str, webhook_url: str = None):
    """Downloads, compresses, and saves an image asynchronously."""
    db: Session = SessionLocal()

    try:
        print(f"🚀 Processing image ID {image_id} from URL: {input_url}")
        print(f"🔍 Webhook URL received in Celery: {webhook_url}")  # Debugging log

        # Download the image
        response = requests.get(input_url, stream=True)
        response.raise_for_status()

        # Open the image
        img = Image.open(BytesIO(response.content))

        # Compress image (reduce quality by 50%)
        output_path = os.path.join(OUTPUT_DIR, f"compressed_{image_id}.jpg")
        img.save(output_path, "JPEG", quality=50)

        print(f"✅ Image {image_id} compressed and saved to {output_path}")

        # Update database with output URL
        image = db.query(models.Image).filter(models.Image.id == image_id).first()
        if image:
            image.output_url = f"/{output_path}"  
            image.status = "completed"
            db.commit()

            # Check if all images for this request are completed
            request_images = db.query(models.Image).filter(models.Image.request_id == image.request_id).all()
            if all(img.status == "completed" for img in request_images):
                request = db.query(models.Request).filter(models.Request.id == image.request_id).first()
                if request:
                    request.status = "completed"
                    db.commit()
                    print(f"✅ Request {image.request_id} marked as completed.")

                    # 🚀 Webhook should be called here
                    if webhook_url:
                        print(f"🔗 Preparing to send webhook to: {webhook_url}")
                        
                        # Convert UUID to string before sending in JSON
                        payload = {
                            "request_id": str(image.request_id),  # ✅ Convert UUID to string
                            "status": "completed",
                            "images": [
                                {
                                    "input_url": img.input_url,
                                    "output_url": img.output_url,
                                    "status": img.status
                                }
                                for img in request_images
                            ],
                        }

                        try:
                            webhook_response = requests.post(webhook_url, json=payload, timeout=10)
                            print(f"✅ Webhook response: {webhook_response.status_code} - {webhook_response.text}")
                        except Exception as e:
                            print(f"❌ Webhook failed: {e}")

        return f"Image {image_id} processed successfully"

    except Exception as e:
        print(f"❌ Error processing image {image_id}: {e}")
        return f"Failed to process image {image_id}: {str(e)}"

    finally:
        db.close()
