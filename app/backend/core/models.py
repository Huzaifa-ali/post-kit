"""Shared models and enums used across the app."""

from enum import StrEnum


class PostStatus(StrEnum):
    IDEA = "idea"
    SCOUTED = "scouted"
    DRAFTING = "drafting"
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"
