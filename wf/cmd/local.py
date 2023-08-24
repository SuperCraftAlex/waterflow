import os

def single(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) < 1 or len(args) > 2:
    err("Invalid arguments for \"local\" command!")
    return False

  if len(args[0]) < 3:
    err("Variable (/local) names need to be at least 3 chars!")
    return False

  name = args[0]

  if (lambda nl: nl(name) or nl("__local_" + name))(lambda n: n in consts.keys() or n in vars.keys()):
    err("Cannot redefine variable \"" + name + "\"!")
    return False

  if len(args) == 2:
    vars["__local_" + name] = pval(args[1], err)
    return True

  vars["__local_" + name] = 0.0
  return True
