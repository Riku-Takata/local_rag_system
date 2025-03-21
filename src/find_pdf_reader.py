# LlamaIndexのSimpleDirectoryReaderの引数を検査するスクリプト
import inspect
import importlib
import sys

def check_simple_directory_reader():
    """SimpleDirectoryReaderの引数を調査"""
    print("=== SimpleDirectoryReader検査 ===")
    
    # パッケージをロード
    try:
        from llama_index.core.readers import SimpleDirectoryReader
        print("✓ llama_index.core.readers から SimpleDirectoryReader をインポートできました")
        
        # 引数の調査
        print("\n引数情報:")
        sig = inspect.signature(SimpleDirectoryReader.__init__)
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            print(f"- {param_name}: {param.default if param.default is not inspect.Parameter.empty else '(必須)'}")
        
        # ソースコードの場所
        print(f"\nソースコード: {inspect.getsourcefile(SimpleDirectoryReader)}")
        
    except ImportError:
        print("✗ llama_index.core.readers から SimpleDirectoryReader をインポートできませんでした")
        
        # 代替の場所を試す
        try:
            from llama_index.readers import SimpleDirectoryReader
            print("✓ llama_index.readers から SimpleDirectoryReader をインポートできました")
            
            # 引数の調査
            print("\n引数情報:")
            sig = inspect.signature(SimpleDirectoryReader.__init__)
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue
                print(f"- {param_name}: {param.default if param.default is not inspect.Parameter.empty else '(必須)'}")
            
            # ソースコードの場所
            print(f"\nソースコード: {inspect.getsourcefile(SimpleDirectoryReader)}")
            
        except ImportError:
            print("✗ llama_index.readers からもSimpleDirectoryReader をインポートできませんでした")
    
    print("\n=== LlamaIndexのバージョン情報 ===")
    try:
        llama_index = importlib.import_module('llama_index')
        print(f"llama_index バージョン: {llama_index.__version__ if hasattr(llama_index, '__version__') else '不明'}")
    except ImportError:
        print("llama_index パッケージがインストールされていません")
    
    try:
        llama_index_core = importlib.import_module('llama_index.core')
        print(f"llama_index.core バージョン: {llama_index_core.__version__ if hasattr(llama_index_core, '__version__') else '不明'}")
    except (ImportError, AttributeError):
        print("llama_index.core が見つからないか、バージョン情報がありません")
    
    print("\n=== Pythonパス ===")
    for path in sys.path:
        print(path)
    
if __name__ == "__main__":
    check_simple_directory_reader()