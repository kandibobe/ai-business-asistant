"""
Document AI integration for advanced document processing.

Google Cloud Document AI provides:
- Advanced OCR for scanned documents
- Structured data extraction (tables, forms, key-value pairs)
- Document classification
- Invoice/receipt processing
- Contract analysis

Setup:
1. Enable Document AI API in Google Cloud Console
2. Create a processor for your document type
3. Set GOOGLE_CLOUD_PROJECT and DOCUMENT_AI_PROCESSOR_ID in .env
4. Ensure service account has Document AI API access
"""
import os
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class ExtractedEntity:
    """Represents an extracted entity from a document."""
    type: str
    value: str
    confidence: float
    normalized_value: Optional[str] = None


@dataclass
class DocumentAIResult:
    """Result from Document AI processing."""
    text: str
    entities: List[ExtractedEntity]
    tables: List[Dict[str, Any]]
    form_fields: Dict[str, str]
    confidence: float
    document_type: Optional[str] = None


class DocumentAIProcessor:
    """
    Wrapper for Google Cloud Document AI API.

    Features:
    - Extract text with better OCR than PyMuPDF
    - Extract structured data (tables, forms, key-value pairs)
    - Classify document types
    - Process invoices, receipts, contracts
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        location: str = "us",
        processor_id: Optional[str] = None,
    ):
        """
        Initialize Document AI processor.

        Args:
            project_id: Google Cloud project ID (from env if not provided)
            location: Processor location (default: 'us')
            processor_id: Document AI processor ID (from env if not provided)
        """
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        self.location = location
        self.processor_id = processor_id or os.getenv('DOCUMENT_AI_PROCESSOR_ID')

        self.enabled = self._check_availability()

        if not self.enabled:
            logger.warning(
                "Document AI not configured. Set GOOGLE_CLOUD_PROJECT and "
                "DOCUMENT_AI_PROCESSOR_ID in .env to enable advanced document processing."
            )

    def _check_availability(self) -> bool:
        """Check if Document AI is properly configured."""
        if not self.project_id or not self.processor_id:
            return False

        try:
            from google.cloud import documentai_v1 as documentai
            return True
        except ImportError:
            logger.warning(
                "google-cloud-documentai not installed. "
                "Install it with: pip install google-cloud-documentai"
            )
            return False

    def process_document(
        self,
        file_path: str,
        mime_type: str = "application/pdf",
    ) -> DocumentAIResult:
        """
        Process document using Document AI.

        Args:
            file_path: Path to document file
            mime_type: MIME type of document

        Returns:
            DocumentAIResult with extracted information

        Raises:
            RuntimeError: If Document AI is not configured
            Exception: On processing errors
        """
        if not self.enabled:
            raise RuntimeError(
                "Document AI not configured. Cannot process document."
            )

        from google.cloud import documentai_v1 as documentai

        # Read file
        with open(file_path, "rb") as f:
            file_content = f.read()

        # Create Document AI client
        client = documentai.DocumentProcessorServiceClient()

        # Build processor name
        processor_name = client.processor_path(
            self.project_id, self.location, self.processor_id
        )

        # Create document
        raw_document = documentai.RawDocument(
            content=file_content,
            mime_type=mime_type,
        )

        # Process document
        request = documentai.ProcessRequest(
            name=processor_name,
            raw_document=raw_document,
        )

        logger.info(f"Processing document with Document AI: {file_path}")
        result = client.process_document(request=request)
        document = result.document

        # Extract entities
        entities = []
        if document.entities:
            for entity in document.entities:
                entities.append(ExtractedEntity(
                    type=entity.type_,
                    value=entity.mention_text,
                    confidence=entity.confidence,
                    normalized_value=entity.normalized_value.text if entity.normalized_value else None,
                ))

        # Extract tables
        tables = self._extract_tables(document)

        # Extract form fields
        form_fields = self._extract_form_fields(document)

        # Get overall confidence
        confidence = document.pages[0].layout.confidence if document.pages else 0.0

        logger.info(f"Document AI processing complete. Extracted {len(entities)} entities, {len(tables)} tables")

        return DocumentAIResult(
            text=document.text,
            entities=entities,
            tables=tables,
            form_fields=form_fields,
            confidence=confidence,
        )

    def _extract_tables(self, document) -> List[Dict[str, Any]]:
        """Extract tables from document."""
        tables = []

        for page in document.pages:
            if not page.tables:
                continue

            for table in page.tables:
                table_data = {
                    'headers': [],
                    'rows': [],
                }

                # Extract headers and rows
                for row_idx, row in enumerate(table.header_rows):
                    header_row = []
                    for cell in row.cells:
                        header_row.append(self._get_cell_text(cell, document.text))
                    table_data['headers'].append(header_row)

                for row in table.body_rows:
                    data_row = []
                    for cell in row.cells:
                        data_row.append(self._get_cell_text(cell, document.text))
                    table_data['rows'].append(data_row)

                tables.append(table_data)

        return tables

    def _extract_form_fields(self, document) -> Dict[str, str]:
        """Extract form fields (key-value pairs) from document."""
        form_fields = {}

        for page in document.pages:
            if not page.form_fields:
                continue

            for field in page.form_fields:
                field_name = self._get_text(field.field_name, document.text)
                field_value = self._get_text(field.field_value, document.text)

                if field_name and field_value:
                    form_fields[field_name] = field_value

        return form_fields

    def _get_text(self, layout, full_text: str) -> str:
        """Extract text from layout object."""
        if not layout or not layout.text_anchor:
            return ""

        text_segments = []
        for segment in layout.text_anchor.text_segments:
            start = int(segment.start_index) if segment.start_index else 0
            end = int(segment.end_index) if segment.end_index else len(full_text)
            text_segments.append(full_text[start:end])

        return "".join(text_segments).strip()

    def _get_cell_text(self, cell, full_text: str) -> str:
        """Extract text from table cell."""
        return self._get_text(cell.layout, full_text)

    def format_for_ai(self, result: DocumentAIResult) -> str:
        """
        Format Document AI result for AI consumption.

        Structures extracted data in a way that's optimal for LLM understanding.

        Args:
            result: DocumentAIResult to format

        Returns:
            Formatted text string
        """
        formatted = []

        # Add document type if available
        if result.document_type:
            formatted.append(f"Document Type: {result.document_type}\n")

        # Add main text
        formatted.append("=== DOCUMENT TEXT ===\n")
        formatted.append(result.text)
        formatted.append("\n")

        # Add extracted entities
        if result.entities:
            formatted.append("\n=== EXTRACTED ENTITIES ===")
            for entity in result.entities:
                formatted.append(f"\n{entity.type}: {entity.value} (confidence: {entity.confidence:.2%})")
                if entity.normalized_value:
                    formatted.append(f"  → Normalized: {entity.normalized_value}")

        # Add tables
        if result.tables:
            formatted.append("\n\n=== TABLES ===")
            for idx, table in enumerate(result.tables, 1):
                formatted.append(f"\nTable {idx}:")

                # Headers
                if table['headers']:
                    formatted.append("Headers: " + " | ".join(table['headers'][0]))

                # Rows (limit to first 10 for context)
                for row in table['rows'][:10]:
                    formatted.append(" | ".join(row))

                if len(table['rows']) > 10:
                    formatted.append(f"... ({len(table['rows']) - 10} more rows)")

        # Add form fields
        if result.form_fields:
            formatted.append("\n\n=== FORM FIELDS ===")
            for key, value in result.form_fields.items():
                formatted.append(f"\n{key}: {value}")

        return "\n".join(formatted)


# Global instance
document_ai_processor = DocumentAIProcessor()


# Convenience function
def process_with_document_ai(
    file_path: str,
    mime_type: str = "application/pdf"
) -> Tuple[str, DocumentAIResult]:
    """
    Process document with Document AI and return formatted text.

    Args:
        file_path: Path to document
        mime_type: MIME type

    Returns:
        Tuple of (formatted_text, DocumentAIResult)
    """
    result = document_ai_processor.process_document(file_path, mime_type)
    formatted = document_ai_processor.format_for_ai(result)
    return formatted, result


if __name__ == "__main__":
    # Test Document AI configuration
    print("Document AI Configuration Test")
    print("=" * 50)

    processor = DocumentAIProcessor()

    if processor.enabled:
        print("✅ Document AI is configured and ready")
        print(f"   Project: {processor.project_id}")
        print(f"   Location: {processor.location}")
        print(f"   Processor: {processor.processor_id}")
    else:
        print("❌ Document AI is NOT configured")
        print("\nTo enable Document AI:")
        print("1. Enable Document AI API in Google Cloud Console")
        print("2. Create a processor (invoice, receipt, or general)")
        print("3. Set environment variables:")
        print("   GOOGLE_CLOUD_PROJECT=your-project-id")
        print("   DOCUMENT_AI_PROCESSOR_ID=your-processor-id")
        print("4. Install: pip install google-cloud-documentai")
