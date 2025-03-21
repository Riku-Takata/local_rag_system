from llama_index import SimpleDirectoryReader
from config import PDF_DIR

def load_documents():
    reader = SimpleDirectoryReader(PDF_DIR, recursive=True, file_extensions=['.pdf'])
    return reader.load_data()