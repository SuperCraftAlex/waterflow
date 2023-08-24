import os

def value(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 2:
    err("Invalid arguments for \"assert\" command!")
    return False

  a = args[0]
  b = args[1]

  left = vars[a] if a in vars.keys() else (consts[a] if a in consts.keys() else (funs[a] if a in funs.keys() else None))
  right = vars[b] if b in vars.keys() else (consts[b] if b in consts.keys() else (funs[b] if a in funs.keys() else None))

  if left != right or left == None or right == None:
    err(f"assert failed: {a}, {b}!")
    return False

  return True

def defined(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 1:
    err("Invalid arguments for \"assert\" command!")
    return False

  a = args[0]

  if not (a in vars.keys() or a in funs.keys() or a in consts.keys()):
    err(f"assert_def failed: {a}!")
    return False

  return True

def undefined(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 1:
    err("Invalid arguments for \"assert\" command!")
    return False

  a = args[0]

  if a in vars.keys() or a in funs.keys() or a in consts.keys():
    err(f"assert_ndef failed: {a}!")
    return False

  return True
