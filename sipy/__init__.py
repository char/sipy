from dataclasses import dataclass
from pathlib import Path
from os import makedirs
from os.path import normpath


@dataclass
class Context:
  source_directory: Path
  output_directory: Path


  def _join(self, directory: Path, name: str) -> str:
    return str(directory.joinpath(name).resolve())


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

    try:
      makedirs(normpath(target + "/.."))
    except FileExistsError:
      pass

    with open(target, "w") as f:
      f.write(data)


  def write_binary(self, name: str, data: bytes):
    """Write binary data to a file in the output directory."""

    target = self._join(self.output_directory, name)
    
    try:
      makedirs(normpath(target + "/.."))
    except FileExistsError:
      pass

    with open(target, "wb") as f:
      f.write(data)
