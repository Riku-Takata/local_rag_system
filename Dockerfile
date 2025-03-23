FROM python:3.10-slim

WORKDIR /app

# 日本語ロケールのインストールと設定
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    locales \
    fonts-ipafont \
    && rm -rf /var/lib/apt/lists/*

# 日本語ロケールの生成と設定
RUN echo "ja_JP.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8

# 環境変数設定
ENV LANG ja_JP.UTF-8
ENV LC_ALL ja_JP.UTF-8
ENV PYTHONIOENCODING utf-8

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir llama-index-embeddings-huggingface

# アプリケーションファイルをコピー
COPY . .

# デフォルトの.envファイルを作成
RUN echo "PDF_DIR=/data/pdfs" > .env && \
    echo "INDEX_DIR=/data/index" >> .env

# ボリュームマウントポイントを作成
RUN mkdir -p /data/pdfs /data/index

# 実行コマンド（docker-composeでオーバーライド可能）
CMD ["python", "src/main.py"]
