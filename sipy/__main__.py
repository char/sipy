from sipy import Context

from importlib.machinery import SourceFileLoader
from types import ModuleType
from pathlib import Path
import argparse
import sys
import os


def build():
  """
    1. Set up the execution context
    2. Evaluate the target site's build.py (`pwd`/build.py)
    3. Call the target site's build.py build(ctx) function
  """

  working_directory = os.getcwd()
  sys.path.append(working_directory)

  source_directory = os.path.join(working_directory, "src")
  output_directory = os.path.join(working_directory, "out")

  ctx = Context(Path(source_directory), Path(output_directory))

  target_site = ModuleType("target_site.build")
  SourceFileLoader("target_site.build", os.path.join(working_directory, "build.py")).exec_module(target_site)
  target_site.build(ctx)


def main():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(title="actions", dest="action")

  subparsers.add_parser("build")
  subparsers.add_parser("serve")

  args = parser.parse_args()

  if args.action == "serve":
    # I'm so sorry.

    import runpy, sys, os
    try:
      os.chdir("./out")
      sys.argv = ["http.server"]
      runpy.run_module("http.server", {}, "__main__")
    except FileNotFoundError:
      print("Could not serve the out/ directory. Does it exist?", file=sys.stderr)
      exit(1)
  else:
    build()


if __name__ == "__main__":
  main()
