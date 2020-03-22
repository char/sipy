import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, ClassNotFound

DEFAULT_FORMATTER = HtmlFormatter(nowrap=True)


def highlight(code, lang, formatter=DEFAULT_FORMATTER):
  try:
    lexer = get_lexer_by_name(lang, stripall=True)

    if lexer:
      return pygments.highlight(code, lexer, formatter)
  except ClassNotFound:
    pass

  return code
