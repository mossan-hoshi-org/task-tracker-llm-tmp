from typing import Dict, List, Any
import json
import google.generativeai as genai  # type: ignore


class GeminiClient:
    def __init__(self, api_key: str) -> None:
        assert api_key, "API key cannot be empty"
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def categorize_tasks(self, tasks: List[str]) -> Dict[str, Any]:
        if not tasks:
            return {"categories": []}

        prompt = f"""以下のタスクリストをプロジェクト別にカテゴリ分類してください。
タスク名からプロジェクト名を識別し、同じプロジェクトのタスクをまとめてください。
各タスクは必ず1つのカテゴリに属するようにしてください。

タスクリスト:
{json.dumps(tasks, ensure_ascii=False, indent=2)}

分類のルール:
- タスク名にプロジェクト名が含まれている場合は、そのプロジェクト名をカテゴリとする
- 例: "プロジェクトA社内打ち合わせ" → カテゴリ: "プロジェクトA"
- プロジェクト名が不明確な場合は "その他" カテゴリに分類

以下のJSON形式で回答してください:
{{
    "categories": [
        {{
            "name": "カテゴリ名（プロジェクト名）",
            "tasks": ["タスク1", "タスク2"]
        }}
    ]
}}

JSONのみを返してください。説明文は不要です。"""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # Extract JSON from response
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            return json.loads(response_text)  # type: ignore
        except Exception as e:
            # Fallback to mock response on error
            print(f"Error calling Gemini API: {e}")
            return self._get_mock_response(tasks)

    def _get_mock_response(self, tasks: List[str]) -> Dict[str, Any]:
        # Extract project names from tasks
        project_categories: Dict[str, List[str]] = {}

        for task in tasks:
            # Try to extract project name from task
            project_found = False

            # Pattern: Extract project names from task
            import re

            project_patterns = [
                r"(プロジェクト[A-Za-z0-9]+)",
                r"(Project[A-Za-z0-9]+)",
                r"([A-Z][A-Za-z0-9]+プロジェクト)",
                r"([A-Z][A-Za-z0-9]+案件)",
            ]

            for pattern in project_patterns:
                match = re.search(pattern, task)
                if match:
                    project_name = match.group(1)
                    if project_name not in project_categories:
                        project_categories[project_name] = []
                    project_categories[project_name].append(task)
                    project_found = True
                    break

            if not project_found:
                if "その他" not in project_categories:
                    project_categories["その他"] = []
                project_categories["その他"].append(task)

        # Convert to expected format
        mock_categories = {
            "categories": [
                {"name": name, "tasks": task_list}
                for name, task_list in project_categories.items()
                if task_list  # Only include non-empty categories
            ]
        }

        return mock_categories
