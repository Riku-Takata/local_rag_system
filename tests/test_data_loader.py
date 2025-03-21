import os
import pytest
from unittest.mock import patch, MagicMock
from src.utils.data_loader import load_documents

def test_load_documents_exists():
    """load_documents関数が存在することをテストする"""
    assert callable(load_documents)

@patch('src.utils.data_loader.SimpleDirectoryReader')
@patch('src.utils.data_loader.PDF_DIR', '/test/path')
def test_load_documents_calls_reader(mock_reader):
    """SimpleDirectoryReaderが正しいパラメータで呼び出されることをテストする"""
    # セットアップ
    mock_reader_instance = MagicMock()
    mock_reader.return_value = mock_reader_instance
    mock_reader_instance.load_data.return_value = ["doc1", "doc2"]
    
    # 実行
    result = load_documents()
    
    # アサート
    mock_reader.assert_called_once_with('/test/path', recursive=True, file_extensions=['.pdf'])
    mock_reader_instance.load_data.assert_called_once()
    assert result == ["doc1", "doc2"]

@patch('src.utils.data_loader.SimpleDirectoryReader')
@patch('src.utils.data_loader.PDF_DIR', '/empty/path')
def test_load_documents_empty_dir(mock_reader):
    """空のディレクトリの処理をテストする"""
    # セットアップ
    mock_reader_instance = MagicMock()
    mock_reader.return_value = mock_reader_instance
    mock_reader_instance.load_data.return_value = []
    
    # 実行
    result = load_documents()
    
    # アサート
    assert result == []

@pytest.mark.parametrize(
    "exception,expected_message",
    [
        (FileNotFoundError, "Directory not found"),
        (PermissionError, "Permission denied"),
    ],
)
@patch('src.utils.data_loader.SimpleDirectoryReader')
@patch('src.utils.data_loader.PDF_DIR', '/test/path')
def test_load_documents_exceptions(mock_reader, exception, expected_message):
    """例外処理をテストする"""
    # セットアップ
    mock_reader.side_effect = exception(expected_message)
    
    # 実行とアサート
    with pytest.raises(exception) as excinfo:
        load_documents()
    assert expected_message in str(excinfo.value)