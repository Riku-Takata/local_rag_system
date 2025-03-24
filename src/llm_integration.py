from llama_index.llms.ollama import Ollama
import os

def get_ollama_llm(model_name="mistral:7b", temperature=0.1):
    """Ollamaベースのモデルを取得する関数"""
    try:
        # 環境変数からOllamaのホストを取得（デフォルトはlocalhost）
        ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        
        # スキーム（http://）がない場合は追加
        if not ollama_host.startswith(('http://', 'https://')):
            ollama_host = f"http://{ollama_host}"
        
        # ポート番号がない場合は追加
        if not any(ollama_host.endswith(f":{port}") for port in ["11434"]) and ":" not in ollama_host.split("/")[-1]:
            ollama_host = f"{ollama_host}:11434"
            
        print(f"Ollama接続先: {ollama_host}")
        
        # タイムアウト設定を大幅に増やしたOllamaインスタンスを返す
        return Ollama(
            model=model_name,
            temperature=temperature,
            base_url=ollama_host,
            request_timeout=600.0,  # タイムアウトを10分に延長
            context_window=4096,    # コンテキストウィンドウサイズを明示的に設定
            max_tokens=2048        # 最大生成トークン数を制限
        )
    except Exception as e:
        print(f"Ollamaモデルの初期化中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return None