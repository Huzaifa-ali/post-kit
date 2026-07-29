"""Credits module routes — plan and usage."""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.modules.credits import service

router = APIRouter(prefix="/api/credits", tags=["credits"])


class UpdatePlanRequest(BaseModel):
    name: str
    limit: int
    period: str = "monthly"


@router.get("")
async def get_credits() -> dict:
    """Get current plan and usage."""
    return service.get_credits()


@router.put("/plan")
async def update_plan(request: UpdatePlanRequest) -> dict:
    """Update plan info."""
    return service.update_plan(request.name, request.limit, request.period)
