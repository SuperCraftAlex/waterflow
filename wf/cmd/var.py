import os

def single(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) < 1 or len(args) > 2:
    err("Invalid arguments for \"var\" command!")
    return False

  if len(args[0]) < 3:
    err("Variable names need to be at least 3 chars!")
    return False

  name = args[0]

  if name in consts.keys() or name in vars.keys():
    err("Cannot redefine variable \"" + name + "\"!")
    return False

  if len(args) == 2:
    vars[name] = pval(args[1])
    return True

  vars[name] = 0.0
  return True
