from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.transaction import Transaction
from app.schemas.analytics import (
    AnalyticsResponse,
    SpendingPatternResponse,
    CategoryAnalysisResponse,
    TrendAnalysisResponse
)
from app.services.analytics_service import AnalyticsService
from main import get_current_user

router = APIRouter()

@router.get("/overview", response_model=AnalyticsResponse)
async def get_analytics_overview(
    days: int = 30,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive analytics overview for the user.

    Args:
        days (int, optional): The number of days to look back for analytics. Defaults to 30.
        current_user (dict, optional): The current authenticated user. Defaults to Depends(get_current_user).
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the analytics calculation fails.

    Returns:
        AnalyticsResponse: An object containing the analytics overview.
    """
    analytics_service = AnalyticsService(db)
    
    try:
        user_id = current_user["user_id"]
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get basic metrics
        total_income = await analytics_service.get_total_income(user_id, start_date, end_date)
        total_expenses = await analytics_service.get_total_expenses(user_id, start_date, end_date)
        net_savings = total_income - total_expenses
        
        # Get transaction counts
        transaction_count = await analytics_service.get_transaction_count(user_id, start_date, end_date)
        
        # Calculate savings rate
        savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0
        
        # Get top spending categories
        top_categories = await analytics_service.get_top_spending_categories(user_id, start_date, end_date)
        
        return AnalyticsResponse(
            period_days=days,
            total_income=float(total_income),
            total_expenses=float(total_expenses),
            net_savings=float(net_savings),
            savings_rate=float(savings_rate),
            transaction_count=transaction_count,
            top_categories=top_categories,
            generated_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics calculation failed: {str(e)}")

@router.get("/spending-patterns", response_model=SpendingPatternResponse)
async def get_spending_patterns(
    days: int = 90,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Analyze spending patterns and identify trends.

    Args:
        days (int, optional): The number of days to look back for spending patterns. Defaults to 90.
        current_user (dict, optional): The current authenticated user. Defaults to Depends(get_current_user).
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the pattern analysis fails.

    Returns:
        SpendingPatternResponse: An object containing the spending pattern analysis.
    """
    analytics_service = AnalyticsService(db)
    
    try:
        user_id = current_user["user_id"]
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get daily spending data
        daily_spending = await analytics_service.get_daily_spending(user_id, start_date, end_date)
        
        # Calculate patterns
        avg_daily_spending = np.mean(daily_spending) if daily_spending else 0
        max_spending_day = np.max(daily_spending) if daily_spending else 0
        min_spending_day = np.min(daily_spending) if daily_spending else 0
        spending_volatility = np.std(daily_spending) if len(daily_spending) > 1 else 0
        
        # Get monthly trends
        monthly_trends = await analytics_service.get_monthly_trends(user_id, start_date, end_date)
        
        return SpendingPatternResponse(
            period_days=days,
            avg_daily_spending=float(avg_daily_spending),
            max_spending_day=float(max_spending_day),
            min_spending_day=float(min_spending_day),
            spending_volatility=float(spending_volatility),
            monthly_trends=monthly_trends,
            generated_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pattern analysis failed: {str(e)}")

@router.get("/category-analysis", response_model=CategoryAnalysisResponse)
async def get_category_analysis(
    category: Optional[str] = None,
    days: int = 30,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Detailed analysis of spending by category.

    Args:
        category (Optional[str], optional): The category to analyze. If None, all categories are analyzed. Defaults to None.
        days (int, optional): The number of days to look back for category analysis. Defaults to 30.
        current_user (dict, optional): The current authenticated user. Defaults to Depends(get_current_user).
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the category analysis fails.

    Returns:
        CategoryAnalysisResponse: An object containing the category analysis.
    """
    analytics_service = AnalyticsService(db)
    
    try:
        user_id = current_user["user_id"]
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        if category:
            # Analyze specific category
            category_data = await analytics_service.analyze_category(user_id, category, start_date, end_date)
        else:
            # Analyze all categories
            category_data = await analytics_service.analyze_all_categories(user_id, start_date, end_date)
        
        return CategoryAnalysisResponse(
            period_days=days,
            category=category,
            analysis_data=category_data,
            generated_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Category analysis failed: {str(e)}")

@router.get("/trends", response_model=TrendAnalysisResponse)
async def get_trend_analysis(
    trend_type: str = "spending",
    period: str = "monthly",  # daily, weekly, monthly
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Analyze financial trends over time.

    Args:
        trend_type (str, optional): The type of trend to analyze. Defaults to "spending".
        period (str, optional): The period to analyze the trend over. Defaults to "monthly".
        current_user (dict, optional): The current authenticated user. Defaults to Depends(get_current_user).
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the trend analysis fails.

    Returns:
        TrendAnalysisResponse: An object containing the trend analysis.
    """
    analytics_service = AnalyticsService(db)
    
    try:
        user_id = current_user["user_id"]
        
        # Get trend data based on type and period
        trend_data = await analytics_service.get_trend_analysis(
            user_id=user_id,
            trend_type=trend_type,
            period=period
        )
        
        return TrendAnalysisResponse(
            trend_type=trend_type,
            period=period,
            trend_data=trend_data,
            generated_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")