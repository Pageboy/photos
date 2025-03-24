import logging

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import PrefixedLogger, event_priority
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext


def on_config(config: MkDocsConfig):

    # Reset state for mkdocs serve changes
    StateHandler.is_sorted = False


# Run after the Blog plugin
@event_priority(-105)
def on_page_context(
    context: TemplateContext, *, page: Page, config: MkDocsConfig, nav: Navigation
):

    # Quit early if already sorted
    if StateHandler.is_sorted:
        return

    posts = context.get("posts")

    # Ignore pages without posts
    if not posts:
        return

    # Sort in-place, this affects the posts globally for all pages that use them
    # Most recently updated at the top
    posts.sort(key=lambda post: post.config.date.updated, reverse=True)

    StateHandler.is_sorted = True
    LOG.info("Blog posts sorted by updated")


class StateHandler:
    is_sorted: bool = False


HOOK_NAME: str = "sort_blog_updated"
"""Name of this hook. Used in logging."""

LOG: PrefixedLogger = PrefixedLogger(
    HOOK_NAME, logging.getLogger(f"mkdocs.hooks.{HOOK_NAME}")
)
"""Logger instance for this hook."""
