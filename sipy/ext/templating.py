from jinja2 import Environment, BaseLoader, FileSystemLoader


loader = BaseLoader()
Template = lambda source: Environment(loader=loader).from_string(source)


def set_base_directory(path: str):
  global loader; loader = FileSystemLoader(path)


def from_file(path: str) -> Template:
  with open(path) as f:
    return Template(f.read())


def from_string(source: str) -> Template:
  return Template(source)
