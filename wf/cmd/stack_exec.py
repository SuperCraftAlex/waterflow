def single(cmd, args, funs, vars, consts, exec_stack, exec, pval):
  if len(args) == 0:
    print("Not enought arguments for \"!\" (single) command!")
    return False

  rargs = []
  outs = []
  ins = []
  for arg in args:
    if arg.endswith(">"):
      ins.append(arg[:-1])
      continue

    if arg.startswith(">"):
      outs.append(arg[1:])
      continue

    rargs.append(arg)

  stack = exec_stack([" ".join(rargs)], list(map(lambda x: pval(x),ins)), pval, exec, funs, vars, consts)
  sp = len(stack)-1

  for out in outs:
    if sp < 0:
      print("Cannot pop more values from stack in \"!\" (single) command!")
      return False

    if out in consts.keys():
      print("Cannot pop into constant!")
      return False

    if not out in vars.keys():
      print("Cannot pop into undefined variable!")
      return False

    vars[out] = stack[sp]
    sp -= 1

  return True


def block(cmd, args, block, funs, vars, consts, exec_stack, exec, pval):
  if len(args) != 0:
    print("Too many arguments for \"!\" command!")
    return False

  exec_stack(block, [], pval, exec, funs, vars, consts)
  return True
