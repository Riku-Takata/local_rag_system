from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import INDEX_DIR, LLM_MODEL, EMBED_MODEL_NAME
import os
import time

# llm_integration.pyからOllamaモデル取得関数をインポート
from llm_integration import get_ollama_llm

def load_index():
    """インデックスをロードする関数"""
    start_time = time.time()
    
    if not os.path.exists(INDEX_DIR):
        print(f"エラー: インデックスディレクトリ '{INDEX_DIR}' が見つかりません。")
        print("先にmain.pyを実行してインデックスを作成してください。")
        return None
    
    try:
        # エンベディングモデルの設定（インデックスロード時にも必要）
        print(f"エンベディングモデルを初期化しています: {EMBED_MODEL_NAME}")
        embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
        
        # エンベディングモデルを指定してStorageContextを作成
        print("インデックスストレージをロードしています...")
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        
        # エンベディングモデルを指定してインデックスをロード
        print("インデックスをロードしています...")
        index = load_index_from_storage(
            storage_context,
            embed_model=embed_model
        )
        
        # インデックス情報の表示
        if hasattr(index, 'docstore'):
            nodes = list(index.docstore.docs.values())
            print(f"ロードされたノード数: {len(nodes)}")
            
            if nodes:
                # サンプルノードの内容確認
                sample_node = nodes[0]
                print(f"\nサンプルノード:")
                print(f"  ID: {sample_node.id_}")
                if hasattr(sample_node, 'text'):
                    print(f"  テキスト長: {len(sample_node.text)} 文字")
        
        end_time = time.time()
        print(f"インデックスロード時間: {end_time - start_time:.2f}秒")
        return index
    except Exception as e:
        print(f"インデックスのロード中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_chat_engine(index):
    """チャットエンジンを作成する関数"""
    if index is None:
        return None
    
    try:
        # インデックスからretrieverを作成
        print("Retrieverを作成しています...")
        retriever = index.as_retriever(similarity_top_k=2)  # 類似ドキュメント数を2に減らす
        
        # LLMの設定
        print("LLMを初期化しています...")
        llm = get_ollama_llm(model_name=LLM_MODEL)
        if llm is None:
            return None
        
        # チャットメモリの設定
        print("チャットメモリを設定しています...")
        memory = ChatMemoryBuffer.from_defaults(token_limit=2048)  # メモリサイズを縮小
        
        # システムプロンプトを短くして軽量化
        system_prompt = (
            "あなたは簡潔に日本語で応答するアシスタントです。"
            "情報源に基づいて短く答えてください。"
            "情報源にない内容についてはわからないとだけ答えてください。"
        )
        
        print("チャットエンジンを構築しています...")
        # コンテキストチャットエンジンの設定
        chat_engine = ContextChatEngine.from_defaults(
            retriever=retriever,
            llm=llm,
            memory=memory,
            context_prompt=system_prompt,
            verbose=True
        )
        
        return chat_engine
    except Exception as e:
        print(f"チャットエンジンの作成中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    # インデックスのロード
    print("インデックスをロードしています...")
    index = load_index()
    if index is None:
        return
    
    # チャットエンジンの作成
    print("チャットエンジンを準備しています...")
    chat_engine = create_chat_engine(index)
    if chat_engine is None:
        return
    
    print("\n=== RAGチャットシステム ===")
    print("質問を入力してください。終了するには 'exit' または 'quit' と入力してください。")
    
    while True:
        # ユーザー入力の受け取り
        user_input = input("\nあなた: ")
        
        # 終了コマンドのチェック
        if user_input.lower() in ["exit", "quit", "終了"]:
            print("チャットを終了します。")
            break
        
        # 空の入力をスキップ
        if not user_input.strip():
            continue
        
        try:
            # デバッグ情報
            print("クエリを処理しています...")
            
            # 1. 検索処理
            print("関連ドキュメントを検索中...")
            search_start_time = time.time()
            nodes = chat_engine._retriever.retrieve(user_input)
            search_end_time = time.time()
            print(f"検索時間: {search_end_time - search_start_time:.2f}秒")
            print(f"検索結果: {len(nodes)}件のドキュメントが見つかりました")
            
            # ノード情報の表示
            for i, node in enumerate(nodes):
                print(f"  ノード {i+1}:")
                if hasattr(node, 'metadata') and 'file_path' in node.metadata:
                    print(f"    ファイル: {os.path.basename(node.metadata['file_path'])}")
                if hasattr(node, 'score'):
                    print(f"    スコア: {node.score}")
                if hasattr(node, 'text'):
                    print(f"    テキスト長: {len(node.text)} 文字")
            
            # 2. 短いコンテキスト生成
            context_text = "\n\n".join([node.get_text()[:500] for node in nodes])
            print(f"生成されたコンテキスト（トークン数削減）: {len(context_text)}文字")
            
            # 3. LLM呼び出し
            print("LLMによる回答生成中...")
            llm_start_time = time.time()
            
            # チャットエンジンからの応答を取得
            response_obj = chat_engine.chat(user_input)
            
            llm_end_time = time.time()
            print(f"LLM応答時間: {llm_end_time - llm_start_time:.2f}秒")
            
            print(f"\nアシスタント: {response_obj.response}")
            
            # 引用元の表示
            if hasattr(response_obj, 'source_nodes') and response_obj.source_nodes:
                print("\n参照情報:")
                for i, node in enumerate(response_obj.source_nodes, 1):
                    if hasattr(node, 'metadata') and 'file_path' in node.metadata:
                        source = node.metadata['file_path']
                        print(f"  {i}. {os.path.basename(source)}")
                    else:
                        print(f"  {i}. 不明な情報源")
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()