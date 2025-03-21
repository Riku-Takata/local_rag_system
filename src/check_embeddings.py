# エンベディングモデルのインポートパスを確認するスクリプト
import importlib
import inspect
import sys

def check_embeddings_modules():
    """エンベディングモジュールの検査"""
    print("=== エンベディングモジュール検査 ===")
    
    # 可能性のあるモジュールパス
    module_paths = [
        "llama_index.core.embeddings",
        "llama_index.embeddings",
        "llama_index.core.embeddings.huggingface",
        "llama_index.embeddings.huggingface"
    ]
    
    for path in module_paths:
        try:
            module = importlib.import_module(path)
            print(f"✓ '{path}' を正常にインポートできました")
            
            # モジュール内のクラスを探索
            if path in ["llama_index.core.embeddings", "llama_index.embeddings"]:
                print(f"  クラス一覧:")
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and obj.__module__ == path:
                        print(f"  - {name}")
            
        except ImportError as e:
            print(f"✗ '{path}' をインポートできませんでした: {e}")
    
    # 'local'エンベディングが使用可能か確認
    try:
        from llama_index.core import Settings
        original_embed_model = Settings.embed_model
        print(f"\n現在のデフォルトエンベディングモデル: {original_embed_model}")
        
        # localエンベディングを試す
        print("\n'local'エンベディングを試行中...")
        Settings.embed_model = "local"
        print(f"設定後のエンベディングモデル: {Settings.embed_model}")
        
        # 元に戻す
        Settings.embed_model = original_embed_model
        
    except Exception as e:
        print(f"Settingsのテスト中にエラーが発生しました: {e}")
    
    # 追加のパッケージ確認
    try:
        import pkg_resources
        packages = [
            "llama-index",
            "llama-index-core",
            "llama-index-embeddings-huggingface",
            "sentence-transformers"
        ]
        
        print("\n=== 関連パッケージの確認 ===")
        for pkg in packages:
            try:
                dist = pkg_resources.get_distribution(pkg)
                print(f"✓ {pkg} がインストールされています (バージョン: {dist.version})")
            except pkg_resources.DistributionNotFound:
                print(f"✗ {pkg} がインストールされていません")
        
    except ImportError:
        print("パッケージ確認中にエラーが発生しました")
    
if __name__ == "__main__":
    check_embeddings_modules()