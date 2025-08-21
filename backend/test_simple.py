from fastapi import FastAPI

app = FastAPI(title="Simple Test")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/test")
def test_imports():
    try:
        import fitz
        fitz_status = "✅ PyMuPDF OK"
    except Exception as e:
        fitz_status = f"❌ PyMuPDF Error: {e}"
    
    try:
        import pdfplumber
        plumber_status = "✅ pdfplumber OK"
    except Exception as e:
        plumber_status = f"❌ pdfplumber Error: {e}"
    
    try:
        import camelot
        camelot_status = "✅ Camelot OK"
    except Exception as e:
        camelot_status = f"❌ Camelot Error: {e}"
    
    try:
        import pytesseract
        tesseract_status = "✅ pytesseract OK"
    except Exception as e:
        tesseract_status = f"❌ pytesseract Error: {e}"
    
    return {
        "PyMuPDF": fitz_status,
        "pdfplumber": plumber_status,
        "Camelot": camelot_status,
        "pytesseract": tesseract_status
    }

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)