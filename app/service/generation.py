import os
import uuid
import logging
from datetime import datetime
from io import BytesIO
from PIL import Image
from google import genai
from fastapi import HTTPException
from schema import image as image_schema
from core.config import settings

logger = logging.getLogger(__name__)

# Initialize clients
try:
    client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    logger.info("Gemini client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini client: {e}")
    client = None

try:
    imagen_client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    logger.info("Google Imagen client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Google Imagen client: {e}")
    imagen_client = None

static_dir = "static"
generated_dir = os.path.join(static_dir, "generated")
os.makedirs(static_dir, exist_ok=True)
os.makedirs(generated_dir, exist_ok=True)

def build_prompt_from_description(data: image_schema.ImageGenerationRequest) -> str:
    """Convert structured description into a detailed paragraph prompt for image generation"""
    desc = data.description
    
    # Base subject description
    prompt = f"A highly detailed portrait of a {desc.ethnicity} {desc.gender} in their {desc.age_range}. "
    
    # Face and head
    prompt += f"They have a {desc.face_shape} face shape with {desc.skin_tone} skin tone and a {desc.jaw_description} jaw. "
    prompt += f"Their hair is {desc.hair_length}, {desc.hair_style}, and {desc.hair_color}. "
    
    # Facial features
    prompt += f"They have {desc.eye_shape} {desc.eye_color} eyes, a {desc.nose_shape} nose, and a {desc.mouth_description} mouth. "
    
    # Body and physique
    prompt += f"They have a {desc.build} build and are {desc.height_description}. "
    
    # Distinctive features
    if desc.facial_hair:
        prompt += f"They have {desc.facial_hair}. "
    if desc.scars_marks:
        prompt += f"Distinctive marks include: {desc.scars_marks}. "
    if desc.glasses:
        prompt += "They are wearing glasses. "
    if desc.additional_features:
        prompt += f"Additional features: {desc.additional_features}. "
        
    # Context
    if data.additional_context:
        prompt += f"Context: {data.additional_context}. "
        
    # Style instructions at the end
    if data.style.lower() == "police sketch":
        prompt += "The image must be a professional forensic police composite sketch. Black and white pencil drawing style, front-facing, neutral expression, plain white background, hyper-detailed clear facial features."
    elif data.style.lower() == "realistic":
        prompt += "The image must be a photorealistic portrait. Studio lighting, highly detailed, 8k resolution, authentic skin texture, front-facing."
    else:
        prompt += f"Rendered in {data.style} style, high quality."
        
    return prompt

def organize_by_date(base_dir: str, filename: str) -> str:
    """Organize images by date folders (YYYY/MM/DD)"""
    today = datetime.now()
    year_dir = os.path.join(base_dir, str(today.year))
    month_dir = os.path.join(year_dir, f"{today.month:02d}")
    day_dir = os.path.join(month_dir, f"{today.day:02d}")
    
    os.makedirs(day_dir, exist_ok=True)
    
    return os.path.join(day_dir, filename)

def ensure_png_extension(filename: str) -> str:
    """Ensure the filename has .png extension"""
    if not filename.lower().endswith('.png'):
        if '.' in filename:
            base_name = filename.rsplit('.', 1)[0]
            return f"{base_name}.png"
        else:
            return f"{filename}.png"
    return filename

async def generate_portrait(request: image_schema.ImageGenerationRequest):
    # Select the appropriate client
    if request.model.lower() == "imagen":
        if imagen_client is None:
            raise HTTPException(status_code=500, detail="Google Imagen client not initialized. Please check API configuration.")
        selected_client = imagen_client
        model_name = "imagen-4.0-generate-001"
    else:  # default to gemini
        if client is None:
            raise HTTPException(status_code=500, detail="Gemini client not initialized. Please check API configuration.")
        selected_client = client
        model_name = "gemini-2.5-flash-image"
    
    try:
        # Build detailed prompt from structured input
        prompt = build_prompt_from_description(request)
        logger.info(f"Generating portrait with model: {request.model}, style: {request.style}")
        
        # Generate image based on selected model
        if request.model.lower() == "imagen":
            # Use Google Imagen API
            response = selected_client.models.generate_images(
                model=model_name,
                prompt=prompt,
                number_of_images=1,
                safety_filter_level="block_some",
                person_generation="allow_all"
            )
            
            # Extract image from Imagen response
            if not response or not hasattr(response, 'images') or not response.images:
                raise HTTPException(status_code=500, detail="No images generated by Imagen model")
            
            # Get the first generated image
            generated_image = response.images[0]
            
            # Imagen returns images differently - check for image data
            if hasattr(generated_image, '_image_bytes'):
                image_data = generated_image._image_bytes
            elif hasattr(generated_image, 'image'):
                image_data = generated_image.image
            else:
                raise HTTPException(status_code=500, detail="Could not extract image data from Imagen response")
            
            generated_text = None
            
        else:
            # Use Gemini Flash Image Preview
            response = selected_client.models.generate_content(
                model=model_name,
                contents=[prompt],
            )

            # Validate response
            if not hasattr(response, 'candidates') or not response.candidates:
                logger.error("No candidates in response")
                raise HTTPException(status_code=500, detail="No generation candidates returned from AI model")
            
            if not response.candidates[0].content:
                logger.error("No content in candidate")
                raise HTTPException(status_code=500, detail="No content in generation candidate")
            
            if not hasattr(response.candidates[0].content, 'parts') or not response.candidates[0].content.parts:
                logger.error("No parts in content")
                raise HTTPException(status_code=500, detail="No parts in generated content")

            # Extract image data
            image_data = None
            generated_text = None

            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text is not None:
                    generated_text = part.text
                elif hasattr(part, 'inline_data') and part.inline_data is not None:
                    image_data = part.inline_data.data
                elif hasattr(part, 'bytes') and part.bytes is not None:
                    image_data = part.bytes

        if not image_data:
            error_msg = "No image data generated by the model"
            if 'generated_text' in locals() and generated_text:
                error_msg += f". Model response: {generated_text[:200]}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

        # Generate filename
        if request.save_name:
            filename = ensure_png_extension(request.save_name)
        else:
            # Create descriptive filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"portrait_{request.model}_{request.description.gender}_{timestamp}_{uuid.uuid4().hex[:6]}.png"
        
        # Save with date organization
        final_path = organize_by_date(generated_dir, filename)
        
        # Process and save image
        try:
            image = Image.open(BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            image.save(final_path, format='PNG', optimize=True)
            logger.info(f"Image saved successfully to: {final_path}")

        except Exception as image_error:
            logger.error(f"Error processing image with PIL: {image_error}")
            # Fallback: save raw bytes
            with open(final_path, 'wb') as f:
                f.write(image_data)
            logger.info(f"Raw image data saved to: {final_path}")

        # Generate web-accessible URL
        relative_path = os.path.relpath(final_path, static_dir)
        image_url = f"/static/{relative_path.replace(os.sep, '/')}"

        return {
            "success": True,
            "message": "Portrait generated successfully",
            "model_used": request.model,
            "filename": filename,
            "filepath": final_path,
            "image_url": image_url,
            "style": request.style,
            "description_summary": {
                "gender": request.description.gender,
                "age_range": request.description.age_range,
                "ethnicity": request.description.ethnicity
            },
            "prompt_used": prompt if len(prompt) < 500 else prompt[:500] + "...",
            "model_response": generated_text if 'generated_text' in locals() else None
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating portrait: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating portrait: {str(e)}")
