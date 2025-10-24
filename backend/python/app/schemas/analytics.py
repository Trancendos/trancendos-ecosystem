from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class AnalyticsResponse(BaseModel):
    period_days: int
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate: float
    transaction_count: int
    top_categories: List[Dict[str, Any]]
    generated_at: datetime

class SpendingPatternResponse(BaseModel):
    period_days: int
    avg_daily_spending: float
    max_spending_day: float
    min_spending_day: float
    spending_volatility: float
    monthly_trends: Dict[str, Any]
    generated_at: datetime

class CategoryAnalysisResponse(BaseModel):
    period_days: int
    category: Optional[str]
    analysis_data: Dict[str, Any]
    generated_at: datetime

class TrendAnalysisResponse(BaseModel):
    trend_type: str
    period: str
    trend_data: List[Dict[str, Any]]
    generated_at: datetime
