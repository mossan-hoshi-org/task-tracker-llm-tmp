from unittest.mock import patch, MagicMock
from src.services.gemini_client import GeminiClient


class TestGeminiClient:
    def test_gemini_client_initialization(self) -> None:
        client = GeminiClient(api_key="test_key")

        assert client.api_key == "test_key"

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_categorize_tasks_returns_mock_response(
        self, mock_model_class: MagicMock, mock_configure: MagicMock
    ) -> None:
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_model.generate_content.side_effect = Exception("Test error")

        client = GeminiClient(api_key="test_key")
        tasks = ["プロジェクトA開発", "プロジェクトA会議", "メール対応"]

        result = client.categorize_tasks(tasks)

        assert isinstance(result, dict)
        assert "categories" in result
        assert len(result["categories"]) > 0

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_categorize_tasks_mock_categories(self, mock_model_class: MagicMock, mock_configure: MagicMock) -> None:
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_model.generate_content.side_effect = Exception("Test error")

        client = GeminiClient(api_key="test_key")
        tasks = ["プロジェクトX React開発", "プロジェクトX コードレビュー", "プロジェクトY会議", "メール返信"]

        result = client.categorize_tasks(tasks)

        categories = result["categories"]
        assert any(cat["name"] == "プロジェクトX" for cat in categories)
        assert any(cat["name"] == "プロジェクトY" for cat in categories)
        # "その他" may or may not exist depending on uncategorized tasks

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_categorize_empty_tasks(self, mock_model_class: MagicMock, mock_configure: MagicMock) -> None:
        client = GeminiClient(api_key="test_key")

        result = client.categorize_tasks([])

        assert result == {"categories": []}

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_categorize_tasks_with_real_api(self, mock_model_class: MagicMock, mock_configure: MagicMock) -> None:
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model

        mock_response = MagicMock()
        mock_response.text = """
        {
            "categories": [
                {
                    "name": "プロジェクトA",
                    "tasks": ["プロジェクトA React開発", "プロジェクトA コードレビュー"]
                },
                {
                    "name": "プロジェクトB",
                    "tasks": ["プロジェクトB会議", "プロジェクトBメール返信"]
                }
            ]
        }
        """
        mock_model.generate_content.return_value = mock_response

        client = GeminiClient(api_key="test_key")
        tasks = [
            "プロジェクトA React開発",
            "プロジェクトA コードレビュー",
            "プロジェクトB会議",
            "プロジェクトBメール返信",
        ]

        result = client.categorize_tasks(tasks)

        assert isinstance(result, dict)
        assert "categories" in result
        assert len(result["categories"]) == 2
        assert result["categories"][0]["name"] == "プロジェクトA"
        assert result["categories"][1]["name"] == "プロジェクトB"

    @patch("google.generativeai.configure")
    def test_gemini_client_configures_api_key(self, mock_configure: MagicMock) -> None:
        client = GeminiClient(api_key="test_key")
        client.categorize_tasks(["test"])

        mock_configure.assert_called_once_with(api_key="test_key")

    @patch("google.generativeai.GenerativeModel")
    def test_api_error_returns_mock_response(self, mock_model_class: MagicMock) -> None:
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_model.generate_content.side_effect = Exception("API Error")

        client = GeminiClient(api_key="test_key")

        result = client.categorize_tasks(["test"])

        assert isinstance(result, dict)
        assert "categories" in result

    def test_json_parsing_from_response(self) -> None:
        with patch("google.generativeai.configure"):
            with patch("google.generativeai.GenerativeModel") as mock_model_class:
                mock_model = MagicMock()
                mock_model_class.return_value = mock_model

                mock_response = MagicMock()
                mock_response.text = """```json
{
    "categories": [
        {
            "name": "プロジェクトZ",
            "tasks": ["プロジェクトZコード実装", "プロジェクトZバグ修正"]
        }
    ]
}
```"""
                mock_model.generate_content.return_value = mock_response

                client = GeminiClient(api_key="test_key")
                result = client.categorize_tasks(["プロジェクトZコード実装", "プロジェクトZバグ修正"])

                assert result == {
                    "categories": [
                        {"name": "プロジェクトZ", "tasks": ["プロジェクトZコード実装", "プロジェクトZバグ修正"]}
                    ]
                }

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_uncategorized_tasks_go_to_others(self, mock_model_class: MagicMock, mock_configure: MagicMock) -> None:
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_model.generate_content.side_effect = Exception("Test error")

        client = GeminiClient(api_key="test_key")
        tasks = ["プロジェクトA開発", "雑務", "メール対応", "勉強会"]

        result = client.categorize_tasks(tasks)

        categories = result["categories"]
        assert any(cat["name"] == "プロジェクトA" for cat in categories)
        assert any(cat["name"] == "その他" for cat in categories)

        # Find その他 category and check its contents
        for cat in categories:
            if cat["name"] == "その他":
                assert "雑務" in cat["tasks"]
                assert "メール対応" in cat["tasks"]
                assert "勉強会" in cat["tasks"]
