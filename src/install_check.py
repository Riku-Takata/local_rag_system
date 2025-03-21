# LlamaIndexのインストール状態を確認するスクリプト
import pkg_resources
import sys
import importlib

def check_package(package_name):
    """パッケージがインストールされているか確認する"""
    try:
        dist = pkg_resources.get_distribution(package_name)
        print(f"✓ {package_name} がインストールされています (バージョン: {dist.version})")
        return True
    except pkg_resources.DistributionNotFound:
        print(f"✗ {package_name} がインストールされていません")
        return False

def try_import(module_path):
    """モジュールのインポートを試みる"""
    try:
        module = importlib.import_module(module_path)
        print(f"✓ '{module_path}' を正常にインポートできました")
        return True
    except ImportError as e:
        print(f"✗ '{module_path}' をインポートできませんでした: {e}")
        return False

def main():
    print("=== LlamaIndex パッケージ確認 ===")
    
    # 基本パッケージの確認
    basic_packages = [
        "llama-index",
        "llama-index-core",
        "llama-index-llms-ollama",
        "llama-index-embeddings-huggingface",
        "llama-index-vector-stores-faiss",
        "sentence-transformers",
        "faiss-cpu",
        "pdfminer.six",
        "python-dotenv",
        "flask"
    ]
    
    for package in basic_packages:
        check_package(package)
    
    print("\n=== モジュールインポート確認 ===")
    
    # 主要なインポートパスを確認
    import_paths = [
        "llama_index",
        "llama_index.core",
        "llama_index.core.vector_stores",
        "llama_index.llms",
        "llama_index.embeddings"
    ]
    
    for path in import_paths:
        try_import(path)
    
    print("\n=== Python情報 ===")
    print(f"Python バージョン: {sys.version}")
    print(f"実行パス: {sys.executable}")

if __name__ == "__main__":
    main()