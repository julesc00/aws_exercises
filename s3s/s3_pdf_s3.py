import io
import boto3
from PyPDF2 import PdfReader, PdfWriter


class S3Handler:
    """Handles S3 operations for a given bucket."""

    def __init__(self, bucket_name, region_name='us-east-1'):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', region_name=region_name)

    def list_pdf_objects(self):
        """List all PDF objects in the bucket."""
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        # Filter only PDF files based on the key ending with '.pdf'
        return [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].lower().endswith('.pdf')]

    def download_pdf(self, key):
        """Download a PDF from S3 and return it as a BytesIO object."""
        pdf_bytes = io.BytesIO()
        self.s3.download_fileobj(Bucket=self.bucket_name, Key=key, Fileobj=pdf_bytes)
        pdf_bytes.seek(0)
        return pdf_bytes

    def upload_pdf(self, file_obj, key):
        """Upload a BytesIO PDF file to S3."""
        file_obj.seek(0)
        self.s3.upload_fileobj(Fileobj=file_obj, Bucket=self.bucket_name, Key=key)
        print(f"Uploaded merged PDF to bucket '{self.bucket_name}' with key '{key}'.")


class PDFDocument:
    """Represents a PDF document and provides methods to extract pages."""

    def __init__(self, file_obj):
        self.reader = PdfReader(file_obj)

    def get_first_page(self):
        """Extract and return the first page of the PDF if it exists."""
        if self.reader.pages:
            return self.reader.pages[0]
        else:
            return None


class PDFMerger:
    """Merges individual PDF pages into a single PDF document."""

    def __init__(self):
        self.writer = PdfWriter()

    def add_page(self, page):
        """Add a page (from a PDFDocument) to the merger."""
        self.writer.add_page(page)

    def get_merged_pdf(self):
        """Return the merged PDF as a BytesIO object."""
        output = io.BytesIO()
        self.writer.write(output)
        output.seek(0)
        return output


class PDFFlow:
    """Orchestrates the entire process of downloading, processing, merging, and uploading PDFs."""

    def __init__(self, source_bucket, destination_bucket, region='us-east-1'):
        self.source_handler = S3Handler(source_bucket, region)
        self.destination_handler = S3Handler(destination_bucket, region)
        self.merger = PDFMerger()

    def process_pdfs(self):
        """Download all PDFs from the source bucket and add their first pages to the merger."""
        pdf_keys = self.source_handler.list_pdf_objects()
        if not pdf_keys:
            print("No PDF files found in the source bucket.")
            return

        for key in pdf_keys:
            print(f"Processing {key}...")
            pdf_bytes = self.source_handler.download_pdf(key)
            pdf_doc = PDFDocument(pdf_bytes)
            first_page = pdf_doc.get_first_page()
            if first_page:
                self.merger.add_page(first_page)
            else:
                print(f"Warning: No pages found in {key}")

    def upload_merged_pdf(self, destination_key):
        """Upload the merged PDF to the destination bucket."""
        merged_pdf = self.merger.get_merged_pdf()
        self.destination_handler.upload_pdf(merged_pdf, destination_key)


# --- Usage Example ---
if __name__ == "__main__":
    SOURCE_BUCKET = "your-source-bucket-name"
    DESTINATION_BUCKET = "your-destination-bucket-name"
    MERGED_PDF_KEY = "merged_first_pages.pdf"

    # Create the PDFFlow object
    pdf_flow = PDFFlow(SOURCE_BUCKET, DESTINATION_BUCKET, region='us-east-1')

    # Process PDFs to extract the first page from each
    pdf_flow.process_pdfs()

    # Upload the merged PDF to the destination bucket
    pdf_flow.upload_merged_pdf(MERGED_PDF_KEY)
