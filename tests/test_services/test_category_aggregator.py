from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.models.session import Session
from src.services.category_aggregator import CategoryAggregator


class TestCategoryAggregator:
    def test_aggregate_single_category(self) -> None:
        sessions = [
            self._create_session("プロジェクトA開発", minutes=30),
            self._create_session("プロジェクトA会議", minutes=15),
        ]

        categories = {"categories": [{"name": "プロジェクトA", "tasks": ["プロジェクトA開発", "プロジェクトA会議"]}]}

        aggregator = CategoryAggregator()
        result = aggregator.aggregate(sessions, categories)

        assert len(result) == 1
        assert result[0]["name"] == "プロジェクトA"
        assert result[0]["total_seconds"] == 45 * 60
        assert result[0]["total_time"] == "0:45:00"
        assert len(result[0]["tasks"]) == 2

    def test_aggregate_multiple_categories(self) -> None:
        sessions = [
            self._create_session("プロジェクトA開発", minutes=30),
            self._create_session("プロジェクトB会議", minutes=20),
            self._create_session("プロジェクトA設計", minutes=40),
        ]

        categories = {
            "categories": [
                {"name": "プロジェクトA", "tasks": ["プロジェクトA開発", "プロジェクトA設計"]},
                {"name": "プロジェクトB", "tasks": ["プロジェクトB会議"]},
            ]
        }

        aggregator = CategoryAggregator()
        result = aggregator.aggregate(sessions, categories)

        assert len(result) == 2
        assert result[0]["name"] == "プロジェクトA"
        assert result[0]["total_seconds"] == 70 * 60
        assert result[1]["name"] == "プロジェクトB"
        assert result[1]["total_seconds"] == 20 * 60

    def test_aggregate_with_uncategorized_tasks(self) -> None:
        sessions = [
            self._create_session("プロジェクトA開発", minutes=30),
            self._create_session("雑務", minutes=10),
        ]

        categories = {"categories": [{"name": "プロジェクトA", "tasks": ["プロジェクトA開発"]}]}

        aggregator = CategoryAggregator()
        result = aggregator.aggregate(sessions, categories)

        assert len(result) == 1
        assert result[0]["name"] == "プロジェクトA"
        assert result[0]["total_seconds"] == 30 * 60

    def test_aggregate_empty_sessions(self) -> None:
        sessions: List[Session] = []
        categories: Dict[str, Any] = {"categories": []}

        aggregator = CategoryAggregator()
        result = aggregator.aggregate(sessions, categories)

        assert result == []

    def test_task_details_in_result(self) -> None:
        sessions = [
            self._create_session("プロジェクトA開発", minutes=30),
            self._create_session("プロジェクトA開発", minutes=20),  # Same task
        ]

        categories = {"categories": [{"name": "プロジェクトA", "tasks": ["プロジェクトA開発"]}]}

        aggregator = CategoryAggregator()
        result = aggregator.aggregate(sessions, categories)

        assert len(result) == 1
        assert len(result[0]["tasks"]) == 1
        assert result[0]["tasks"][0]["name"] == "プロジェクトA開発"
        assert result[0]["tasks"][0]["total_seconds"] == 50 * 60
        assert result[0]["tasks"][0]["total_time"] == "0:50:00"

    def _create_session(self, task_name: str, minutes: int) -> Session:
        session = Session(task_name)
        session.start_time = datetime.now()
        session.end_time = session.start_time + timedelta(minutes=minutes)
        session.is_running = False
        return session
