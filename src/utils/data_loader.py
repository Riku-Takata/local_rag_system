from llama_index.core.readers import SimpleDirectoryReader
from config import PDF_DIR
import os

def load_documents():
    """PDFファイルを読み込む関数"""
    try:
        # 正しい引数を使用 (llama_index.core v0.12.25)
        reader = SimpleDirectoryReader(
            input_dir=PDF_DIR,
            recursive=True,
            required_exts=['.pdf']
        )
        documents = reader.load_data()
        if documents:
            print(f"PDFファイルを{len(documents)}件読み込みました")
        else:
            print("読み込まれたドキュメントはありません。PDF_DIRの設定を確認してください。")
        return documents
    except Exception as e:
        print(f"ドキュメントの読み込み中にエラーが発生しました: {e}")
        # PDFディレクトリの状態確認
        if not os.path.exists(PDF_DIR):
            print(f"指定されたPDF_DIR '{PDF_DIR}' が存在しません。")
        else:
            print(f"PDF_DIRの内容: {os.listdir(PDF_DIR) if os.path.isdir(PDF_DIR) else '(ディレクトリではありません)'}")
        return []