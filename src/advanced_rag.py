from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.llms import Ollama
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.prompts import PromptTemplate
from config import INDEX_DIR, LLM_MODEL
import os
import argparse

# 高度なプロンプトテンプレート
SYSTEM_PROMPT = """あなたは日本語で応答する知識豊富なアシスタントです。
以下の情報源を参考にして、ユーザーの質問に正確に答えてください。

回答のルール:
1. 情報源に含まれる情報のみを使用してください
2. 情報源にない内容については「その情報は資料に含まれていません」と正直に答えてください
3. 回答の根拠となる情報源からの引用を明示してください
4. 「この内容について教えてください」のような一般的な質問には、資料の概要を説明してください
5. 回答は簡潔にまとめてください

これから提供するコンテキストを元に回答を構成してください:
{context_str}

"""

def load_index():
    """インデックスをロードする関数"""
    if not os.path.exists(INDEX_DIR):
        print(f"エラー: インデックスディレクトリ '{INDEX_DIR}' が見つかりません。")
        print("先にmain.pyを実行してインデックスを作成してください。")
        return None
    
    try:
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        index = load_index_from_storage(storage_context)
        return index
    except Exception as e:
        print(f"インデックスのロード中にエラーが発生しました: {e}")
        return None

def create_chat_engine(index, similarity_top_k=3, similarity_cutoff=0.7, verbose=False):
    """チャットエンジンを作成する関数"""
    if index is None:
        return None
    
    # LLMの設定
    from llm_integration import get_ollama_llm
    llm = get_ollama_llm(temperature=0.1)
    
    # チャットメモリの設定
    memory = ChatMemoryBuffer.from_defaults(token_limit=4096)
    
    # テキスト生成用のプロンプト
    text_qa_template = PromptTemplate(SYSTEM_PROMPT)
    
    # ポストプロセッサ - 類似度によるフィルタリング
    postprocessor = SimilarityPostprocessor(similarity_cutoff=similarity_cutoff)
    
    # コンテキストチャットエンジンの設定
    chat_engine = ContextChatEngine.from_defaults(
        index=index,
        llm=llm,
        memory=memory,
        system_prompt=text_qa_template,
        similarity_top_k=similarity_top_k,
        node_postprocessors=[postprocessor],
        verbose=verbose
    )
    
    return chat_engine

def format_sources(nodes):
    """ソース情報を整形する関数"""
    sources = []
    for i, node in enumerate(nodes, 1):
        if hasattr(node, 'metadata') and 'file_path' in node.metadata:
            source = node.metadata['file_path']
            folder = node.metadata.get('folder', '不明')
            score = getattr(node, 'score', '不明')
            
            # スコアが数値なら小数点以下3桁に丸める
            if isinstance(score, float):
                score = round(score, 3)
                
            source_info = f"{i}. {os.path.basename(source)} (フォルダ: {os.path.basename(folder)}, 類似度: {score})"
            sources.append(source_info)
        else:
            sources.append(f"{i}. 不明な情報源")
    return sources

def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='高度なRAGチャットシステム')
    parser.add_argument('--top-k', type=int, default=3, help='検索する類似ドキュメントの数')
    parser.add_argument('--cutoff', type=float, default=0.7, help='類似度のカットオフ値')
    parser.add_argument('--verbose', action='store_true', help='詳細な出力を表示')
    args = parser.parse_args()
    
    # インデックスのロード
    print("インデックスをロードしています...")
    index = load_index()
    if index is None:
        return
    
    # チャットエンジンの作成
    print("チャットエンジンを準備しています...")
    chat_engine = create_chat_engine(
        index, 
        similarity_top_k=args.top_k, 
        similarity_cutoff=args.cutoff, 
        verbose=args.verbose
    )
    if chat_engine is None:
        return
    
    print("\n=== 高度なRAGチャットシステム ===")
    print(f"設定: 検索数={args.top_k}, 類似度閾値={args.cutoff}, 詳細モード={args.verbose}")
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
                sources = format_sources(response.source_nodes)
                for source in sources:
                    print(f"  {source}")
            else:
                print("\n参照情報: なし")
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()