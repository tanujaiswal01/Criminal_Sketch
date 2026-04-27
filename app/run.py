# run.py
import uvicorn
import os
import sys
from dotenv import load_dotenv

# Determine paths
app_dir = os.path.dirname(os.path.abspath(__file__))      # .../Image_project/app
project_root = os.path.dirname(app_dir)                    # .../Image_project

# Load environment variables from the project root .env
load_dotenv(os.path.join(project_root, ".env"))

# Change working directory to app/ so that relative imports work
os.chdir(app_dir)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",        # main.py file and app object
        host="127.0.0.1",  # localhost
        port=8001,         # port
        reload=True        # auto-reload on code changes
    )
