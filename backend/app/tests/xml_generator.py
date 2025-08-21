from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from typing import Dict, List, Any
import html

class XMLGenerator:
    def __init__(self):
        self.namespace = "http://example.com/pdf-xml"
    
    def generate_xml(self, extracted_data: Dict[str, Any]) -> str:
        """Generate XML from extracted PDF data"""
        
        # Create root element
        root = Element('document')
        root.set('xmlns', self.namespace)
        root.set('version', '1.0')
        
        # Add metadata section
        self._add_metadata(root, extracted_data.get('metadata', {}))
        
        # Add document info
        doc_info = SubElement(root, 'document_info')
        SubElement(doc_info, 'page_count').text = str(extracted_data.get('page_count', 0))
        SubElement(doc_info, 'total_tables').text = str(len(extracted_data.get('tables', [])))
        SubElement(doc_info, 'total_images').text = str(len(extracted_data.get('images', [])))
        
        # Add text content
        self._add_text_content(root, extracted_data.get('text_content', []))
        
        # Add tables
        self._add_tables(root, extracted_data.get('tables', []))
        
        # Add images
        self._add_images(root, extracted_data.get('images', []))
        
        # Convert to formatted XML string
        rough_string = tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
    
    def _add_metadata(self, root: Element, metadata: Dict[str, Any]):
        """Add metadata section to XML"""
        meta_element = SubElement(root, 'metadata')
        
        for key, value in metadata.items():
            if value:
                meta_item = SubElement(meta_element, key)
                meta_item.text = html.escape(str(value))
    
    def _add_text_content(self, root: Element, text_content: List[Dict[str, Any]]):
        """Add text content section to XML"""
        if not text_content:
            return
        
        text_section = SubElement(root, 'text_content')
        
        for page_data in text_content:
            page_element = SubElement(text_section, 'page')
            page_element.set('number', str(page_data.get('page', 0)))
            page_element.set('char_count', str(page_data.get('char_count', 0)))
            page_element.set('word_count', str(page_data.get('word_count', 0)))
            
            # Add text content in CDATA section to preserve formatting
            text_element = SubElement(page_element, 'text')
            text_element.text = page_data.get('text', '')
    
    def _add_tables(self, root: Element, tables: List[Dict[str, Any]]):
        """Add tables section to XML"""
        if not tables:
            return
        
        tables_section = SubElement(root, 'tables')
        
        for table_data in tables:
            table_element = SubElement(tables_section, 'table')
            table_element.set('id', str(table_data.get('table_id', 0)))
            table_element.set('page', str(table_data.get('page', 0)))
            table_element.set('accuracy', str(table_data.get('accuracy', 0)))
            table_element.set('rows', str(table_data.get('rows', 0)))
            table_element.set('columns', str(table_data.get('columns', 0)))
            
            # Add headers
            headers_element = SubElement(table_element, 'headers')
            for header in table_data.get('headers', []):
                header_element = SubElement(headers_element, 'header')
                header_element.text = html.escape(str(header))
            
            # Add table data
            data_element = SubElement(table_element, 'data')
            for row_index, row in enumerate(table_data.get('data', [])):
                row_element = SubElement(data_element, 'row')
                row_element.set('index', str(row_index))
                
                for column_name, cell_value in row.items():
                    cell_element = SubElement(row_element, 'cell')
                    cell_element.set('column', str(column_name))
                    cell_element.text = html.escape(str(cell_value) if cell_value is not None else '')
    
    def _add_images(self, root: Element, images: List[Dict[str, Any]]):
        """Add images section to XML"""
        if not images:
            return
        
        images_section = SubElement(root, 'images')
        
        for image_data in images:
            image_element = SubElement(images_section, 'image')
            image_element.set('id', str(image_data.get('image_id', '')))
            image_element.set('page', str(image_data.get('page', 0)))
            image_element.set('width', str(image_data.get('width', 0)))
            image_element.set('height', str(image_data.get('height', 0)))
            image_element.set('format', str(image_data.get('format', 'PNG')))
            
            # Add OCR text
            if image_data.get('ocr_text'):
                ocr_element = SubElement(image_element, 'ocr_text')
                ocr_element.text = html.escape(image_data['ocr_text'])
            
            # Add base64 image data
            if image_data.get('base64_data'):
                data_element = SubElement(image_element, 'image_data')
                data_element.set('encoding', 'base64')
                data_element.text = image_data['base64_data']