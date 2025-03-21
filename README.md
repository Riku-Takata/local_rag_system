# RAG System

日本語対応の検索拡張生成 (RAG) システム。PDF文書を取り込み、ベクトル検索を用いて質問応答を行います。

## 🌟 特徴

- PDF文書の自動インデックス化
- 多言語対応（特に日本語に最適化）
- コンテキストに基づく正確な回答生成
- ローカルLLMを使用したプライバシー保護
- インタラクティブCLIと簡易Webインターフェース
- ドキュメント参照の明示的な引用

## 🛠️ 技術スタック

- **フレームワーク**: [LlamaIndex](https://www.llamaindex.ai/) (≥0.9.0)
- **埋め込みモデル**: [sentence-transformers](https://www.sbert.net/) (paraphrase-multilingual-MiniLM-L12-v2)
- **ベクトルストア**: [FAISS](https://github.com/facebookresearch/faiss)
- **ローカルLLM**: [Ollama](https://ollama.ai/) (mistral:7b)
- **PDFパーサー**: pdfminer.six
- **Webインターフェース**: Flask
- **テスト**: pytest

## 📋 前提条件

- Python 3.8+
- [Ollama](https://ollama.ai/download)がインストールされ、実行中であること
- Ollama上で`mistral:7b`モデルをダウンロード済み
  ```
  ollama pull mistral:7b
  ```

## 🚀 セットアップと実行

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/japanese-rag-system.git
cd japanese-rag-system
```

### 2. Python仮想環境の作成

```bash
python -m venv rag_env
source rag_env/bin/activate  # Linuxの場合
# または
rag_env\Scripts\activate     # Windowsの場合
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 環境設定ファイルの作成

プロジェクトのルートディレクトリに`.env`ファイルを作成:

```
PDF_DIR=/path/to/your/pdf/documents
INDEX_DIR=/path/to/store/vector/index
```

- `PDF_DIR`: PDF文書が格納されているディレクトリへのパス
- `INDEX_DIR`: ベクトルインデックスを保存するディレクトリへのパス

### 5. インデックスの作成

```bash
python src/main.py
```

### 6. インタラクティブRAGシステムの起動

基本版:
```bash
python src/interactive_rag.py
```

高度な機能を備えたバージョン:
```bash
python src/advanced_rag.py
```

Webインターフェース:
```bash
python src/web_interface.py
```
その後、ブラウザで `http://localhost:5000` にアクセスしてください。

## 🏗️ プロジェクト構成

```
japanese-rag-system/
├── .env                    # 環境変数設定ファイル（作成が必要）
├── .gitignore              # Gitの除外設定
├── README.md               # プロジェクト説明
├── requirements.txt        # 依存パッケージリスト
├── src/                    # ソースコード
│   ├── advanced_rag.py     # 高度なRAGシステム（類似度フィルタリング等）
│   ├── check_embeddings.py # エンベディングモデル診断ツール
│   ├── check_llms.py       # LLMモジュール診断ツール
│   ├── config.py           # 設定ファイル
│   ├── find_pdf_reader.py  # PDFリーダー設定診断ツール
│   ├── install_check.py    # インストール状態確認ツール
│   ├── interactive_rag.py  # 基本的なRAGシステム
│   ├── main.py             # インデックス作成のエントリーポイント
│   ├── web_interface.py    # Webインターフェース
│   └── utils/              # ユーティリティ関数
│       ├── __init__.py     
│       ├── data_loader.py  # PDF文書ローダー
│       ├── metadata_handler.py # メタデータ処理
│       └── text_extractor.py  # テキスト抽出
└── tests/                  # テストコード
    ├── test_data_loader.py 
    ├── test_indexing.py
    ├── test_metadata_handler.py
    └── test_text_extractor.py
```

## 🔧 カスタマイズオプション

### 埋め込みモデルの変更

`src/config.py`ファイルを編集して、異なる埋め込みモデルを使用できます:

```python
EMBED_MODEL_NAME = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
```

### LLMモデルの変更

`src/config.py`ファイルでOllamaモデルを別のものに変更できます:

```python
LLM_MODEL = 'mistral:7b'
```

Ollama対応の他のモデル（例: `llama3`、`mistral-openorca`など）も使用可能です。

### 検索パラメータの調整

`advanced_rag.py`で実行時に検索パラメータを指定できます:

```bash
python src/advanced_rag.py --top-k 5 --cutoff 0.5 --verbose
```

- `--top-k`: 検索する類似ドキュメントの数
- `--cutoff`: 類似度のカットオフ値（これより低いものは除外）
- `--verbose`: 詳細なログを出力

## 📝 使用例

1. PDF文書を`PDF_DIR`に配置します
2. `python src/main.py`を実行してインデックスを作成します
3. `python src/interactive_rag.py`を実行してRAGシステムを起動します
4. 質問を入力すると、関連文書に基づいた回答が生成されます

```
=== RAGチャットシステム ===
質問を入力してください。終了するには 'exit' または 'quit' と入力してください。

あなた: このプロジェクトの目的は何ですか？

アシスタント: このプロジェクトは、日本語PDFドキュメントを検索可能なインデックスに変換し、
それに基づいて質問応答を行うRAG（検索拡張生成）システムを提供することが目的です。
...
```

## 🔍 トラブルシューティング

問題が発生した場合は以下のツールで診断できます:

```bash
python src/install_check.py    # パッケージのインストール状態を確認
python src/check_embeddings.py # エンベディングモデルの設定を診断
python src/check_llms.py       # LLMモジュールの設定を診断
python src/find_pdf_reader.py  # PDFリーダーの設定を診断
```

## 🧪 テスト

テストを実行するには:

```bash
pytest
```

または特定のテストのみ実行:

```bash
pytest tests/test_data_loader.py
```

## 📄 ライセンス

このプロジェクトはMITライセンスで公開されています。詳細はLICENSEファイルを参照してください。