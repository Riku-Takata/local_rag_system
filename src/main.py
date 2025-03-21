from llama_index import VectorStoreIndex, StorageContext
from llama_index.vector_stores import FaissVectorStore
from llama_index.embeddings import HuggingFaceEmbedding
from utils.data_loader import load_documents
from utils.metadata_handler import add_folder_metadata
from config import EMBED_MODEL_NAME, INDEX_DIR

# ドキュメントの読み込みとメタデータ追加
documents = load_documents()
documents = add_folder_metadata(documents)

# 埋め込みモデルの設定
embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)

# FAISSベクトルストアの設定
vector_store = FaissVectorStore(dim=384)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# インデックスの作成
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model)

# インデックスの保存
index.storage_context.persist(persist_dir=INDEX_DIR)