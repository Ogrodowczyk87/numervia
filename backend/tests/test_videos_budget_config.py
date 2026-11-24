import pytest
from pydantic import ValidationError

from app.videos.state import VideoBudget


@pytest.mark.parametrize(
    "daily,cost,budget",
    [(100, 1, 81), (10000, 100, 81), (10, 1, 8), (100, 0, 12), (0, 1, 12)],
)
def test_video_budget_rejects_unsafe_or_insufficient_configuration(daily, cost, budget):
    with pytest.raises(ValidationError):
        VideoBudget(daily_quota=daily, cost_per_search=cost, request_budget=budget)
