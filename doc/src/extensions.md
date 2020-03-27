---
title: Extensions - sipy
---

# Extensions

The core of `sipy` only provides a select number of primitives:

- `read_text` and `read_data`, to read from the `src/` directory.
- `write_text` and `write_data`, to write to the `out/` directory.

But, most static sites need:

- Templates for a consistent feel, with injected content
- A more ergonomic way of writing content than plain HTML
- Optimization of site output

## Templating

`sipy` uses [Jinja2](https://jinja.palletsprojects.com/) for templating. To use it in a build script, simply use either of the `templating.from_file` or `templating.from_string` methods:

```python
def build(ctx):
  templating = ctx.ext("templating")
  my_template = templating.from_file("./build_src/my_template.html.j2")
  # my_template.html.j2: <html><body>{{ content }}</body></html>

  # Later...
  my_template.render(content="<p>Hello, world!</p>")
```

## Markdown

[Markdown](https://commonmark.org/) is a simple markup language.

You can use markdown with `sipy` with the `markdown` extension's `parse_frontmatter` and `render` methods.

```python
def build(ctx):
  md = ctx.ext("markdown")

  markdown_file_contents = ctx.read_text("my_document.md")
  # my_document.md:
  # ---
  # name: document
  # ---
  # 
  # # Markdown
  # 
  # Hello, world!

  metadata, content = md.parse_frontmatter(markdown_file_contents)
  # metadata is a dict, content is a string
  content = md.render(content)

  ctx.write_file(metadata["name"] + ".html", content)
  # >>> [+] document.html
```

## Highlighting

Syntax highlighting is done with `pygments`.

**Note:** `pygments` is **not** defined as a dependency of `sipy`. You will have to install it manually. If `pygments` is not present, `ctx.ext("highlighting")` will return `None`.

The highlighting extension can be used in two ways:

### Direct Usage

```python
def build(ctx):
  highlighting = ctx.ext("highlighting")
  if highlighting is None:
    raise Exception("Install pygments!")

  python_code = '''\
def main():
  print("Hello, world!")

if __name__ == "__main__":
  main()\
'''

  highlighted_code = highlighting.highlight(python_code, "python")
  ctx.write_text("highlighted.html", """
    <html>
      <head>
        <style>
          /* Syntax highlighting styles */
          .hl {
            display: block;
            overflow-x: auto;
            
            background: black;
            color: white;
          }
          .hl .k, .hl .gh { /* Keywords */
            font-weight: bold;
            color: hsl(61, 86%, 68%);
          }
          .hl .c1 { color: hsl(248, 7%, 56%); } /* Comments */
          .hl .nb, .hl .nt { color: hsl(147, 68%, 72%); } /* Builtins */
          .hl .s1, .hl .s2 { color: hsl(167, 100%, 74%); } /* Strings */
          .hl .mi { color: hsl(202, 91%, 67%) } /* Integers */
        </style>
      </head>

      <body>
        <pre><code class="hl">{}</code></pre>
      </body>
    </html>
  """.format(highlighted_code))
```

### Usage with Markdown

In Markdown, a fenced code block can have a language attached to it.

By passing in the highlighting extension through `markdown.render(..., highlighting=ctx.ext("highlighting"))`, the Markdown renderer will automatically highlight the syntax in language-tagged code blocks.

```python
def build(ctx):
  md = ctx.ext("markdown")
  hl = ctx.ext("highlighting")
  tplt = ctx.ext("templating")

  content = ctx.read_text("highlighting.md")
  metadata, content = md.parse_frontmatter(content)
  content = md.render(content)

  template = tplt.from_string("""
    <html>
      <head>
        <style>
          /* Syntax highlighting styles */
          .hl {
            display: block;
            overflow-x: auto;
            
            background: black;
            color: white;
          }
          .hl .k, .hl .gh { /* Keywords */
            font-weight: bold;
            color: hsl(61, 86%, 68%);
          }
          .hl .c1 { color: hsl(248, 7%, 56%); } /* Comments */
          .hl .nb, .hl .nt { color: hsl(147, 68%, 72%); } /* Builtins */
          .hl .s1, .hl .s2 { color: hsl(167, 100%, 74%); } /* Strings */
          .hl .mi { color: hsl(202, 91%, 67%) } /* Integers */
        </style>
      </head>
      <body>
        {{ content }}
      </body>
    </html>
  """)

  # 'content' is a highlighted <pre><code>...</code></pre> element
  ctx.write_text("highlighting.html", template.render(content=content))
```

## Minification

Minification provides two methods: `minify_css` and `minify_html`.

**Note:** To use `minify_html`, you need the `htmlmin` package. It will silently fail over to the raw HTML otherwise.

```python
def build(ctx):
  mini = ctx.ext("minification")
  tplt = ctx.ext("templating")

  template = tplt.from_string("""
    <html>
      <head>
        <style>{{ styles }}</style>
      </head>
      <body>
        {{ content }}
      </body>
    </html>
  """)

  styles = ctx.read_text("styles.css")
  styles = mini.minify_css(styles)


  content = """
    <p>Hello, world!</p>
    <p>This is my minified HTML document.</p>
  """

  output_html = template.render(content=content, styles=styles)
  output_html = mini.minify_html(output_html)

  ctx.write_text("min.html", output_html)
```
