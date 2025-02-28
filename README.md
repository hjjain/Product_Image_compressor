# 📦 FastAPI Image Processing with Celery & Webhooks

## 🚀 Overview
This project allows users to upload a CSV file containing image URLs. The images are processed asynchronously using **FastAPI, Celery, Redis, and PostgreSQL**. Once processing is completed, a webhook notification is sent.

## 🛠️ Tech Stack
- **Backend:** FastAPI
- **Task Queue:** Celery
- **Message Broker:** Redis
- **Database:** PostgreSQL
- **Image Processing:** Pillow (PIL)
- **Webhook Handling:** Requests

---

## 📌 Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/hjjain/Product_Image_compressor.git
cd Product_Image_compressor
```

### **2️⃣ Create and Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Start Services**
```bash
# Start PostgreSQL
sudo service postgresql start

# Start Redis
sudo service redis-server start
```

### **5️⃣ Run Database Migrations**
```bash
alembic upgrade head
```

### **6️⃣ Start FastAPI Server**
```bash
uvicorn app.main:app --reload
```

### **7️⃣ Start Celery Worker**
```bash
celery -A app.worker.celery worker --loglevel=info --pool=solo
```

---

## 📌 API Endpoints

### **1️⃣ Upload CSV File**
`POST /upload/`
- **Request Parameters:**
  - `file` (CSV File)
  - `webhook_url` (Optional)
- **Response:**
```json
{
  "request_id": "de7b859a-e72f-4a33-8121-6cefb3bf3ee5",
  "message": "File uploaded successfully"
}
```

### **2️⃣ Get Processing Status**
`GET /status/{request_id}`
- **Response Example:**
```json
{
  "request_id": "de7b859a-e72f-4a33-8121-6cefb3bf3ee5",
  "status": "completed",
  "images": [
    {
      "input_url": "https://picsum.photos/200/300",
      "output_url": "/processed_images/compressed_4224f8a2.jpg",
      "status": "completed"
    }
  ]
}
```

### **3️⃣ Webhook Notification**
`POST {webhook_url}`
- **Webhook Payload:**
```json
{
  "request_id": "de7b859a-e72f-4a33-8121-6cefb3bf3ee5",
  "status": "completed",
  "images": [
    {
      "input_url": "https://picsum.photos/200/300",
      "output_url": "/processed_images/compressed_4224f8a2.jpg",
      "status": "completed"
    }
  ]
}
```

---

## 📌 Postman Collection
You can import the Postman collection to test the APIs easily.

🔗 **Download Collection**: [postman_collection.json](./postman_collection.json)

### **Steps to Import in Postman**
1️⃣ Open **Postman**  
2️⃣ Click **Import** (Top Left)  
3️⃣ Select `postman_collection.json`  
4️⃣ Start testing the APIs 🚀  

---

## 📌 Error Handling
| Error Code | Description |
|-----------|-------------|
| 400 Bad Request | Invalid input (e.g., missing CSV file) |
| 404 Not Found | Request ID not found |
| 500 Internal Server Error | Server encountered an issue |



