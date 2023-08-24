def single(cmd, args, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) == 0:
    err("Not enought arguments for \"!\" (single) command!")
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

  stack = exec_stack([" ".join(rargs)], list(map(lambda x: pval(x, err),ins)), pval, exec, funs, vars, consts, err)
  sp = len(stack)-1

  for out in outs:
    if sp < 0:
      err("Cannot pop more values from stack in \"!\" (single) command!")
      return False

    if out in consts.keys():
      err("Cannot pop into constant!")
      return False

    if not out in vars.keys():
      err("Cannot pop into undefined variable!")
      return False

    vars[out] = stack[sp]
    sp -= 1

  return True


def block(cmd, args, block, funs, vars, consts, exec_stack, exec, pval, err):
  if len(args) != 0:
    err("Too many arguments for \"!\" command!")
    return False

  exec_stack(block, [], pval, exec, funs, vars, consts, err)
  return True
