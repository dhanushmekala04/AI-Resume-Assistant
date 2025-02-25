from io import BytesIO
import pdfplumber
import docx

def handle_file_upload(uploaded_file) -> str:
    """
    Convert uploaded file to text. Handles PDF, DOCX, and TXT files.
    """
    if uploaded_file is None:
        raise ValueError("No file uploaded!")
    
    # Check if the uploaded_file is a file-like object
    if not hasattr(uploaded_file, 'read'):
        raise ValueError(f"Expected file-like object, but got: {type(uploaded_file)}")
    
    # Read file content as bytes
    content_bytes = uploaded_file.read()
    
    # Process based on file type
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(content_bytes)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(content_bytes)
    else:
        # Assume it's a text file
        try:
            return content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return content_bytes.decode("ISO-8859-1", errors="replace")

def extract_text_from_pdf(content_bytes: bytes) -> str:
    """
    Extract text from PDF using pdfplumber.
    """
    with pdfplumber.open(BytesIO(content_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(content_bytes: bytes) -> str:
    """
    Extract text from DOCX using python-docx.
    """
    doc = docx.Document(BytesIO(content_bytes))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()
