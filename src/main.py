from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from utils.data_loader import load_documents
from utils.metadata_handler import add_folder_metadata
from config import INDEX_DIR, EMBED_MODEL_NAME
import os
import time

def main():
    start_time = time.time()
    print("=== RAGシステム インデックス作成 ===")
    
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
    
    print(f"読み込んだドキュメント数: {len(documents)}")
    
    # サンプルドキュメントの内容確認
    sample_doc = documents[0]
    print(f"\nサンプルドキュメント:")
    print(f"  メタデータ: {sample_doc.metadata}")
    print(f"  テキスト長: {len(sample_doc.text)} 文字")
    print(f"  テキストサンプル: {sample_doc.text[:200]}...")

    # メタデータの追加
    print("\nメタデータを追加しています...")
    documents = add_folder_metadata(documents)

    # エンベディングモデルの設定
    print(f"エンベディングモデルを初期化しています: {EMBED_MODEL_NAME}")
    embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)

    # インデックスの作成（エンベディングモデルを明示的に指定）
    print("インデックスを作成しています...")
    index_start_time = time.time()
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model
    )
    index_end_time = time.time()
    print(f"インデックス作成時間: {index_end_time - index_start_time:.2f}秒")

    # インデックスの保存
    print(f"インデックスを保存しています: {INDEX_DIR}")
    save_start_time = time.time()
    index.storage_context.persist(persist_dir=INDEX_DIR)
    save_end_time = time.time()
    print(f"インデックス保存時間: {save_end_time - save_start_time:.2f}秒")
    
    # インデックス情報の表示
    print("\nインデックス情報:")
    if hasattr(index, 'docstore'):
        nodes = list(index.docstore.docs.values())
        print(f"ノード数: {len(nodes)}")
    
    end_time = time.time()
    print("\nインデックスの作成が完了しました！")
    print(f"合計処理時間: {end_time - start_time:.2f}秒")
    print(f"次のコマンドで対話型RAGシステムを起動できます: python src/interactive_rag.py")

if __name__ == "__main__":
    main()