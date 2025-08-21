
# PDF to XML Converter

A simple tool to convert PDF files to XML format using FastAPI (backend) and Streamlit (frontend).

## Features
- Upload PDF files
- Extract text and data from PDFs
- Convert extracted data to XML
- Download and preview XML output

## Technologies Used
- **Backend:** FastAPI (Python)
- **Frontend:** Streamlit (Python)
- **PDF Processing:** PyMuPDF, pdfplumber, camelot, pandas, Pillow, pytesseract

## Requirements
- Python 3.8+
- Required Python packages (see `requirements.txt`)
- Tesseract OCR (for image extraction, optional)

## Installation
1. Clone the repository:
	```
	git clone https://github.com/karan4533/pdf-to-xml-converter.git
	```
2. Install Python dependencies:
	```
	pip install -r backend/requirements.txt
	pip install streamlit requests
	```
3. (Optional) Install Tesseract OCR for image extraction:
	- Download from https://github.com/tesseract-ocr/tesseract/wiki
	- Add Tesseract to your system PATH

## Usage
### Start Backend (FastAPI)
```
cd backend
uvicorn app.main:app --reload
```

### Start Frontend (Streamlit)
```
cd frontend
streamlit run app.py
```

### Workflow
1. Upload a PDF file in the Streamlit app
2. The backend processes the PDF and generates XML
3. Download or preview the XML output

## Notes
- If Tesseract is not installed, image extraction will be skipped.
- For local use, ensure both backend and frontend are running.

## License
MIT
