from dotenv import load_dotenv
import os

load_dotenv()

PDF_DIR = os.getenv('PDF_DIR')
INDEX_DIR = os.getenv('INDEX_DIR')
EMBED_MODEL_NAME = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'

# Dockerの場合は環境変数からOllamaのホスト名を取得
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'localhost')
OLLAMA_PORT = os.getenv('OLLAMA_PORT', '11434')
LLM_MODEL = 'mistral:7b'

# Ollama APIのベースURLを構築
OLLAMA_BASE_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"