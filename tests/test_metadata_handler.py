import pytest
from src.utils.metadata_handler import add_folder_metadata

class MockDocument:
    def __init__(self, file_path):
        self.metadata = {'file_path': file_path}

def test_add_folder_metadata_exists():
    """add_folder_metadata関数が存在することをテストする"""
    assert callable(add_folder_metadata)

def test_add_folder_metadata():
    """フォルダメタデータが正しく追加されることをテストする"""
    # セットアップ
    docs = [
        MockDocument("/path/to/file1.pdf"),
        MockDocument("/another/path/file2.pdf"),
        MockDocument("file3.pdf")
    ]
    
    # 実行
    result = add_folder_metadata(docs)
    
    # アサート
    assert result[0].metadata['folder'] == "/path/to"
    assert result[1].metadata['folder'] == "/another/path"
    assert result[2].metadata['folder'] == ""

def test_add_folder_metadata_empty_list():
    """空のドキュメントリストのテスト"""
    # セットアップ
    docs = []
    
    # 実行
    result = add_folder_metadata(docs)
    
    # アサート
    assert result == []

def test_add_folder_metadata_missing_file_path():
    """file_pathがないドキュメントの処理テスト"""
    # セットアップ
    doc_with_path = MockDocument("/path/to/file.pdf")
    doc_without_path = MockDocument.__new__(MockDocument)
    doc_without_path.metadata = {}  # file_pathなし
    
    docs = [doc_with_path, doc_without_path]
    
    # 実行とアサート
    with pytest.raises(KeyError):
        add_folder_metadata(docs)