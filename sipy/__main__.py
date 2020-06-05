from sipy import Context

from importlib.machinery import SourceFileLoader
from types import ModuleType
from pathlib import Path
import argparse
import sys
import os


SOURCE_DIRECTORY = "src"
OUTPUT_DIRECTORY = "out"


def build():
  """
    1. Set up the execution context
    2. Evaluate the target site's build.py (`pwd`/build.py)
    3. Call the target site's build.py build(ctx) function
  """

  working_directory = os.getcwd()
  sys.path.append(working_directory)

  target_site = ModuleType("build")
  SourceFileLoader("build", os.path.join(working_directory, "build.py")).exec_module(target_site)

  source_directory_name = target_site.source_directory_name or SOURCE_DIRECTORY
  output_directory_name = target_site.output_directory_name or OUTPUT_DIRECTORY

  source_directory = os.path.join(working_directory, source_directory_name)
  output_directory = os.path.join(working_directory, output_directory_name)

  ctx = Context(Path(source_directory), Path(output_directory))
  target_site.build(ctx)


def watch():
  from watchdog.observers import Observer
  from watchdog.events import FileSystemEventHandler

  class SipyWatcher(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
      if event.is_directory:
        return None

      if event.event_type in ["created", "modified"]:
        build()
        print()
  
  print("Watching for changes...")
  observer = Observer()
  observer.schedule(SipyWatcher(), SOURCE_DIRECTORY, recursive=True)
  observer.start()
  observer.join()


def main():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(title="actions", dest="action")

  subparsers.add_parser("build")
  subparsers.add_parser("serve")
  subparsers.add_parser("watch")

  args = parser.parse_args()

  if args.action == "serve":
    # I'm so sorry.

    import runpy, sys, os
    try:
      os.chdir("./" + OUTPUT_DIRECTORY)
      sys.argv = ["http.server"]
      runpy.run_module("http.server", {}, "__main__")
    except FileNotFoundError:
      print("Could not serve the out/ directory. Does it exist?", file=sys.stderr)
      exit(1)
  elif args.action == "watch":
    watch()
  else:
    build()


if __name__ == "__main__":
  main()
