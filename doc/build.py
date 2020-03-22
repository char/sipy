from sipy import Context


# Ad-hoc implementation of CSS minification
# TODO: Should this go in sipy proper?
def minify_css(css):
  import re

  minified_css = ""

  # Remove comments
  css = re.sub(r"/\*[\s\S]*?\*/", "", css)
  # Collapse multiple spaces
  css = re.sub(r"\s+", " ", css)
  # Replace #aabbcc with #abc
  css = re.sub(r"#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)", r"#\1\2\3\4", css)
  # Remove quotes from url()
  css = re.sub(r"url\(([\"'])([^)]*)\1\)", r"url(\2)", css)

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


def build(ctx: Context):
  templating = ctx.ext("templating")
  md = ctx.ext("markdown")
  highlighting = ctx.ext("highlighting")

  markdown_template = templating.from_file("build_src/markdown_template.html.j2")

  css_styles = open("build_src/styles.css").read()
  css_styles = minify_css(css_styles)

  for name in ctx.names:
    if name.endswith(".md"):
      content = ctx.read_text(name)
      metadata, content = md.parse_frontmatter(content)
      if not "title" in metadata:
        raise NameError(f"No title for page {name}")

      rendered_markdown = md.render(content, highlighting=highlighting)

      content = markdown_template.render(content=rendered_markdown, styles=css_styles, **metadata)
      ctx.write_text(name[:-len(".md")] + ".html", content)
    else:
      ctx.copy(name)
