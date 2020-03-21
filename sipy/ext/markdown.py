import misaka

markdown_extensions = ('quote', 'fenced-code', 'footnotes', 'tables')

def render(markdown: str) -> str:
  """Renders a markdown string to an embeddable HTML string."""

  return misaka.html(markdown, extensions=markdown_extensions)
