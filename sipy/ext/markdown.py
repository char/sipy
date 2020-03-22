import misaka
import re
import yaml

from typing import Tuple

MARKDOWN_EXTENSIONS = ('quote', 'fenced-code', 'footnotes', 'tables')
FRONTMATTER_BOUNDARY = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def parse_frontmatter(markdown: str, **default_metadata) -> Tuple[dict, str]:
  """Parses a markdown file's YAML frontmatter into the frontmatter metadata and the text contents."""

  metadata = default_metadata.copy()

  if FRONTMATTER_BOUNDARY.match(markdown):
    _, frontmatter, content = FRONTMATTER_BOUNDARY.split(markdown, 2)
    if frontmatter:
      fm_metadata = yaml.load(frontmatter, Loader=yaml.SafeLoader)
      if fm_metadata:
        metadata.update(fm_metadata)

    return metadata, content.strip()

  return metadata, markdown

def render(markdown: str) -> str:
  """Renders a markdown string to an embeddable HTML string."""

  return misaka.html(markdown, extensions=MARKDOWN_EXTENSIONS)
