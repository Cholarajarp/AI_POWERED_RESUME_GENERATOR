import io
from typing import Tuple

def extract_text_from_pdf_bytes(b: bytes) -> str:
    # placeholder: in production integrate pdfminer or similar
    return b.decode(errors='ignore')[:2000] 
