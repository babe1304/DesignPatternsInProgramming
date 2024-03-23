from importlib import import_module
def myfactory(moduleName):
  return getattr(import_module(f'.{moduleName}', 'plugins'), moduleName)