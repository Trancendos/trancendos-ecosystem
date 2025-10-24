import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime

from app.services.ai_service import AIService

@pytest.fixture
def mock_transactions():
    """Fixture to provide mock transaction data."""
    return [
        {'id': 1, 'amount': 100.0, 'category': 'Groceries', 'transaction_date': datetime(2023, 1, 1, 10, 0)},
        {'id': 2, 'amount': 50.0, 'category': 'Transport', 'transaction_date': datetime(2023, 1, 2, 12, 0)},
        {'id': 3, 'amount': 200.0, 'category': 'Groceries', 'transaction_date': datetime(2023, 1, 3, 14, 0)},
        {'id': 4, 'amount': 75.0, 'category': 'Entertainment', 'transaction_date': datetime(2023, 1, 4, 16, 0)},
        {'id': 5, 'amount': 120.0, 'category': 'Utilities', 'transaction_date': datetime(2023, 1, 5, 18, 0)},
    ]

@pytest.fixture
def ai_service():
    """Fixture to create an AIService instance with mocked models."""
    with patch('joblib.load') as mock_joblib_load, \
         patch('joblib.dump') as mock_joblib_dump, \
         patch('os.path.exists', return_value=True):

        service = AIService()
        # Mock the models to avoid actual loading/training
        service.spending_model = MagicMock()
        service.anomaly_detector = MagicMock()
        service.scaler = MagicMock()
        return service

def test_prepare_features(ai_service, mock_transactions):
    """Test the feature preparation method."""
    df = ai_service.prepare_features(mock_transactions)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'day_of_week' in df.columns
    assert 'rolling_mean_7d' in df.columns
    assert 'category_encoded' in df.columns
    assert df['category_encoded'].nunique() == 4  # 4 unique categories

def test_prepare_features_empty(ai_service):
    """Test feature preparation with no transactions."""
    df = ai_service.prepare_features([])
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_generate_insights(ai_service, mock_transactions):
    """Test the insight generation method."""
    # Add more data to test trends
    transactions = mock_transactions + [
        {'id': 6, 'amount': 150.0, 'category': 'Groceries', 'transaction_date': datetime(2023, 2, 1)},
        {'id': 7, 'amount': 80.0, 'category': 'Transport', 'transaction_date': datetime(2023, 2, 5)},
    ]

    insights = ai_service.generate_insights(transactions)

    assert "spending_trends" in insights
    assert "savings_opportunities" in insights

    # Check spending trend insight
    assert len(insights["spending_trends"]) > 0
    assert "Your spending is" in insights["spending_trends"][0]["insight"]

    # Check savings opportunities
    assert len(insights["savings_opportunities"]) > 0
    assert insights["savings_opportunities"][0]["category"] == "Groceries"

def test_generate_insights_empty(ai_service):
    """Test insight generation with no transactions."""
    insights = ai_service.generate_insights([])
    assert not insights["spending_trends"]
    assert not insights["savings_opportunities"]

@patch('app.services.ai_service.RandomForestRegressor')
def test_train_spending_predictor(mock_rf, ai_service, mock_transactions):
    """Test the spending predictor training method."""
    # Mock the scaler to return a simple array
    ai_service.scaler.fit_transform.return_value = np.random.rand(len(mock_transactions) - 1, 7)
    ai_service.scaler.transform.return_value = np.random.rand(1, 7)

    # Make the transaction list longer to pass the minimum data check
    long_transactions = mock_transactions * 3

    result = ai_service.train_spending_predictor(long_transactions)

    assert result["success"]
    assert "train_score" in result
    assert "test_score" in result
    mock_rf.assert_called_once()
    ai_service.spending_model.fit.assert_called_once()

def test_predict_spending_no_model(ai_service):
    """Test spending prediction when the model is not trained."""
    ai_service.spending_model = None
    result = ai_service.predict_spending({})
    assert not result["success"]
    assert "Model not trained" in result["message"]

@patch('numpy.std')
def test_predict_spending_success(mock_np_std, ai_service):
    """Test a successful spending prediction."""
    mock_np_std.return_value = 0.5  # Mock standard deviation for confidence

    ai_service.spending_model.predict.return_value = [123.45]
    ai_service.spending_model.estimators_ = [MagicMock()] # Mock estimators
    ai_service.scaler.transform.return_value = np.array([[0.1, 0.2]])

    features = {'day_of_week': 3, 'month': 5}
    result = ai_service.predict_spending(features)

    assert result["success"]
    assert result["predicted_amount"] == 123.45

@patch('app.services.ai_service.IsolationForest')
def test_train_anomaly_detector(mock_if, ai_service, mock_transactions):
    """Test the anomaly detector training method."""
    ai_service.scaler.fit_transform.return_value = np.random.rand(len(mock_transactions), 8)

    # Mock the anomaly detector to return some anomalies
    mock_detector_instance = mock_if.return_value
    mock_detector_instance.predict.return_value = np.array([-1, 1, 1, 1, 1] * 5) # 5 anomalies
    mock_detector_instance.decision_function.return_value = np.random.rand(25)

    # Make transactions long enough
    long_transactions = mock_transactions * 5

    result = ai_service.train_anomaly_detector(long_transactions)

    assert result["success"]
    assert "anomalies_detected" in result
    assert result["anomalies_detected"] == 5
    mock_if.assert_called_once()
    ai_service.anomaly_detector.fit.assert_called_once()

def test_detect_anomalies_no_model(ai_service):
    """Test anomaly detection when the model is not trained."""
    ai_service.anomaly_detector = None
    result = ai_service.detect_anomalies([])
    assert result == []

def test_detect_anomalies_success(ai_service, mock_transactions):
    """Test a successful anomaly detection."""
    ai_service.anomaly_detector.predict.return_value = [-1, 1, 1, -1, 1]  # -1 is anomaly
    ai_service.anomaly_detector.decision_function.return_value = [-0.6, 0.1, 0.2, -0.8, 0.3]
    ai_service.scaler.transform.return_value = np.random.rand(len(mock_transactions), 8)

    anomalies = ai_service.detect_anomalies(mock_transactions)

    assert len(anomalies) == 2
    assert anomalies[0]["transaction_id"] == 1
    assert anomalies[1]["transaction_id"] == 4
    assert anomalies[0]["severity"] == "high"
