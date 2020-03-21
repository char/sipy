from jinja2 import Template

def from_file(path: str) -> Template:
  with open(path) as f:
    return Template(f.read())
