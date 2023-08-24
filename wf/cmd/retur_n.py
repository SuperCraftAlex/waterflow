import os

def single(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 1:
    err("Invalid arguments for \"setret\" command!")
    return False

  vars["R"] = pval(args[0], err)

  return True
