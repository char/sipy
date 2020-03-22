from jinja2 import Template

def from_file(path: str) -> Template:
  with open(path) as f:
    return Template(f.read())


def from_string(source: str) -> Template:
  return Template(source)
