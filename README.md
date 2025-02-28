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


### **API DOCUMENTATION**

# 📌 API Documentation - FastAPI Image Processing System

## **1️⃣ Overview**
This API processes images asynchronously from a CSV file containing image URLs and sends a webhook notification when processing is completed.

## **2️⃣ Base URL**
```
http://127.0.0.1:8000
```

---

## **3️⃣ Endpoints**

### **🔹 1. Upload CSV File**
#### **Endpoint:**
```
POST /upload/
```
#### **Description:**
Uploads a CSV file containing image URLs to process asynchronously.

#### **Request Parameters:**
| Parameter     | Type  | Required | Description                  |
|--------------|-------|----------|------------------------------|
| `file`       | File  | ✅ Yes    | CSV file with image URLs     |
| `webhook_url` | String | ❌ No     | Webhook URL for notifications |

#### **Request Example (Form-Data in Postman):**
```
Key: file        Value: test.csv
Key: webhook_url Value: https://webhook.site/example
```

#### **Response:**
```json
{
  "request_id": "de7b859a-e72f-4a33-8121-6cefb3bf3ee5",
  "message": "File uploaded successfully"
}
```

---

### **🔹 2. Get Request Status**
#### **Endpoint:**
```
GET /status/{request_id}
```
#### **Description:**
Fetches the current status of an image processing request.

#### **Path Parameter:**
| Parameter    | Type  | Required | Description |
|-------------|-------|----------|-------------|
| `request_id` | UUID  | ✅ Yes    | Request ID received from `/upload/` |

#### **Response Example (Pending Status):**
```json
{
  "request_id": "de7b859a-e72f-4a33-8121-6cefb3bf3ee5",
  "status": "pending",
  "images": []
}
```

#### **Response Example (Completed Status):**
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

### **🔹 3. Webhook Notification (Triggered on Completion)**
#### **Endpoint:**
```
POST {webhook_url}
```
#### **Description:**
Once image processing is completed, a webhook notification is sent.

#### **Request Body:**
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

#### **Expected Webhook Response:**
```json
{
  "success": true,
  "message": "Webhook received successfully"
}
```





### **Component DIAGRAM**

![component_diagram drawio](https://github.com/user-attachments/assets/0fae3cf8-3508-4d53-9dbe-a4222cc41f8e)

### **SEQUENCE DIAGRAM**

![Sequence_diagram drawio](https://github.com/user-attachments/assets/ed475641-f4e9-4960-8cd2-72a9c614d856)


### **ER DIAGRAM**

![ER_diagram drawio](https://github.com/user-attachments/assets/3e8595de-044e-472e-8a0b-ce7507604b45)


