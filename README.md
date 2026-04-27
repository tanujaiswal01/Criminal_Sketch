<<<<<<< HEAD
<<<<<<< HEAD
# Image Generation & Printing API

A modern, scalable FastAPI application for AI-powered image generation and mockup printing using Google's Gemini AI.

## Features

- 🎨 **AI Image Generation**: Generate images from text prompts using Gemini AI
- 👕 **Mockup Printing**: Apply generated designs to product mockups (shirts, bedsheets, cups, etc.)
- 🔄 **Design Updates**: Modify existing designs on mockups with natural language prompts
- 📁 **File Management**: Download and list generated images and outputs
- 🏗️ **Modern Architecture**: Clean, scalable FastAPI structure with separation of concerns
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 📝 **Comprehensive Logging**: Structured logging for monitoring and debugging
- 🔒 **Type Safety**: Full type hints with Pydantic models

## Project Structure

```
Image_project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application setup
│   ├── api/                    # API route handlers
│   │   ├── __init__.py
│   │   ├── image_generation.py # Image generation endpoints
│   │   ├── mockup_processing.py# Mockup processing endpoints
│   │   └── file_management.py  # File management endpoints
│   ├── core/                   # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py          # Application settings
│   │   └── logging.py         # Logging configuration
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   └── image.py           # Image-related models
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── gemini_service.py  # Gemini AI integration
│   │   └── image_service.py   # Image processing
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── file_utils.py      # File operations
│       └── image_utils.py     # Image processing utilities
├── static/                     # Static files and uploads
│   ├── uploads/
│   ├── generated_images/
│   └── output_images/
├── tests/                      # Test files
├── logs/                       # Application logs
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── run.py                     # Development server runner
└── README.md                  # This file
```

## Quick Start

### Prerequisites

- Python 3.11+
- Google AI API key (for Gemini)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd Image_project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\\Scripts\\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:8000`

### Using Docker

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   The API will be available at `http://localhost:8000`

## API Endpoints

### Image Generation
- `POST /api/v1/generate/image` - Generate image from text prompt
- `GET /api/v1/generate/test-gemini` - Test Gemini API connection

### Mockup Processing  
- `POST /api/v1/mockup/print` - Print design on mockup
- `POST /api/v1/mockup/update-design` - Update existing design

### File Management
- `GET /api/v1/files/download/{image_type}/{filename}` - Download images
- `GET /api/v1/files/list/{image_type}` - List images by type
- `GET /api/v1/files/list/all` - List all images

### System
- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger)
- `GET /redoc` - Alternative API documentation

## Usage Examples

### 1. Generate an Image

```bash
curl -X POST "http://localhost:8000/api/v1/generate/image" \\
     -H "Content-Type: multipart/form-data" \\
     -F "prompt=A beautiful sunset over mountains" \\
     -F "save_name=sunset_mountains"
```

### 2. Print Design on T-Shirt Mockup

```bash
curl -X POST "http://localhost:8000/api/v1/mockup/print" \\
     -H "Content-Type: multipart/form-data" \\
     -F "generated_image=@generated_design.png" \\
     -F "mockup_image=@tshirt_mockup.jpg" \\
     -F "category=shirt" \\
     -F "output_name=custom_tshirt"
```

### 3. Update Design on Mockup

```bash
curl -X POST "http://localhost:8000/api/v1/mockup/update-design" \\
     -H "Content-Type: multipart/form-data" \\
     -F "update_prompt=Make the text bigger and add a red border" \\
     -F "mockup_image=@existing_design.jpg" \\
     -F "category=shirt"
```

## Supported Product Categories

- `shirt` / `tshirt` - T-shirts and shirts
- `bedsheet` - Bed sheets and bedding
- `cup` / `mug` - Cups and mugs  
- `hoodie` - Hoodies and sweatshirts
- `pillow` - Pillows and cushions

## Configuration

Key configuration options in `.env`:

```env
# Application
APP_NAME=Image Generation & Printing API
DEBUG=False
HOST=127.0.0.1
PORT=8000

# Google AI
GOOGLE_API_KEY=your_api_key_here

# File Storage
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=static/uploads
GENERATED_IMAGES_DIR=static/generated_images
OUTPUT_IMAGES_DIR=static/output_images

# Logging
LOG_LEVEL=INFO
```

## Development

### Running Tests (when implemented)
```bash
pytest tests/
```

### Code Formatting
```bash
black app/
isort app/
```

### Linting
```bash
flake8 app/
```

## Deployment

### Production with Docker
```bash
docker-compose -f docker-compose.yml up -d
```

### Environment Variables for Production
- Set `DEBUG=False`
- Configure proper CORS origins
- Use a production ASGI server like Gunicorn
- Set up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team.
=======
# Major_Project01
this is our project.
>>>>>>> b71b2b694f6eb1b4444ef47c94c9b3edddbc9ab7
=======
# Criminal_Sketch
this is our project.
>>>>>>> 0d8ff8e3dd6eb7ca74e03d629c39d5add7b4913a
