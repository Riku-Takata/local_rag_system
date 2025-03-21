from dotenv import load_dotenv
import os

load_dotenv()

PDF_DIR = os.getenv('PDF_DIR')
INDEX_DIR = os.getenv('INDEX_DIR')
EMBED_MODEL_NAME = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
LLM_MODEL = 'mistral:7b'