# LLMモジュールのインポートパスを確認するスクリプト
import importlib
import sys
import pkg_resources

def check_llm_modules():
    """LLMモジュールの検査"""
    print("=== LLMモジュール検査 ===")
    
    # 可能性のあるモジュールパス
    module_paths = [
        "llama_index.llms",
        "llama_index.core.llms",
        "llama_index.llms.ollama",
    ]
    
    for path in module_paths:
        try:
            module = importlib.import_module(path)
            print(f"✓ '{path}' を正常にインポートできました")
            
            # モジュール内のクラスを探索
            print(f"  クラス一覧:")
            for name, obj in vars(module).items():
                if isinstance(obj, type):
                    print(f"  - {name}")
            
        except ImportError as e:
            print(f"✗ '{path}' をインポートできませんでした: {e}")
    
    # 追加のパッケージ確認
    print("\n=== 関連パッケージの確認 ===")
    packages = [
        "llama-index",
        "llama-index-core",
        "llama-index-llms-ollama",
    ]
    
    for pkg in packages:
        try:
            dist = pkg_resources.get_distribution(pkg)
            print(f"✓ {pkg} がインストールされています (バージョン: {dist.version})")
        except pkg_resources.DistributionNotFound:
            print(f"✗ {pkg} がインストールされていません")
    
if __name__ == "__main__":
    check_llm_modules()