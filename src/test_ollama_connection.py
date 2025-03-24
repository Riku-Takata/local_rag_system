import requests
import time
import sys
import os

def test_ollama_connection():
    """Ollamaサーバーへの接続をテストする"""
    print("=== Ollama接続テスト ===")
    
    # 環境変数からOllamaのURLを取得（デフォルトはlocalhost）
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    
    # スキーム（http://）がない場合は追加
    if not ollama_host.startswith(('http://', 'https://')):
        ollama_host = f"http://{ollama_host}"
    
    # ポート番号がない場合は追加
    if not any(ollama_host.endswith(f":{port}") for port in ["11434"]) and ":" not in ollama_host.split("/")[-1]:
        ollama_host = f"{ollama_host}:11434"
        
    print(f"接続先: {ollama_host}")
    
    # モデル一覧の取得を試みる
    try:
        print("\n1. モデル一覧の取得:")
        start_time = time.time()
        response = requests.get(f"{ollama_host}/api/tags", timeout=10)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"  ✓ 成功 ({elapsed:.2f}秒)")
            print(f"  利用可能なモデル: {[m['name'] for m in models]}")
        else:
            print(f"  ✗ 失敗: ステータスコード {response.status_code}")
            print(f"  レスポンス: {response.text}")
    except requests.exceptions.Timeout:
        print("  ✗ タイムアウト: サーバーからの応答がありません")
    except requests.exceptions.ConnectionError:
        print("  ✗ 接続エラー: サーバーに接続できません")
    except Exception as e:
        print(f"  ✗ エラー: {e}")
    
    # シンプルな生成をテスト
    try:
        print("\n2. テキスト生成テスト:")
        model_name = "mistral:7b"
        print(f"  モデル: {model_name}")
        
        payload = {
            "model": model_name,
            "prompt": "こんにちは、簡単なテストです。",
            "stream": False
        }
        
        start_time = time.time()
        response = requests.post(f"{ollama_host}/api/generate", json=payload, timeout=30)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ 成功 ({elapsed:.2f}秒)")
            print(f"  応答: {result.get('response', '')[:100]}...")
        else:
            print(f"  ✗ 失敗: ステータスコード {response.status_code}")
            print(f"  レスポンス: {response.text}")
    except requests.exceptions.Timeout:
        print("  ✗ タイムアウト: 生成に時間がかかりすぎています")
    except Exception as e:
        print(f"  ✗ エラー: {e}")
    
    print("\n=== 接続テスト完了 ===")

if __name__ == "__main__":
    test_ollama_connection()