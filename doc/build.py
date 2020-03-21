from sipy import Context

# A simple blog

def build(ctx: Context):
  templating = ctx.ext("templating")
  md = ctx.ext("markdown")

  blog_post_template = templating.from_file("build_src/blog_post.html.j2")

  for name in ctx.names:
    if name.endswith(".md"):
      content = md.render(ctx.read_text(name))
      content = blog_post_template.render(content=content)

      ctx.write_text(name[:-len(".md")] + ".html", content)
    else:
      ctx.copy(name)

