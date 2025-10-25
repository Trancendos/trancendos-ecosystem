"""API router for version 1 of the Luminous-MastermindAI API."""
from fastapi import APIRouter
from app.api.v1.endpoints import analytics, predictions, ai_insights

api_router = APIRouter()

api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["analytics"]
)

api_router.include_router(
    predictions.router,
    prefix="/predictions",
    tags=["predictions"]
)

api_router.include_router(
    ai_insights.router,
    prefix="/insights",
    tags=["ai-insights"]
)