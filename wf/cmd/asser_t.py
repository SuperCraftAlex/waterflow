import os

def value(cmd, args, funs, vars, consts, exec_stack, exec, pval):
  if len(args) != 2:
    print("Invalid arguments for \"assert\" command!")
    return False

  a = args[0]
  b = args[1]

  left = vars[a] if a in vars.keys() else (consts[a] if a in consts.keys() else (funs[a] if a in funs.keys() else None))
  right = vars[b] if b in vars.keys() else (consts[b] if b in consts.keys() else (funs[b] if a in funs.keys() else None))

  if left != right or left == None or right == None:
    print("assert failed!")
    return False

  return True

def defined(cmd, args, funs, vars, consts, exec_stack, exec, pval):
  if len(args) != 1:
    print("Invalid arguments for \"assert\" command!")
    return False

  a = args[0]

  if not (a in vars.keys() or a in funs.keys() or a in consts.keys()):
    print("assert_def failed!")
    return False

  return True

def undefined(cmd, args, funs, vars, consts, exec_stack, exec, pval):
  if len(args) != 1:
    print("Invalid arguments for \"assert\" command!")
    return False

  a = args[0]

  if a in vars.keys() or a in funs.keys() or a in consts.keys():
    print("assert_ndef failed!")
    return False

  return True
