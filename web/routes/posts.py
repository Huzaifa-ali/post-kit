"""Posts routes — read-only views for generated posts."""

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from .helpers import templates, is_setup_complete
from ..services import db

router = APIRouter()


@router.get("/posts")
async def posts_page(request: Request):
    if not is_setup_complete():
        return RedirectResponse(url="/onboarding", status_code=302)

    all_posts = await db.get_all_posts()
    total = await db.get_posts_count()

    return templates.TemplateResponse(request, "posts.html", {
        "posts": all_posts,
        "total": total,
        "page": "posts",
    })


@router.get("/posts/{post_id}")
async def view_post(request: Request, post_id: int):
    post = await db.get_post(post_id)
    if not post:
        return RedirectResponse(url="/posts", status_code=302)
    return templates.TemplateResponse(request, "post_view.html", {
        "post": post,
        "page": "posts",
    })


@router.post("/posts/{post_id}/delete")
async def delete_post(post_id: int):
    await db.delete_post(post_id)
    return RedirectResponse(url="/posts", status_code=302)
