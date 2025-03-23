from llama_index.llms import Ollama
from config import OLLAMA_BASE_URL, LLM_MODEL

def get_ollama_llm(temperature=0.1):
    """
    Docker環境内でOllamaに接続するためのLLMオブジェクトを返す
    デフォルトでconfig.pyで設定したホスト名とポートを使用
    """
    return Ollama(
        model=LLM_MODEL,
        temperature=temperature,
        base_url=OLLAMA_BASE_URL
    )