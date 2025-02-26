import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Request(Base):
    __tablename__ = "requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # ✅ Use UUID
    status = Column(String, default="pending")

    images = relationship("Image", back_populates="request")

class Image(Base):
    __tablename__ = "images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # ✅ Use UUID
    request_id = Column(UUID(as_uuid=True), ForeignKey("requests.id"))  # ✅ Foreign key as UUID
    product_name = Column(String)
    input_url = Column(String)
    output_url = Column(String, nullable=True)
    status = Column(String, default="pending")

    request = relationship("Request", back_populates="images")
