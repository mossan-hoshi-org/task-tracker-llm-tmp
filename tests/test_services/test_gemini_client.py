from src.services.gemini_client import GeminiClient


class TestGeminiClient:
    def test_gemini_client_initialization(self) -> None:
        client = GeminiClient(api_key="test_key")

        assert client.api_key == "test_key"

    def test_categorize_tasks_returns_mock_response(self) -> None:
        client = GeminiClient(api_key="test_key")
        tasks = ["プログラミング", "会議", "メール対応"]

        result = client.categorize_tasks(tasks)

        assert isinstance(result, dict)
        assert "categories" in result
        assert len(result["categories"]) > 0

    def test_categorize_tasks_mock_categories(self) -> None:
        client = GeminiClient(api_key="test_key")
        tasks = ["React開発", "コードレビュー", "会議", "メール返信"]

        result = client.categorize_tasks(tasks)

        categories = result["categories"]
        assert any(cat["name"] == "開発" for cat in categories)
        assert any(cat["name"] == "コミュニケーション" for cat in categories)

    def test_categorize_empty_tasks(self) -> None:
        client = GeminiClient(api_key="test_key")

        result = client.categorize_tasks([])

        assert result == {"categories": []}
