---
title: sipy - A scriptable static site generator.
---

# sipy: A scriptable static site generator.

`sipy` is a static site generator, where configuration is done by writing Python.

## Install

`sipy` can be easily installed using `pip`:

```shell
$ pip3 install "git+https://github.com/half-cambodian-hacker-man/sipy.git"
```

## Getting Started

To create a site using `sipy`, all you need is a folder structure like so:

```
├── build.py
└── src
    └── ...
```

As an example, we can create a simple markdown processor by filling in `build.py` like so:

```python
def build(ctx):
  # We use the 'markdown' and 'templating' extensions
  md = ctx.ext("markdown")
  templating = ctx.ext("templating") # Templating is done using Jinja2

  # Also available: templating.from_file("./build_src/template.html.j2") relative to build.py
  template = templating.from_string(r"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>{{ title }}</title>
      </head>

      <body>
        {{ content }}
      </body>
    </html>
  """)

  # For each file, render markdown if it's a '.md' file,
  # but otherwise just copy it to the output directory.
  for name in ctx.names:
    if name.endswith(".md"):
      # 1. Read the contents of the file
      file_contents = ctx.read_text(name)
      
      # 2. Parse the frontmatter to get a custom 'title' attribute for the page.
      # We use the string "[unnamed page]" as a placeholder if 'title' is not defined
      frontmatter, content = md.parse_frontmatter(file_contents, title="[unnamed page]")

      # 3. Render the markdown using the markdown extension.
      # Note: We use 'content' instead of 'file_contents' here,
      # so that we don't include the raw front matter.
      rendered_markdown = md.render(content)

      # 4. Use our defined template to render out the page.
      # The 'content' variable is defined by the rendered markdown,
      # and all the front matter variables are passed in. (We care about 'title')
      rendered_page = template.render(content=rendered_markdown, **frontmatter)

      # 5. Write out the rendered page as a .html file.
      # We use a simple replace() here, but you can put anything here.
      # Perhaps something like:
      # 
      #   base_name = strip_extension(name, ".md")
      #   f"{base_name}.html" if base_name == "index" \
      #   else f"{base_name}/index.html"
      # 
      ctx.write_text(name.replace(".md", ".html"), rendered_page)
    else:
      ctx.copy(name)
```

Then, populate `src/index.md` with any content you want:

```md
---
title: My Markdown Page
---

# Hello, world!

This is a test of markdown with [sipy](https://github.com/half-cambodian-hacker-man/sipy).
```

And simply run:

```shell
$ sipy # Build the site
$ sipy serve # Start a static web server (equivalent to python3 -m http.server)
```
