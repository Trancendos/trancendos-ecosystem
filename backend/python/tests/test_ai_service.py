import pytest
from datetime import datetime
from unittest.mock import MagicMock
from backend.python.app.services.ai_service import AIService

class MockSeries:
    def __init__(self, data):
        self.data = data
        self.iloc = self

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)

@pytest.fixture
def mock_dependencies(mocker):
    mocker.patch('backend.python.app.services.ai_service.pd', MagicMock())
    mocker.patch('backend.python.app.services.ai_service.np', MagicMock())
    mocker.patch('backend.python.app.services.ai_service.joblib', MagicMock())

    mock_sklearn = MagicMock()
    mocker.patch('backend.python.app.services.ai_service.RandomForestRegressor', mock_sklearn)
    mocker.patch('backend.python.app.services.ai_service.IsolationForest', mock_sklearn)
    mocker.patch('backend.python.app.services.ai_service.StandardScaler', mock_sklearn)
    mocker.patch('backend.python.app.services.ai_service.train_test_split', mock_sklearn)

@pytest.fixture
def mock_pandas_for_insights(mocker):
    mock_pd = mocker.patch('backend.python.app.services.ai_service.pd')
    mock_df = MagicMock()
    mock_pd.DataFrame.return_value = mock_df

    # Mock the result of the groupby(...).sum() chain
    mock_monthly_spending = MockSeries([0, 50])  # Prev month 0, current month 50
    mock_df.groupby.return_value.__getitem__.return_value.sum.return_value = mock_monthly_spending

    return mock_pd

def test_generate_insights_division_by_zero(mock_dependencies, mock_pandas_for_insights):
    ai_service = AIService()
    transactions = [
        {"transaction_date": datetime(2023, 1, 15), "amount": 0, "category": "Groceries"},
        {"transaction_date": datetime(2023, 2, 5), "amount": 50, "category": "Transport"},
    ]
    insights = ai_service.generate_insights(transactions)
    assert "spending_trends" in insights
    assert len(insights["spending_trends"]) == 1
    assert insights["spending_trends"][0]["change_percentage"] == 100.0
