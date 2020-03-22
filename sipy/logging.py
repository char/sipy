colorama_exists = False
try:
  import colorama
  colorama.init()
  colorama_exists = True
except ModuleNotFoundError:
  pass

def log(message, tag=None):
  if colorama_exists:
    from colorama import Fore, Style

    if tag:
      print(Fore.GREEN + Fore.LIGHTGREEN_EX + tag + Style.RESET_ALL, end=" ")
    print(message)
  else:
    if tag:
      print(tag, end=" ")
    print(message)
