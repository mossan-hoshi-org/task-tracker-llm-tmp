from unittest.mock import Mock, patch

from src.utils.clipboard import copy_to_clipboard


class TestClipboard:
    @patch("src.utils.clipboard.tk.Tk")
    def test_copy_to_clipboard(self, mock_tk_class: Mock) -> None:
        mock_root = Mock()
        mock_tk_class.return_value = mock_root

        test_text = "Test text for clipboard"
        copy_to_clipboard(test_text)

        mock_tk_class.assert_called_once()
        mock_root.withdraw.assert_called_once()
        mock_root.clipboard_clear.assert_called_once()
        mock_root.clipboard_append.assert_called_once_with(test_text)
        mock_root.update.assert_called_once()
        mock_root.destroy.assert_called_once()
