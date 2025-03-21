import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# srcディレクトリをパスに追加してモジュールをインポートできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@patch('src.main.load_documents')
@patch('src.main.add_folder_metadata')
@patch('src.main.HuggingFaceEmbedding')
@patch('src.main.FaissVectorStore')
@patch('src.main.StorageContext.from_defaults')
@patch('src.main.VectorStoreIndex.from_documents')
def test_indexing_process(mock_index, mock_storage, mock_faiss, mock_embedding, 
                         mock_metadata, mock_load_docs):
    """インデックス作成プロセス全体をテストする"""
    # セットアップ
    mock_docs = [MagicMock(), MagicMock()]
    mock_load_docs.return_value = mock_docs
    mock_metadata.return_value = mock_docs
    
    mock_embed_instance = MagicMock()
    mock_embedding.return_value = mock_embed_instance
    
    mock_vector_instance = MagicMock()
    mock_faiss.return_value = mock_vector_instance
    
    mock_storage_instance = MagicMock()
    mock_storage.return_value = mock_storage_instance
    
    mock_index_instance = MagicMock()
    mock_index.return_value = mock_index_instance
    
    # インポートしてmainモジュールを実行
    import src.main
    
    # アサート
    mock_load_docs.assert_called_once()
    mock_metadata.assert_called_once_with(mock_docs)
    mock_embedding.assert_called_once()
    mock_faiss.assert_called_once_with(dim=384)
    mock_storage.assert_called_once_with(vector_store=mock_vector_instance)
    mock_index.assert_called_once_with(mock_docs, 
                                      storage_context=mock_storage_instance, 
                                      embed_model=mock_embed_instance)
    mock_index_instance.storage_context.persist.assert_called_once()