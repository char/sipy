from sipy import Context
from importlib.machinery import SourceFileLoader
import os
from pathlib import Path

def main():
  """
    1. Set up the execution context
    2. Evaluate the target site's build.py (`pwd`/build.py)
    3. Call the target site's build.py build(ctx) function
  """

  working_directory = os.getcwd()

  source_directory = os.path.join(working_directory, "src")
  output_directory = os.path.join(working_directory, "out")

  ctx = Context(Path(source_directory), Path(output_directory))

  target_site = SourceFileLoader("target_site", os.path.join(working_directory, "build.py")).load_module()
  target_site.build(ctx)


if __name__ == "__main__":
  main()
