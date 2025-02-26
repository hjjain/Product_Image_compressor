from pydantic import BaseModel
from typing import List, Optional

class ImageSchema(BaseModel):
    product_name: str
    input_url: str
    output_url: Optional[str] = None
    status: str

class RequestSchema(BaseModel):
    id: int
    status: str
    images: List[ImageSchema]
    
    class Config:
        orm_mode = True
