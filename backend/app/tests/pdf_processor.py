import fitz  # PyMuPDF
import pdfplumber
import camelot
import pandas as pd
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\karanm\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
import io
import base64
from typing import Dict, List, Any

class PDFProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Main processing function that extracts all data from PDF"""
        
        extracted_data = {
            'metadata': {},
            'text_content': [],
            'tables': [],
            'images': [],
            'page_count': 0
        }
        
        try:
            # Extract metadata and basic info
            extracted_data['metadata'] = self._extract_metadata(pdf_path)
            
            # Extract text content
            extracted_data['text_content'] = self._extract_text(pdf_path)
            
            # Extract tables
            extracted_data['tables'] = self._extract_tables(pdf_path)
            
            # Extract images and OCR
            extracted_data['images'] = self._extract_images(pdf_path)
            
            # Get page count
            with fitz.open(pdf_path) as doc:
                extracted_data['page_count'] = len(doc)
            
            return extracted_data
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
    
    def _extract_metadata(self, pdf_path: str) -> Dict[str, Any]:
        """Extract PDF metadata"""
        with fitz.open(pdf_path) as doc:
            metadata = doc.metadata
            return {
                'title': metadata.get('title', ''),
                'author': metadata.get('author', ''),
                'subject': metadata.get('subject', ''),
                'creator': metadata.get('creator', ''),
                'producer': metadata.get('producer', ''),
                'creation_date': metadata.get('creationDate', ''),
                'modification_date': metadata.get('modDate', '')
            }
    
    def _extract_text(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract text content from each page"""
        text_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_content.append({
                        'page': page_num,
                        'text': page_text.strip(),
                        'char_count': len(page_text),
                        'word_count': len(page_text.split())
                    })
        
        return text_content
    
    def _extract_tables(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract tables using Camelot"""
        tables_data = []
        
        try:
            # Try to extract tables with Camelot
            tables = camelot.read_pdf(pdf_path, pages='all')
            
            for i, table in enumerate(tables):
                table_dict = {
                    'table_id': i + 1,
                    'page': table.page,
                    'accuracy': table.accuracy,
                    'data': table.df.to_dict('records'),
                    'headers': table.df.columns.tolist(),
                    'rows': len(table.df),
                    'columns': len(table.df.columns)
                }
                tables_data.append(table_dict)
        
        except Exception as e:
            print(f"Table extraction error: {e}")
            # Fallback to pdfplumber for table extraction
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages, 1):
                        tables = page.extract_tables()
                        for i, table in enumerate(tables):
                            if table:
                                df = pd.DataFrame(table[1:], columns=table[0])
                                table_dict = {
                                    'table_id': len(tables_data) + 1,
                                    'page': page_num,
                                    'accuracy': 0.8,  # Default accuracy
                                    'data': df.to_dict('records'),
                                    'headers': df.columns.tolist(),
                                    'rows': len(df),
                                    'columns': len(df.columns)
                                }
                                tables_data.append(table_dict)
            except Exception as e2:
                print(f"Fallback table extraction error: {e2}")
        
        return tables_data
    
    def _extract_images(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract images and perform OCR"""
        images_data = []
        
        with fitz.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    try:
                        # Get image data
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        
                        if pix.n < 5:  # GRAY or RGB
                            # Convert to PIL Image
                            img_data = pix.tobytes("png")
                            pil_image = Image.open(io.BytesIO(img_data))
                            
                            # Perform OCR
                            ocr_text = pytesseract.image_to_string(pil_image)
                            
                            # Convert image to base64 for embedding
                            buffered = io.BytesIO()
                            pil_image.save(buffered, format="PNG")
                            img_base64 = base64.b64encode(buffered.getvalue()).decode()
                            
                            image_info = {
                                'image_id': f"img_{page_num + 1}_{img_index + 1}",
                                'page': page_num + 1,
                                'width': pix.width,
                                'height': pix.height,
                                'ocr_text': ocr_text.strip(),
                                'base64_data': img_base64,
                                'format': 'PNG'
                            }
                            images_data.append(image_info)
                        
                        pix = None  # Free memory
                        
                    except Exception as e:
                        print(f"Image extraction error: {e}")
                        continue
        
        return images_data