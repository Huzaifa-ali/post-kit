"""How It Works route — explains the workflow for new users."""

from fastapi import APIRouter, Request

from .helpers import templates

router = APIRouter()


@router.get("/how-it-works")
async def how_it_works_page(request: Request):
    return templates.TemplateResponse(request, "how_it_works.html", {"page": "how"})
