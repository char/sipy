import re


def minify_css(css: str) -> str:
  """A simple implementation of CSS minification using regex substitutions."""

  # 1. We do some simple pre-processing of the CSS via regexes:

  css = re.sub(r"/\*[\s\S]*?\*/", "", css) # Remove comment
  css = re.sub(r"\s+", " ", css) # Collapse multiple spaces
  css = re.sub(r"#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)", r"#\1\2\3\4", css) # Replace #aabbcc with #abc

  # 2. Then, we emit each rule while performing some transformations.
  # We only want to emit rules with declarations.

  minified_css = ""

  for rule in re.findall(r"([^{]+){([^}]*)}", css):
    # Remove spaces around operators
    selectors = [re.sub(r"(?<=[\[\(>+=])\s+|\s+(?=[=~^$*|>+\]\)])", r"", selector.strip()) for selector in rule[0].split(",")]

    # Only emit rules with declarations
    properties = {}
    porder = [] # Use a list here since order of declarations matters
    for prop in re.findall("(.*?):(.*?)(;|$)", rule[1]):
      key = prop[0].strip().lower()
      if key not in porder: porder.append(key)
      properties[ key ] = prop[1].strip()

    if properties:
      minified_css += "%s{%s}" % (",".join(selectors), "".join(["%s:%s;" % (key, properties[key]) for key in porder])[:-1])

  return minified_css


def minify_html(html: str) -> str:
  """HTML minification using the 'htmlmin' package"""
  try:
    import htmlmin
    return htmlmin.minify(html)
  except ModuleNotFoundError:
    return html # TODO: Do some simple regexes or something
