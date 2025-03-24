from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import INDEX_DIR, EMBED_MODEL_NAME
import os

def check_index():
    """インデックスの状態を診断する"""
    print("=== インデックス診断 ===")
    
    if not os.path.exists(INDEX_DIR):
        print(f"エラー: インデックスディレクトリ '{INDEX_DIR}' が見つかりません")
        return
    
    print(f"インデックスディレクトリ: {INDEX_DIR}")
    print(f"ディレクトリ内のファイル: {os.listdir(INDEX_DIR)}")
    
    try:
        print("\nエンベディングモデルを初期化しています...")
        embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
        
        print("\nインデックスをロードしています...")
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        index = load_index_from_storage(storage_context, embed_model=embed_model)
        
        # インデックスの基本情報
        print(f"\nインデックスタイプ: {type(index).__name__}")
        
        # ノード数の確認
        if hasattr(index, 'docstore'):
            nodes = list(index.docstore.docs.values())
            print(f"ノード数: {len(nodes)}")
            
            if nodes:
                # サンプルノードの内容確認
                sample_node = nodes[0]
                print(f"\nサンプルノード:")
                print(f"  ID: {sample_node.id_}")
                if hasattr(sample_node, 'text'):
                    print(f"  テキスト長: {len(sample_node.text)} 文字")
                    print(f"  テキストサンプル: {sample_node.text[:100]}...")
                
                # メタデータの確認
                if hasattr(sample_node, 'metadata') and sample_node.metadata:
                    print(f"  メタデータ: {sample_node.metadata}")
        
        # シンプルなクエリのテスト
        print("\nシンプルなクエリテスト:")
        retriever = index.as_retriever(similarity_top_k=2)
        nodes = retriever.retrieve("このプロジェクトについて教えてください")
        
        if nodes:
            print(f"  結果数: {len(nodes)}")
            for i, node in enumerate(nodes):
                print(f"  結果 {i+1}:")
                if hasattr(node, 'text'):
                    print(f"    テキスト: {node.text[:100]}...")
                if hasattr(node, 'score'):
                    print(f"    スコア: {node.score}")
                if hasattr(node, 'metadata') and node.metadata:
                    print(f"    メタデータ: {node.metadata}")
        else:
            print("  クエリ結果がありません")
            
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_index()