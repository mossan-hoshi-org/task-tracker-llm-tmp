from typing import Dict, List, Any
from src.models.session import Session


class CategoryAggregator:
    def aggregate(self, sessions: List[Session], categories: Dict[str, Any]) -> List[Dict[str, Any]]:
        assert isinstance(sessions, list), "Sessions must be a list"
        assert isinstance(categories, dict), "Categories must be a dict"
        assert "categories" in categories, "Categories dict must have 'categories' key"

        if not sessions or not categories["categories"]:
            return []

        # Create task to category mapping
        task_to_category: Dict[str, str] = {}
        for category in categories["categories"]:
            for task in category["tasks"]:
                task_to_category[task] = category["name"]

        # Aggregate time by category and task
        category_data: Dict[str, Dict[str, Any]] = {}

        for session in sessions:
            category_name = task_to_category.get(session.task_name)
            if not category_name:
                continue  # Skip uncategorized tasks

            if category_name not in category_data:
                category_data[category_name] = {"name": category_name, "total_seconds": 0, "tasks": {}}

            # Add time to category total
            duration = session.get_duration()
            category_data[category_name]["total_seconds"] += duration

            # Add time to task within category
            task_name = session.task_name
            if task_name not in category_data[category_name]["tasks"]:
                category_data[category_name]["tasks"][task_name] = {"name": task_name, "total_seconds": 0}
            category_data[category_name]["tasks"][task_name]["total_seconds"] += duration

        # Convert to final format
        result = []
        for category_name, data in category_data.items():
            category_result = {
                "name": data["name"],
                "total_seconds": data["total_seconds"],
                "total_time": self._format_duration(data["total_seconds"]),
                "tasks": [],
            }

            for task_name, task_data in data["tasks"].items():
                category_result["tasks"].append(
                    {
                        "name": task_data["name"],
                        "total_seconds": task_data["total_seconds"],
                        "total_time": self._format_duration(task_data["total_seconds"]),
                    }
                )

            result.append(category_result)

        return result

    def _format_duration(self, seconds: int) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        return f"{hours}:{minutes:02d}:{remaining_seconds:02d}"
