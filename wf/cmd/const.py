import os

def single(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 2:
    err("Invalid arguments for \"const\" command!")
    return False

  if len(args[0]) < 3:
    err("Constant names need to be at least 3 chars!")
    return False

  name = args[0]

  if name in consts.keys() or name in vars.keys():
    err("Cannot redefine constant \"" + name + "\"!")
    return False

  consts[name] = pval(args[1], err)

  return True
