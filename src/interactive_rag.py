from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.llms.ollama import Ollama
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import INDEX_DIR, LLM_MODEL, EMBED_MODEL_NAME
import os

def load_index():
    """インデックスをロードする関数"""
    if not os.path.exists(INDEX_DIR):
        print(f"エラー: インデックスディレクトリ '{INDEX_DIR}' が見つかりません。")
        print("先にmain.pyを実行してインデックスを作成してください。")
        return None
    
    try:
        # エンベディングモデルの設定（インデックスロード時にも必要）
        print(f"エンベディングモデルを初期化しています: {EMBED_MODEL_NAME}")
        embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
        
        # エンベディングモデルを指定してStorageContextを作成
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        
        # エンベディングモデルを指定してインデックスをロード
        index = load_index_from_storage(
            storage_context,
            embed_model=embed_model
        )
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
        # インデックスからretrieverを作成（LlamaIndex最新版での変更点）
        retriever = index.as_retriever(similarity_top_k=3)
        
        # LLMの設定
        llm = Ollama(model=LLM_MODEL)
        
        # チャットメモリの設定
        memory = ChatMemoryBuffer.from_defaults(token_limit=4096)
        
        # コンテキストチャットエンジンの設定
        chat_engine = ContextChatEngine.from_defaults(
            retriever=retriever,  # indexの代わりにretrieverを使用
            llm=llm,
            memory=memory,
            context_prompt=(
                "あなたは日本語で応答するアシスタントです。"
                "以下の情報源を参考にして、ユーザーの質問に答えてください。"
                "情報源に含まれない内容についてはわからないと正直に答えてください。"
                "回答には参照した情報源の箇所を引用してください。"
                "「この内容について教えてください」のような一般的な質問には、資料の概要を説明してください。"
            ),
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
            # クエリの実行
            response = chat_engine.chat(user_input)
            print(f"\nアシスタント: {response.response}")
            
            # 引用元の表示
            if hasattr(response, 'source_nodes') and response.source_nodes:
                print("\n参照情報:")
                for i, node in enumerate(response.source_nodes, 1):
                    if hasattr(node, 'metadata') and 'file_path' in node.metadata:
                        source = node.metadata['file_path']
                        print(f"  {i}. {os.path.basename(source)}")
                    else:
                        print(f"  {i}. 不明な情報源")
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()