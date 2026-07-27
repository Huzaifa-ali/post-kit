"""
save_post.py — Helper the CLI agent uses to push posts to the database.

Usage:
    python save_post.py --topic "..." --content "..." --platform linkedin --image-prompt "..." --video-prompt "..." --references "..." --hashtags "..." --cli kiro
"""

import asyncio
import argparse
from web.services.db import init_db, save_post


async def main():
    parser = argparse.ArgumentParser(description="Save a post to the post-kit database")
    parser.add_argument("--topic", required=True, help="Post topic")
    parser.add_argument("--content", required=True, help="Post content")
    parser.add_argument("--platform", default="linkedin", help="Platform (linkedin, twitter, instagram, reddit)")
    parser.add_argument("--type", default="opinion", help="Post type (opinion, news, educational, story, meme)")
    parser.add_argument("--hashtags", default=None, help="Hashtags string")
    parser.add_argument("--image-prompt", default=None, help="Image generation prompt")
    parser.add_argument("--video-prompt", default=None, help="Video generation prompt (Veo3, 30sec)")
    parser.add_argument("--references", default=None, help="Sources/references used")
    parser.add_argument("--cli", default="kiro", help="CLI tool used (kiro, claude, cursor, etc.)")
    parser.add_argument("--saved-to", default=None, help="Filesystem path where post was saved")

    args = parser.parse_args()

    await init_db()
    post_id = await save_post(
        topic=args.topic,
        content=args.content,
        platform=args.platform,
        post_type=args.type,
        hashtags=args.hashtags,
        image_prompt=args.image_prompt,
        video_prompt=args.video_prompt,
        references_used=args.references,
        cli_tool=args.cli,
        saved_to=args.saved_to,
    )
    print(f"Saved post #{post_id}")


if __name__ == "__main__":
    asyncio.run(main())
