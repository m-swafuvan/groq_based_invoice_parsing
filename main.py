from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import tempfile
import os
import fitz  # PyMuPDF for PDF text extraction
from src.services.groq_service import parse_invoice_with_groq, validate_invoice_json
from src.services.extraction_service import extract_text_from_pdf

app = FastAPI()

@app.post("/extract-invoice")
async def extract_invoice(file: UploadFile = File(...)):
    task_log = {}

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        return JSONResponse(status_code=400, content={"error": "Uploaded file is empty."})
    
    file_text = extract_text_from_pdf(file_bytes, task_log)
    print(f"Extracted text: {file_text[:10000]}...")

    if not file_text.strip():
        return JSONResponse(status_code=400, content={
            "error": "No text extracted from PDF.",
            "task_log": task_log
        })

    # Assuming these methods are defined elsewhere
    invoice_json = parse_invoice_with_groq(file_text, task_log)
    validated_invoice = validate_invoice_json(invoice_json, task_log)

    if not validated_invoice:
        return JSONResponse(status_code=400, content={
            "error": "Failed to extract invoice fields.",
            "task_log": task_log
        })

    return validated_invoice
