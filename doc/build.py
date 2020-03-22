from sipy import Context

# A simple markdown to HTML renderer

def build(ctx: Context):
  templating = ctx.ext("templating")
  md = ctx.ext("markdown")

  markdown_template = templating.from_file("build_src/markdown_template.html.j2")

  for name in ctx.names:
    if name.endswith(".md"):
      content = ctx.read_text(name)
      metadata, content = md.parse_frontmatter(content)

      if not "title" in metadata:
        raise NameError(f"No title for page {name}")

      content = markdown_template.render(content=md.render(content), **metadata)
      ctx.write_text(name[:-len(".md")] + ".html", content)
    else:
      ctx.copy(name)
