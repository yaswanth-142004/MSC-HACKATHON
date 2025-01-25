from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ocr import initialize_client, perform_ocr
from agent import call
import tempfile
import os
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ocr")
async def process_ocr(file: UploadFile = File(...)):
    try:
        logging.debug(f"Received file: {file.filename}")
        client = initialize_client()
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        with open(temp_file_path, "rb") as f:
            image_content = f.read()
            text = perform_ocr(client, image_content)
        
        os.unlink(temp_file_path)
        logging.debug(f"OCR Result: {text}")
        return {"text": text}
    except Exception as e:
        logging.error(f"OCR Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate")
async def evaluate_answer(data: dict):
    try:
        response = call(
            data["question"], 
            data["correct_answer"], 
            data["student_answer"]
        )
        return {"result": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))