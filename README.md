# sipy

(si)tes with (py)thon. A scriptable static site generator.

## Usage

```shell
$ pip3 install git+https://github.com/half-cambodian-hacker-man/sipy.git
$ cd <site>/
$ sipy
```

## Requirements

- `misaka`, and `PyYAML` are required for the `markdown` extension. These are hard requirements, and are installed transitively.
- `jinja2` is required for the `templating` extension. This is a hard requirement, and is installed transitively.
- If `pygments` is installed, it can be used for syntax highlighting (using `markdown.render_markdown(..., highlighting=ctx.ext("highlighting"))`).
  - If `pygments` is not installed, `ctx.ext("highlighting")` will be `None` and no highlighting will occur.
