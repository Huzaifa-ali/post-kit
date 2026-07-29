"""Analytics module data models."""

from pydantic import BaseModel


class ImportResponse(BaseModel):
    """Response after importing analytics data."""
    rows_imported: int
    columns: list[str]
    filename: str


class DashboardData(BaseModel):
    """Aggregated analytics dashboard data."""
    total_posts: int
    columns: list[str]
    data: list[dict]
