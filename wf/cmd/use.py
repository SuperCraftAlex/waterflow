import os

def single(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 1:
    err("Invalid arguments for \"use\" command!")
    return False

  x = args[0]
  ox = x

  std = consts["__stdlib_path"]

  if x.startswith("std/"):
    x = os.path.join(std, x[4:])

  if not x.endswith(".wf"):
    x += ".wf"

  if x in consts["__path"]:
    return True

  if not os.path.isfile(x):
    err("Cannot import \"" + x + "\"!")
    return False

  with open(x, "r") as f:
    exec(0, f.read().split("\n"), err)

  consts["__path"].append(x)
  consts["__path"].append(ox.removesuffix(".wf"))

  return True
