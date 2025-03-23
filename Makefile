.PHONY: build start stop index interactive advanced web test clean logs

# ビルドと初期セットアップ
build:
	docker-compose build

# コンテナを起動し、Webインターフェースを実行（デフォルト）
start:
	docker-compose up -d

# コンテナを停止
stop:
	docker-compose down

# インデックスの作成
index:
	docker-compose run --rm rag-app python src/main.py

# インタラクティブRAGシステムの実行
interactive:
	docker-compose run --rm rag-app python src/interactive_rag.py

# 高度な機能を備えたRAGシステムの実行
advanced:
	docker-compose run --rm rag-app python src/advanced_rag.py

# Webインターフェースの実行（既定）
web:
	docker-compose run --rm -p 5000:5000 rag-app python src/web_interface.py

# テストの実行
test:
	docker-compose run --rm rag-app pytest

# コンテナとイメージを削除（ボリュームは残す）
clean:
	docker-compose down --rmi local

# ログの表示
logs:
	docker-compose logs -f

# PDFファイルをコンテナにコピー
copy-pdfs:
	@echo "PDFファイルをコンテナにコピーするには以下のコマンドを使用してください："
	@echo "docker cp /path/to/your/pdfs/. rag-app:/data/pdfs/"