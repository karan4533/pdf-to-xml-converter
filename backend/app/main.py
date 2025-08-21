from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from .pdf_processor import PDFProcessor
from .xml_generator import XMLGenerator

app = FastAPI(title="PDF to XML Converter", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
pdf_processor = PDFProcessor()
xml_generator = XMLGenerator()

@app.post("/convert-pdf-to-xml")
async def convert_pdf_to_xml(file: UploadFile = File(...)):
    """Main endpoint for PDF to XML conversion"""
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        # Process PDF
        extracted_data = pdf_processor.process_pdf(temp_file_path)
        
        # Generate XML
        xml_content = xml_generator.generate_xml(extracted_data)
        
        # Save XML file
        xml_filename = f"{file.filename.replace('.pdf', '')}.xml"
        xml_path = f"temp/{xml_filename}"
        
        os.makedirs("temp", exist_ok=True)
        with open(xml_path, 'w', encoding='utf-8') as xml_file:
            xml_file.write(xml_content)
        
        return JSONResponse({
            "status": "success",
            "message": "PDF converted successfully",
            "xml_file": xml_filename,
            "download_url": f"/download/{xml_filename}"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    finally:
        # Clean up temporary PDF file
        os.unlink(temp_file_path)

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Endpoint to download generated XML file"""
    file_path = f"temp/{filename}"
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/xml'
        )
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/preview/{filename}")
async def preview_xml(filename: str):
    """Endpoint to preview XML content"""
    file_path = f"temp/{filename}"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return JSONResponse({"xml_content": content})
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}