from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import shutil
import subprocess
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def performImageProcessing(inputPath, outputPath):
    # Replace the path below with the correct path to your compiled C++ executable
    cpp_executable_path = 'E:/Code/C++/imageSharpening-master/build/Debug/imageSharpening.exe'
    # Execute the C++ program with the uploaded image path and the output path
    subprocess.run([cpp_executable_path, inputPath, outputPath])
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Create a unique filename for the uploaded image
        temp_file_path = f"temp/{file.filename}"
        # Save the uploaded image to the temporary file
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
        # Define the output path for the sharpened image
        output_file_path = f"static/uploads/sharpened_{file.filename}"
        # Call the image processing function
        performImageProcessing(temp_file_path, output_file_path)
        # Return the sharpened image
        return FileResponse(output_file_path, media_type="image/png", headers={"Content-Disposition": f"inline; filename=sharpened_{file.filename}"})
    except Exception as e:
        return {"status": "error", "message": f"Error sharpening image. {str(e)}"}