def single(cmd, args, funs, vars, consts, exec_stack, exec, pval):
  if len(args) != 1:
    print("Invalid arguments for \"undef\" command!")
    return False

  x = args[0]

  if x in vars.keys():
    del vars[x]

  if x in consts.keys():
    del consts[x]

  if x in funs.keys():
    del funs[x]

  return True
