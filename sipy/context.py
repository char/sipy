from sipy.logging import log

from dataclasses import dataclass
from pathlib import Path
from os import makedirs
from os.path import normpath
from importlib import import_module

@dataclass
class FileAccessContext:
  source_directory: Path
  output_directory: Path


  def _join(self, directory: Path, name: str) -> str:
    return str(directory.joinpath(name).resolve())


  def _create_parent_directories(self, path: str):
    parent_directory = self._join(Path(path), "..")

    try:
      makedirs(parent_directory)
    except FileExistsError:
      pass


  @property
  def names(self):
    """List the files in the source directory, recursively."""

    for p in self.source_directory.rglob("*"):
      if p.is_file():
        yield str(p.relative_to(self.source_directory))


  def read_text(self, name: str) -> str:
    """Read text from a file in the source directory, encoded with UTF-8."""

    with open(self._join(self.source_directory, name), "r") as f:
      return f.read()
    
    return None


  def read_data(self, name: str) -> bytes:
    """Read binary data from a file in the source directory."""

    with open(self._join(self.source_directory, name), "rb") as f:
      return f.read()
    
    return None


  def write_text(self, name: str, data: str):
    """Write text to a file in the output directory, encoded with UTF-8."""

    target = self._join(self.output_directory, name)
    self._create_parent_directories(target)

    with open(target, "w") as f:
      f.write(data)
    
    log(name, tag="[+]")


  def write_data(self, name: str, data: bytes):
    """Write binary data to a file in the output directory."""

    target = self._join(self.output_directory, name)
    self._create_parent_directories(target)

    with open(target, "wb") as f:
      f.write(data)

    log(name, tag="[+]")


  def copy(self, name: str):
    """Copy a file from the source directory to the output directory."""

    self.write_data(name, self.read_data(name))


class ExtensionAccessContext:
  def __init__(self):
    self.extension_cache = {}


  def ext(self, identifier: str):
    # TODO: Caching
    if identifier in self.extension_cache:
      return self.extension_cache[identifier]

    try:
      extension = import_module("sipy.ext." + identifier)
      self.extension_cache[identifier] = extension
      return extension
    except ModuleNotFoundError:
      return None


class Context(FileAccessContext, ExtensionAccessContext):
  def __init__(self, source_directory, output_directory):
    FileAccessContext.__init__(self, source_directory, output_directory)
    ExtensionAccessContext.__init__(self)
