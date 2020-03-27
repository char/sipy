from importlib.machinery import SourceFileLoader
from types import ModuleType

def run(ctx, name, out_name=None, *args, **kwargs):
  out_name = out_name or name[:3]

  module_name = "__direct_render__." + name
  loader = SourceFileLoader(module_name, ctx.source_directory.joinpath(name).resolve())
  script_module = ModuleType(module_name)
  loader.exec_module(script_module)

  if "render_text" in dir(script_module):
    ctx.write_text(out_name, script_module.render_text(ctx, *args, **kwargs))
  elif "render_data" in dir(script_module):
    ctx.write_data(out_name, script_module.render_data(ctx, *args, **kwargs))
  else:
    raise Exception("Cannot run direct script: " + name + ". Is render_text or render_data defined?")
