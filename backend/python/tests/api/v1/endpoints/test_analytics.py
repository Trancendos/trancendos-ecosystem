import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import types
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np

# Create dummy pydantic models to satisfy FastAPI decorators
class DummyAnalyticsResponse(BaseModel):
    period_days: int
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate: float
    transaction_count: int
    top_categories: list
    generated_at: datetime

class DummySpendingPatternResponse(BaseModel):
    period_days: int
    avg_daily_spending: float
    max_spending_day: float
    min_spending_day: float
    spending_volatility: float
    monthly_trends: dict
    generated_at: datetime

class DummyCategoryAnalysisResponse(BaseModel):
    period_days: int
    category: Optional[str]
    analysis_data: dict
    generated_at: datetime

class DummyTrendAnalysisResponse(BaseModel):
    trend_type: str
    period: str
    trend_data: list
    generated_at: datetime

# Create mock modules and inject dummy models
mock_schemas_analytics = types.ModuleType('app.schemas.analytics')
mock_schemas_analytics.AnalyticsResponse = DummyAnalyticsResponse
mock_schemas_analytics.SpendingPatternResponse = DummySpendingPatternResponse
mock_schemas_analytics.CategoryAnalysisResponse = DummyCategoryAnalysisResponse
mock_schemas_analytics.TrendAnalysisResponse = DummyTrendAnalysisResponse
sys.modules['app.schemas.analytics'] = mock_schemas_analytics

# Mock other missing dependencies
sys.modules['app.core.database'] = MagicMock()
sys.modules['app.models.transaction'] = MagicMock()
sys.modules['app.services.analytics_service'] = MagicMock()
sys.modules['main'] = MagicMock()

# Import the endpoint after mocking
from app.api.v1.endpoints.analytics import get_spending_patterns

@pytest.mark.asyncio
@patch('app.api.v1.endpoints.analytics.AnalyticsService')
async def test_get_spending_patterns_handles_invalid_data(MockAnalyticsService):
    """
    Tests that the endpoint correctly handles non-numeric data from the service
    by filtering it out before performing calculations, instead of crashing.
    """
    # Arrange
    mock_service_instance = MockAnalyticsService.return_value
    # Return a mix of valid and invalid data
    mock_service_instance.get_daily_spending = AsyncMock(return_value=[10, 20, 'a', None, 30.5])
    mock_service_instance.get_monthly_trends = AsyncMock(return_value={})

    mock_db = MagicMock()

    # Act: This will currently raise an exception due to the bug
    # The fix will make this code path return a valid response.
    response = await get_spending_patterns(
        days=90,
        current_user={"user_id": "test_user"},
        db=mock_db
    )

    # Assert that the calculation is based on filtered, valid data ([10, 20, 30.5])
    valid_data = [10, 20, 30.5]
    assert response.avg_daily_spending == pytest.approx(np.mean(valid_data))
    assert response.max_spending_day == pytest.approx(np.max(valid_data))
    assert response.min_spending_day == pytest.approx(np.min(valid_data))
    assert response.spending_volatility == pytest.approx(np.std(valid_data))
