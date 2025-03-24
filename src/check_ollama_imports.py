# check_ollama_imports.py
import sys
import importlib
import pkg_resources

print("=== Python パッケージの診断 ===")

print("\n1. llama-indexの関連パッケージ:")
dists = [d for d in pkg_resources.working_set]
for dist in dists:
    if 'llama' in dist.key:
        print(f"  • {dist.key} (version: {dist.version})")

print("\n2. インポートパスの確認:")
modules_to_check = [
    "llama_index",
    "llama_index.llms",
    "llama_index.llms.ollama",
    "llama_index_llms_ollama",
    "llama_index_llms_ollama.ollama"
]

for module_path in modules_to_check:
    try:
        module = importlib.import_module(module_path)
        print(f"  ✓ {module_path} をインポートできました")
        
        if module_path.endswith("ollama"):
            print(f"    内容: {[item for item in dir(module) if not item.startswith('_')]}")
    except ImportError as e:
        print(f"  ✗ {module_path} をインポートできませんでした: {e}")

print("\n3. Ollamaクラスの検索:")
import_statements = [
    "from llama_index.llms import Ollama",
    "from llama_index.llms.ollama import Ollama",
    "from llama_index_llms_ollama import Ollama",
    "from llama_index_llms_ollama.ollama import Ollama"
]

for statement in import_statements:
    try:
        exec(statement)
        print(f"  ✓ `{statement}` は成功しました")
    except ImportError as e:
        print(f"  ✗ `{statement}` は失敗しました: {e}")
    except Exception as e:
        print(f"  ! `{statement}` は別のエラーが発生しました: {e}")