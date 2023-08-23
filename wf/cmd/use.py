import os

def single(cmd, args, funs, vars, consts, exec_stack, exec, pval):
  if len(args) != 1:
    print("Invalid arguments for \"use\" command!")
    return False

  x = args[0]

  std = consts["__stdlib_path"]

  if x.startswith("std/"):
    x = os.path.join(std, x[4:])

  if not x.endswith(".wf"):
    x += ".wf"

  if x in consts["__path"]:
    return True

  if not os.path.isfile(x):
    print("Cannot import \"" + x + "\"!")
    return False

  with open(x, "r") as f:
    exec(0, f.read().split("\n"))

  consts["__path"].append(x)

  return True
