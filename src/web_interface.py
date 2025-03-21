from flask import Flask, render_template, request, jsonify
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.llms import Ollama
from llama_index.core.memory import ChatMemoryBuffer
from config import INDEX_DIR, LLM_MODEL
import os

app = Flask(__name__)

# チャットエンジンのインスタンスを保持する辞書
chat_engines = {}

def initialize_chat_engine():
    """チャットエンジンを初期化する関数"""
    try:
        # インデックスのロード
        if not os.path.exists(INDEX_DIR):
            return {"error": f"インデックスディレクトリ '{INDEX_DIR}' が見つかりません。"}
        
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        index = load_index_from_storage(storage_context)
        
        # LLMの設定
        llm = Ollama(model=LLM_MODEL)
        
        # チャットメモリの設定
        memory = ChatMemoryBuffer.from_defaults(token_limit=4096)
        
        # コンテキストチャットエンジンの設定
        chat_engine = ContextChatEngine.from_defaults(
            index=index,
            llm=llm,
            memory=memory,
            context_prompt=(
                "あなたは日本語で応答するアシスタントです。"
                "以下の情報源を参考にして、ユーザーの質問に答えてください。"
                "情報源に含まれない内容についてはわからないと正直に答えてください。"
                "回答には参照した情報源の箇所を引用してください。"
            ),
            citation_query_kwargs={"similarity_top_k": 3},
            verbose=True
        )
        
        return {"chat_engine": chat_engine}
    
    except Exception as e:
        return {"error": f"チャットエンジンの初期化中にエラーが発生しました: {str(e)}"}

@app.route('/')
def home():
    """ホームページのルート"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """チャットAPIエンドポイント"""
    # リクエストからデータを取得
    data = request.json
    session_id = data.get('session_id', 'default')
    message = data.get('message', '')
    
    # セッションIDに対応するチャットエンジンを取得または作成
    if session_id not in chat_engines:
        result = initialize_chat_engine()
        if "error" in result:
            return jsonify({"error": result["error"]})
        chat_engines[session_id] = result["chat_engine"]
    
    chat_engine = chat_engines[session_id]
    
    try:
        # クエリの実行
        response = chat_engine.chat(message)
        
        # 引用元の取得
        sources = []
        if hasattr(response, 'source_nodes') and response.source_nodes:
            for node in response.source_nodes:
                if hasattr(node, 'metadata') and 'file_path' in node.metadata:
                    source = os.path.basename(node.metadata['file_path'])
                    sources.append(source)
        
        return jsonify({
            "response": response.response,
            "sources": sources
        })
    
    except Exception as e:
        return jsonify({"error": f"エラーが発生しました: {str(e)}"})

# テンプレートディレクトリの作成
@app.before_first_request
def setup_templates():
    """テンプレートディレクトリのセットアップ"""
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # index.htmlの作成
    index_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RAGチャットシステム</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Helvetica Neue', Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .chat-container {
                height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 20px;
            }
            .message {
                margin-bottom: 10px;
                padding: 8px 12px;
                border-radius: 18px;
                max-width: 80%;
                word-wrap: break-word;
            }
            .user-message {
                background-color: #dcf8c6;
                margin-left: auto;
                margin-right: 0;
            }
            .assistant-message {
                background-color: #f1f0f0;
            }
            .input-container {
                display: flex;
            }
            #user-input {
                flex-grow: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }
            #send-button {
                padding: 10px 20px;
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 5px;
                margin-left: 10px;
                cursor: pointer;
                font-size: 16px;
            }
            .sources {
                font-size: 12px;
                color: #666;
                margin-top: 5px;
                font-style: italic;
            }
            .error {
                color: red;
                font-weight: bold;
            }
            .loading {
                text-align: center;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>RAGチャットシステム</h1>
            <div id="chat-container" class="chat-container"></div>
            <div class="input-container">
                <input type="text" id="user-input" placeholder="質問を入力してください..." />
                <button id="send-button">送信</button>
            </div>
        </div>

        <script>
            // セッションIDの生成（ブラウザを閉じるまで同じIDを使用）
            const sessionId = Math.random().toString(36).substring(2, 15);
            const chatContainer = document.getElementById('chat-container');
            const userInput = document.getElementById('user-input');
            const sendButton = document.getElementById('send-button');

            // メッセージの追加
            function addMessage(content, isUser, sources = []) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'assistant-message'}`;
                messageDiv.textContent = content;
                
                // 情報源の追加
                if (!isUser && sources.length > 0) {
                    const sourcesDiv = document.createElement('div');
                    sourcesDiv.className = 'sources';
                    sourcesDiv.textContent = '参照: ' + sources.join(', ');
                    messageDiv.appendChild(sourcesDiv);
                }
                
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            // ローディング表示の追加/削除
            function toggleLoading(show) {
                if (show) {
                    const loadingDiv = document.createElement('div');
                    loadingDiv.id = 'loading';
                    loadingDiv.className = 'loading';
                    loadingDiv.textContent = '考え中...';
                    chatContainer.appendChild(loadingDiv);
                } else {
                    const loadingDiv = document.getElementById('loading');
                    if (loadingDiv) loadingDiv.remove();
                }
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            // メッセージの送信
            async function sendMessage() {
                const message = userInput.value.trim();
                if (!message) return;
                
                // ユーザーメッセージの表示
                addMessage(message, true);
                userInput.value = '';
                
                // ローディング表示
                toggleLoading(true);
                
                try {
                    // APIにリクエスト
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            session_id: sessionId,
                            message: message
                        }),
                    });
                    
                    const data = await response.json();
                    
                    // ローディング表示を削除
                    toggleLoading(false);
                    
                    if (data.error) {
                        // エラーメッセージの表示
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'message assistant-message error';
                        errorDiv.textContent = data.error;
                        chatContainer.appendChild(errorDiv);
                    } else {
                        // アシスタントの応答を表示
                        addMessage(data.response, false, data.sources);
                    }
                } catch (error) {
                    // ローディング表示を削除
                    toggleLoading(false);
                    
                    // エラーメッセージの表示
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'message assistant-message error';
                    errorDiv.textContent = 'ネットワークエラーが発生しました。';
                    chatContainer.appendChild(errorDiv);
                    console.error('Error:', error);
                }
            }

            // イベントリスナーの設定
            sendButton.addEventListener('click', sendMessage);
            userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendMessage();
            });

            // 初期メッセージ
            addMessage('こんにちは！資料について質問してください。', false);
        </script>
    </body>
    </html>
    """
    
    with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)