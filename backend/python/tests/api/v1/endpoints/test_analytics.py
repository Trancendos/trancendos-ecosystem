import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import sys

# Mock pandas and the database module before importing the application code
sys.modules["pandas"] = MagicMock()
sys.modules["app.core.database"] = MagicMock()
sys.modules["main"] = MagicMock()

from app.api.v1.endpoints.analytics import get_analytics_overview

@pytest.mark.asyncio
@patch("app.api.v1.endpoints.analytics.AnalyticsService")
async def test_get_analytics_overview_negative_income(mock_analytics_service):
    # Arrange
    mock_service_instance = mock_analytics_service.return_value
    mock_service_instance.get_total_income = AsyncMock(return_value=-100.0)
    mock_service_instance.get_total_expenses = AsyncMock(return_value=50.0)
    mock_service_instance.get_transaction_count = AsyncMock(return_value=5)
    mock_service_instance.get_top_spending_categories = AsyncMock(return_value=[])

    mock_db = AsyncMock()
    mock_current_user = {"user_id": "test_user"}

    # Act
    response = await get_analytics_overview(
        days=30,
        current_user=mock_current_user,
        db=mock_db
    )

    # Assert
    assert response.total_income == -100.0
    assert response.total_expenses == 50.0
    assert response.net_savings == -150.0
    assert response.savings_rate == 150.0
