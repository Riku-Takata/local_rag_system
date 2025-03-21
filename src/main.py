from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from utils.data_loader import load_documents
from utils.metadata_handler import add_folder_metadata
from config import INDEX_DIR, EMBED_MODEL_NAME
import os

def main():
    # フォルダの確認と作成
    if not os.path.exists(INDEX_DIR):
        os.makedirs(INDEX_DIR, exist_ok=True)
        print(f"インデックスディレクトリを作成しました: {INDEX_DIR}")

    # ドキュメントの読み込み
    print("ドキュメントを読み込んでいます...")
    documents = load_documents()
    if not documents:
        print("警告: ドキュメントが読み込めませんでした。PDF_DIRの設定を確認してください。")
        return

    # メタデータの追加
    print("メタデータを追加しています...")
    documents = add_folder_metadata(documents)

    # エンベディングモデルの設定
    print(f"エンベディングモデルを初期化しています: {EMBED_MODEL_NAME}")
    embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)

    # インデックスの作成（エンベディングモデルを明示的に指定）
    print("インデックスを作成しています...")
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model
    )

    # インデックスの保存
    print(f"インデックスを保存しています: {INDEX_DIR}")
    index.storage_context.persist(persist_dir=INDEX_DIR)
    print("インデックスの作成が完了しました！")
    print(f"次のコマンドで対話型RAGシステムを起動できます: python src/interactive_rag.py")

if __name__ == "__main__":
    main()