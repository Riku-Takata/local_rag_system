from llama_index import VectorStoreIndex
from llama_index.llms import Ollama
from config import INDEX_DIR, LLM_MODEL

# インデックスのロード
index = VectorStoreIndex.load_from_disk(INDEX_DIR)

# LLMの設定
llm = Ollama(model=LLM_MODEL)

# クエリエンジンの設定
query_engine = index.as_query_engine(llm=llm)

# クエリの実行
response = query_engine.query("リモートワークの生産性への影響は何ですか？")
print(response)