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
git clone https://github.com/yourusername/local_rag_system.git
cd japanese-rag-system
```

### 2. Python仮想環境の作成

```bash
python -m venv rag_env
source rag_env/bin/activate  # Linuxの場合
# または
.\rag_env\Scripts\activate     # Windowsの場合
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

- `PDF_DIR`: PDF文書が格納されているディレクトリへのパス（ここをOnedrive上のPDF資料を入れていたディレクトリパスにする。エクスプローラーでコピーできるやつ。）
- `INDEX_DIR`: ベクトルインデックスを保存するディレクトリへのパス（ここは`src/index/faiss_index`とした）

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

# 技術スタックの詳細説明

## LlamaIndex (≥0.9.0)
LlamaIndexは検索拡張生成(RAG)システム構築のための高度なフレームワークです。

- **主な機能**：
  - ドキュメントの読み込み、分割、インデックス化
  - セマンティック検索と取得
  - LLMと組み合わせたコンテキスト付き回答生成
  - 様々なベクトルデータベースとの連携

- **このプロジェクトでの役割**：
  - PDFからのテキスト抽出とチャンク分割の自動化
  - ベクトル検索インデックスの管理
  - ユーザークエリに関連するコンテキストの検索
  - Ollamaとの統合によるLLM推論制御

- **特徴的な実装**：
  - `VectorStoreIndex.from_documents`でドキュメントからインデックスを作成
  - `ContextChatEngine`でコンテキスト対応の会話機能を実現
  - `SimilarityPostprocessor`で類似度に基づくフィルタリング

## sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2)
文や段落をベクトル空間に変換するための最先端の埋め込みモデルライブラリです。

- **主な機能**：
  - テキストを固定長の密ベクトルに変換
  - 意味的類似性に基づく検索を可能に
  - 多言語対応モデルを提供

- **paraphrase-multilingual-MiniLM-L12-v2の特徴**：
  - 50以上の言語をサポート（日本語含む）
  - 小型かつ高性能（384次元のベクトル出力）
  - 文間の意味的類似性を効果的にキャプチャ

- **このプロジェクトでの役割**：
  - PDFから抽出された日本語テキストの埋め込み生成
  - 質問とドキュメントの意味的関連性の計算

## FAISS (Facebook AI Similarity Search)
Facebookが開発した、大規模な高次元ベクトルデータを効率的に保存・検索するライブラリです。

- **主な機能**：
  - 数十億のベクトルを扱える拡張性
  - GPUサポートによる高速検索
  - 複数の索引タイプとクラスタリング機能

- **このプロジェクトでの役割**：
  - 埋め込みベクトルのインデックス化と保存
  - 質問ベクトルに対する最近傍検索の実行
  - RAGシステムのベクトルストアとして機能

- **特徴的な実装**：
  - `faiss-cpu`バージョンを使用（CPU最適化版）
  - `INDEX_DIR`内に永続化されたインデックスを保存

## Ollama (mistral:7b)
大規模言語モデル（LLM）をローカル環境で実行するためのツールです。

- **主な機能**：
  - オープンソースモデルのダウンロードと管理
  - RESTful APIによるシンプルなアクセス
  - ローカル環境での推論実行

- **mistral:7bモデルの特徴**：
  - 70億パラメータの高性能モデル
  - 多言語対応（日本語含む）
  - 推論速度と品質のバランスが良好

- **このプロジェクトでの役割**：
  - 検索されたコンテキストに基づく回答生成
  - 会話の履歴管理と継続的な対話の維持
  - プライバシー保護（データがローカル環境で処理される）

- **設定例**：
  ```python
  llm = Ollama(model="mistral:7b", temperature=0.1)
  ```

## pdfminer.six
PDFドキュメントからテキストを抽出するためのPythonライブラリです。

- **主な機能**：
  - PDFからのテキスト、レイアウト、フォント情報の抽出
  - Unicode対応（日本語などの多言語処理）
  - 組み込みのPDF分析ツール

- **このプロジェクトでの役割**：
  - PDFファイルからのテキスト抽出
  - 抽出したテキストの前処理とインデックス作成の準備

- **実装例**：
  ```python
  from pdfminer.high_level import extract_text
  text = extract_text("document.pdf")
  ```

## 技術スタックの連携フロー

1. **ドキュメント処理**：pdfminer.sixがPDFからテキストを抽出
2. **埋め込み生成**：sentence-transformersがテキストチャンクをベクトル化
3. **インデックス作成**：FAISSがベクトルを効率的に保存・索引付け
4. **検索**：LlamaIndexがユーザークエリを処理し、関連コンテキストを検索
5. **回答生成**：OllamaのLLMが検索されたコンテキストを使って回答を生成

このアーキテクチャにより、ローカル環境で高性能な日本語対応RAGシステムが実現しています。
