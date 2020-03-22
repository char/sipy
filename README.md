# sipy

(si)tes with (py)thon. A scriptable static site generator.

## Usage

```shell
$ pip3 install git+https://github.com/half-cambodian-hacker-man/sipy-gen.git
$ cd <site>/
$ python3 -m sipy
```

## Requirements

- `misaka` and `jinja2` are both hard requirements.
- If `pygments` is installed, it can be used for syntax highlighting (using `markdown.render_markdown(..., highlighting=ctx.ext("highlighting"))).
