from typing import Dict, List, Any


class GeminiClient:
    def __init__(self, api_key: str) -> None:
        assert api_key, "API key cannot be empty"
        self.api_key = api_key

    def categorize_tasks(self, tasks: List[str]) -> Dict[str, Any]:
        if not tasks:
            return {"categories": []}

        # Mock response for now
        mock_categories = {
            "categories": [
                {
                    "name": "開発",
                    "tasks": [
                        task
                        for task in tasks
                        if any(
                            keyword in task.lower()
                            for keyword in ["開発", "プログラミング", "コード", "実装", "react", "python"]
                        )
                    ],
                },
                {
                    "name": "コミュニケーション",
                    "tasks": [
                        task
                        for task in tasks
                        if any(
                            keyword in task.lower() for keyword in ["会議", "ミーティング", "メール", "連絡", "相談"]
                        )
                    ],
                },
                {
                    "name": "ドキュメント",
                    "tasks": [
                        task
                        for task in tasks
                        if any(keyword in task.lower() for keyword in ["ドキュメント", "資料", "仕様書", "設計"])
                    ],
                },
                {"name": "その他", "tasks": []},
            ]
        }

        # Put uncategorized tasks in "その他"
        categorized_tasks: set[str] = set()
        for category in mock_categories["categories"]:
            categorized_tasks.update(category["tasks"])

        uncategorized = [task for task in tasks if task not in categorized_tasks]
        for category in mock_categories["categories"]:
            if category["name"] == "その他":
                category["tasks"] = uncategorized
                break

        # Remove empty categories
        mock_categories["categories"] = [cat for cat in mock_categories["categories"] if cat["tasks"]]

        return mock_categories
