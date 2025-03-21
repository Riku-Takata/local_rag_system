import pytest
from unittest.mock import patch
from src.utils.text_extractor import extract_text_from_pdf

def test_extract_text_exists():
    """extract_text_from_pdf関数が存在することをテストする"""
    assert callable(extract_text_from_pdf)

@patch('src.utils.text_extractor.extract_text')
def test_extract_text_from_pdf(mock_extract):
    """PDFからテキストが正しく抽出されることをテストする"""
    # セットアップ
    mock_extract.return_value = "サンプル抽出テキスト"
    
    # 実行
    result = extract_text_from_pdf("test.pdf")
    
    # アサート
    mock_extract.assert_called_once_with("test.pdf")
    assert result == "サンプル抽出テキスト"

@pytest.mark.parametrize(
    "exception,expected_message",
    [
        (FileNotFoundError, "File not found"),
        (PermissionError, "Permission denied"),
        (ValueError, "Invalid PDF file"),
    ],
)
@patch('src.utils.text_extractor.extract_text')
def test_extract_text_exceptions(mock_extract, exception, expected_message):
    """例外処理をテストする"""
    # セットアップ
    mock_extract.side_effect = exception(expected_message)
    
    # 実行とアサート
    with pytest.raises(exception) as excinfo:
        extract_text_from_pdf("test.pdf")
    assert expected_message in str(excinfo.value)