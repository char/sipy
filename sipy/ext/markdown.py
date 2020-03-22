from typing import Tuple

import misaka
import yaml
import re

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

def render(markdown: str, highlighting = None) -> str:
  """Renders a markdown string to an embeddable HTML string."""

  if highlighting:
    html_and_highlight = misaka.Markdown(
      HighlightingRenderer(highlighting),
      extensions=MARKDOWN_EXTENSIONS
    )

    return html_and_highlight(markdown)

  return misaka.html(markdown, extensions=MARKDOWN_EXTENSIONS)

class HighlightingRenderer(misaka.HtmlRenderer):
  def __init__(self, highlighting):
    super().__init__()
    self.highlighting = highlighting

  def blockcode(self, text, lang):
    return "<pre><code class=\"hl\">{}</pre></code>".format(self.highlighting.highlight(text, lang))
