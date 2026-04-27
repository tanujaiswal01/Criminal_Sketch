from pydantic import BaseModel, Field
from typing import Optional

class PhysicalDescription(BaseModel):
    gender: str = Field(..., description="Gender of the person")
    age_range: str = Field(..., description="Age range (e.g., 'late 30s')")
    ethnicity: str = Field(..., description="Ethnicity")
    face_shape: str = Field(..., description="Face shape (e.g., 'oval', 'round')")
    skin_tone: str = Field(..., description="Skin tone description")
    hair_color: str = Field(..., description="Hair color")
    hair_style: str = Field(..., description="Hair style description")
    hair_length: str = Field(..., description="Hair length")
    eye_color: str = Field(..., description="Eye color")
    eye_shape: str = Field(..., description="Eye shape description")
    nose_shape: str = Field(..., description="Nose shape description")
    mouth_description: str = Field(..., description="Mouth and lips description")
    jaw_description: str = Field(..., description="Jaw description")
    build: str = Field(..., description="Body build")
    height_description: str = Field(..., description="Height description")
    facial_hair: Optional[str] = Field(None, description="Facial hair description")
    scars_marks: Optional[str] = Field(None, description="Scars or distinctive marks")
    glasses: bool = Field(False, description="Whether person wears glasses")
    additional_features: Optional[str] = Field(None, description="Any additional distinctive features")

class ImageGenerationRequest(BaseModel):
    description: PhysicalDescription
    style: str = Field(default="police sketch", description="Style of the image (e.g., 'police sketch', 'portrait', 'realistic')")
    additional_context: Optional[str] = Field(None, description="Additional context about the person")
    save_name: Optional[str] = Field(None, description="Optional custom filename for the generated image")
    model: str = Field(default="gemini", description="Model to use: 'gemini' or 'imagen' (Google's Imagen model)")
